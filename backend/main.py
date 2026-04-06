from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import models, schemas, rag_service, export_service
from database import engine, get_db
from worker import run_swarm_task
import io

# Initialize DB and Vector Extensions
models.Base.metadata.create_all(bind=engine)
try:
    rag_service.init_vector_db()
except Exception as e:
    print(f"Warning: Could not initialize vector extension: {e}")

app = FastAPI(title="BishopTech Swarm API")

# --- Agent Templates ---

@app.post("/api/templates", response_model=schemas.AgentTemplate)
def create_template(template: schemas.AgentTemplateCreate, db: Session = Depends(get_db)):
    db_template = models.AgentTemplate(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@app.get("/api/templates", response_model=List[schemas.AgentTemplate])
def read_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    templates = db.query(models.AgentTemplate).offset(skip).limit(limit).all()
    return templates

# --- Swarms ---

@app.post("/api/swarms", response_model=schemas.Swarm)
def create_swarm(swarm: schemas.SwarmCreate, db: Session = Depends(get_db)):
    db_swarm = models.Swarm(name=swarm.name, description=swarm.description)
    db.add(db_swarm)
    db.commit()
    db.refresh(db_swarm)
    
    for agent in swarm.agents:
        db_agent = models.SwarmAgent(
            swarm_id=db_swarm.id,
            agent_template_id=agent.agent_template_id,
            sequence_order=agent.sequence_order
        )
        db.add(db_agent)
    
    db.commit()
    return db_swarm

@app.get("/api/swarms", response_model=List[schemas.Swarm])
def read_swarms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    swarms = db.query(models.Swarm).offset(skip).limit(limit).all()
    return swarms

# --- Knowledge Bases ---

@app.post("/api/knowledge-bases", response_model=schemas.KnowledgeBase)
def create_kb(kb: schemas.KnowledgeBaseCreate, db: Session = Depends(get_db)):
    db_kb = models.KnowledgeBase(**kb.model_dump())
    db.add(db_kb)
    db.commit()
    db.refresh(db_kb)
    return db_kb

@app.get("/api/knowledge-bases", response_model=List[schemas.KnowledgeBase])
def read_kbs(db: Session = Depends(get_db)):
    return db.query(models.KnowledgeBase).all()

@app.post("/api/knowledge-bases/{kb_id}/documents")
async def upload_document(kb_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    kb = db.query(models.KnowledgeBase).filter(models.KnowledgeBase.id == kb_id).first()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
        
    content = await file.read()
    text_content = ""
    
    if file.filename.endswith(".pdf"):
        import pypdf
        pdf_reader = pypdf.PdfReader(io.BytesIO(content))
        for page in pdf_reader.pages:
            text_content += page.extract_text()
    else:
        text_content = content.decode("utf-8")
        
    db_doc = models.Document(kb_id=kb_id, filename=file.filename, content=text_content)
    db.add(db_doc)
    db.commit()
    
    # Background: Ingest into RAG
    rag_service.add_documents_to_rag(kb_id, file.filename, text_content)
    
    return {"status": "uploaded", "id": db_doc.id}

# --- Swarm Runs ---

@app.post("/api/swarms/{swarm_id}/run", response_model=schemas.SwarmRun)
def run_swarm(swarm_id: int, run_create: schemas.SwarmRunCreate, db: Session = Depends(get_db)):
    swarm = db.query(models.Swarm).filter(models.Swarm.id == swarm_id).first()
    if not swarm:
        raise HTTPException(status_code=404, detail="Swarm not found")
        
    db_run = models.SwarmRun(
        swarm_id=swarm_id,
        input_prompt=run_create.input_prompt,
        use_rag=run_create.use_rag,
        kb_id=run_create.kb_id,
        status="pending"
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    
    # Dispatch Celery task
    run_swarm_task.delay(db_run.id)
    
    return db_run

@app.get("/api/runs/{run_id}", response_model=schemas.SwarmRun)
def read_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(models.SwarmRun).filter(models.SwarmRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
        
    logs = db.query(models.RunLog).filter(models.RunLog.run_id == run_id).order_by(models.RunLog.timestamp).all()
    
    run_schema = schemas.SwarmRun.model_validate(run)
    run_schema.logs = [schemas.RunLog.model_validate(l) for l in logs]
    return run_schema

# --- Exports ---

@app.get("/api/runs/{run_id}/export-pdf")
def export_run_pdf(run_id: int, db: Session = Depends(get_db)):
    pdf_bytes = export_service.generate_swarm_pdf(run_id, db)
    if not pdf_bytes:
        raise HTTPException(status_code=404, detail="Run not found")
        
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=swarm_run_{run_id}.pdf"}
    )

@app.post("/api/runs/{run_id}/export-rag")
def export_run_to_rag(run_id: int, kb_id: int, db: Session = Depends(get_db)):
    run = db.query(models.SwarmRun).filter(models.SwarmRun.id == run_id).first()
    if not run or not run.final_output:
        raise HTTPException(status_code=404, detail="Run not found or not completed")
        
    db_doc = models.Document(
        kb_id=kb_id,
        filename=f"Run_{run_id}_Output.txt",
        content=run.final_output
    )
    db.add(db_doc)
    db.commit()
    
    rag_service.add_documents_to_rag(kb_id, db_doc.filename, db_doc.content)
    
    return {"status": "exported_to_rag", "doc_id": db_doc.id}

# --- Chat with Output ---

@app.post("/api/runs/{run_id}/chat")
def chat_with_run(run_id: int, request: schemas.ChatRequest, db: Session = Depends(get_db)):
    run = db.query(models.SwarmRun).filter(models.SwarmRun.id == run_id).first()
    if not run or not run.final_output:
        raise HTTPException(status_code=404, detail="Run not found or not completed")
    
    # Save user message
    user_msg = models.ChatMessage(run_id=run_id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()
    
    # Get history
    history = db.query(models.ChatMessage).filter(models.ChatMessage.run_id == run_id).order_by(models.ChatMessage.timestamp).all()
    
    # Prep Gemini prompt
    gemini_messages = [
        {"role": "system", "content": f"You are a helpful assistant. You are chatting about the following swarm output:\n\n{run.final_output}"},
    ]
    for h in history:
        gemini_messages.append({"role": h.role, "content": h.content})
    
    import os
    from litellm import completion
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")
    
    try:
        response = completion(
            model="gemini/gemini-1.5-pro-latest",
            messages=gemini_messages,
            api_key=api_key
        )
        assistant_content = response.choices[0].message.content
        
        # Save assistant message
        assistant_msg = models.ChatMessage(run_id=run_id, role="assistant", content=assistant_content)
        db.add(assistant_msg)
        db.commit()
        
        return {"response": assistant_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
