from ..utils.web_scraper import get_job_details
from ..utils.llm_utils import get_skill_set
from ..models import UploadedPDF
from ..services.openai_service import generate_study_plan


def process_job_urls(urls):
    job_descriptions = []
    for url in urls:
        job_data = get_job_details(url.url)
        if job_data:
            job_descriptions.append(job_data['description'])
    
    if not job_descriptions:
        return {"error": "No job descriptions found."}
    
    extracted_skills = get_skill_set(job_descriptions)
    
    latest_pdf = UploadedPDF.objects.last()
    if not latest_pdf:
        return {"error": "No PDF available for processing."}
    
    study_plan = generate_study_plan(latest_pdf.text, extracted_skills)
    
    if isinstance(study_plan, dict) and "error" in study_plan:
        return {"error": study_plan["error"]}
    
    return {
        "skills": extracted_skills,
        "study_plan": study_plan  # Pass the study plan directly from the LLM
    }
