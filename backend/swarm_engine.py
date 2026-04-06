import os
from litellm import completion
import models
from datetime import datetime
import rag_service

def call_llm(system_prompt: str, user_prompt: str, api_choice: str):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Force Gemini for "Super Gemini" multi-agent swarm
    model_name = "gemini/gemini-3.1-pro-latest"
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment."
    
    try:
        response = completion(
            model=model_name,
            messages=messages,
            api_key=api_key
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling Gemini: {str(e)}"

def run_swarm_pipeline(run_id: int, db_session):
    run = db_session.query(models.SwarmRun).filter(models.SwarmRun.id == run_id).first()
    if not run:
        return
        
    run.status = "running"
    db_session.commit()
    
    try:
        # Check for RAG context
        rag_context = ""
        if run.use_rag and run.kb_id:
            try:
                rag_context = rag_service.query_rag(run.kb_id, run.input_prompt)
            except Exception as e:
                print(f"RAG Error: {str(e)}")
        
        agents = db_session.query(models.SwarmAgent).filter(
            models.SwarmAgent.swarm_id == run.swarm_id
        ).order_by(models.SwarmAgent.sequence_order).all()
        
        current_context = f"Original Request:\n{run.input_prompt}\n"
        if rag_context:
            current_context = f"Context from Knowledge Base:\n{rag_context}\n\n" + current_context
            
        final_result = ""
        
        for agent_link in agents:
            template = db_session.query(models.AgentTemplate).filter(
                models.AgentTemplate.id == agent_link.agent_template_id
            ).first()
            
            agent_input = current_context
            output = call_llm(template.system_prompt, agent_input, template.default_api)
            
            log = models.RunLog(
                run_id=run.id,
                agent_name=template.name,
                input_context=agent_input,
                output=output
            )
            db_session.add(log)
            db_session.commit()
            
            current_context += f"\n--- Output from {template.name} ---\n{output}\n"
            final_result = output
            
        run.status = "completed"
        run.final_output = final_result
        run.completed_at = datetime.utcnow()
        db_session.commit()
        
    except Exception as e:
        run.status = "failed"
        run.final_output = str(e)
        db_session.commit()
