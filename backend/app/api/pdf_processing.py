from app.utils.pdf_utils import pdf_to_string
from app.utils.llm_utils import get_skill_set

def process_resume_and_generate_plan(pdf_path, skills):
    """
    Processes a resume PDF and generates a study plan based on extracted skills.
    """
    resume_text = pdf_to_string(pdf_path)
    if not resume_text:
        return {"error": "Failed to extract text from resume PDF."}
    
    # Generate study plan using LLM
    from app.services.openai_service import generate_study_plan  # Lazy import to avoid circular imports
    
    study_plan = generate_study_plan(resume_text, skills)
    return study_plan