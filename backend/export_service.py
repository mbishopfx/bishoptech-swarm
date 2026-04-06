from fpdf import FPDF
import io
import models

def generate_swarm_pdf(run_id: int, db_session):
    run = db_session.query(models.SwarmRun).filter(models.SwarmRun.id == run_id).first()
    if not run:
        return None
        
    logs = db_session.query(models.RunLog).filter(models.RunLog.run_id == run_id).order_by(models.RunLog.timestamp).all()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"BishopTech Swarm Run #{run_id}", ln=True, align='C')
    pdf.ln(10)
    
    # Input
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Original Input Prompt:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, txt=run.input_prompt)
    pdf.ln(5)
    
    # Phases
    for log in logs:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"Phase: {log.agent_name}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, txt=log.output)
        pdf.ln(5)
        
    # Final Result
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Final Synthesis:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, txt=run.final_output if run.final_output else "Incomplete")
    
    return pdf.output() # returns bytes
