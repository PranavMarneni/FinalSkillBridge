import openai
from pydantic import BaseModel
import PyPDF2
from .web_scrapper import *

# /Users/pranavmarneni/Documents/GitHub/SkillBridge-HackGT/backend/app/utils/web_scrapper.py
# /Users/pranavmarneni/Documents/GitHub/SkillBridge-HackGT/backend/app/utils/LLM.py
# /Users/pranavmarneni/Documents/GitHub/SkillBridge-HackGT/backend/app/views.py
# /Users/pranavmarneni/Documents/GitHub/SkillBridge-HackGT/backend
# /Users/pranavmarneni/Documents/GitHub/SkillBridge-HackGT/backend/backend
# /Users/pranavmarneni/Documents/GitHub/SkillBridge-HackGT/backend/app/utils/LLM.py


# Import everything from the module
  # or import specific functions like main
 # Relative import
 # If web_scrapper.py is in the app directory

 # Import your web scraper module

# Initialize the OpenAI API key

class CourseraInput(BaseModel):
    searchList: list[str]

class SkillsFormat(BaseModel):
    skillList: list[str]

def getSkillSet(scrapedJobs):
    scrapedSkills = []
    allSkills = []
    for job in scrapedJobs:
        # Prepare previous skills as a string
        previous_skills = ', '.join(scrapedSkills) if scrapedSkills else 'None'

        # Define the messages with the job description included
        messages = [
            {
                "role": "system",
                "content": (
                    f"Extract the key technical computer science skills needed for this job offering. "
                    f"Previous jobs had the following skills: {previous_skills}. "
                    f"Using the information from this job post and previous skills, create a list of 5-6 skills each described in 1-2 key words "
                    f"that are most useful for employment opportunities in these types of jobs."
                )
            },
            {
                "role": "user",
                "content": job  # Pass the job description here
            }
        ]

        # API call to OpenAI's ChatCompletion
        completion = openai.ChatCompletion.create(
            model="gpt-4",  # Ensure you're using the correct model
            messages=messages,
            temperature=0,  # For consistent results
            max_tokens=150
        )
        skills = completion.choices[0].message['content'].strip()

        # Assume skills come as a comma-separated list, parse and clean them
        skills_list = [skill.strip() for skill in skills.split(",")]

        # Update the scrapedSkills and allSkills lists
        scrapedSkills.extend(skills_list)
        allSkills.extend(skills_list)
    
    # Remove duplicates
    uniqueSkills = list(set(allSkills))
    
    return uniqueSkills

# Instead of hardcoding, get scraped jobs from the web_scrapper module
scrapedJobs = main_method()  # Call the web scraper's main function to get job descriptions

if scrapedJobs:
    skills = getSkillSet(scrapedJobs)

class PlanCard(BaseModel):
    topic: str
    description: str
    videoLinks: list[str]

# Function to extract text from a PDF file
def pdf_to_string(pdf_file):
    try:
        with open(pdf_file, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

# Function to generate a study plan based on the resume (PDF text) and required skills
def createStudyPlan(pdf_text, skills):
    messages = [
        {
            "role": "system",
            "content": (
                f"Extract the technical computer science skills the user has on their resume: {pdf_text}. "
                f"Identify skill gaps in their resume compared to the skills jobs are looking for, given here: {skills}. "
                f"Based on that gap, generate a study plan for the user to address these gaps in the format of: "
                f"topic, description, and a list of 3 video links for each topic."
                f"Ensure the video links are valid https or http raw links."
            )
        }
    ]
    
    # API call to OpenAI's ChatCompletion
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
        max_tokens=500
    )

    # Extract the generated study plan from the response
    response_text = completion.choices[0].message['content'].strip()

    # Parsing logic
    topics = response_text.split("\n\n")  # Split based on double newline
    study_plan = []
    
    for topic_text in topics:
        lines = topic_text.strip().split('\n')
        
        # Ensure there are enough lines to extract the expected information
        if len(lines) < 3:
            continue

        topic = lines[0].replace("Topic:", "").strip()
        description = lines[1].replace("Description:", "").strip()
        video_links = [link.strip() for line in lines[2:] for link in line.replace("Video Links:", "").split(",") if link.strip()]

        # Create a PlanCard object
        plan_card = PlanCard(
            topic=topic,
            description=description,
            videoLinks=video_links
        )
        study_plan.append(plan_card)
    
    return study_plan

# Path to your PDF
pdf_path = "/Users/pranavmarneni/Downloads/Main_Resume-2.pdf"
pdf_text = pdf_to_string(pdf_path)


# Generate study plan based on the PDF text and required skills
study_plan = createStudyPlan(pdf_text, skills)

courseraList = []
# Output the study plan
for plan in study_plan[2:]:
    courseraList.append(plan.topic[4:])
    print(plan)

def projectIdeas(skillList):
    messages = [
            {
                "role": "system",
                "content": (
                    f"Based on the provided list of computer science topics : {skillList}"
                    f"Provide a couple of project ideas an undergraduate student can complete to gain experience."
                )
            }
        ]

    # API call to OpenAI's ChatCompletion
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
        max_tokens=500
    )
    print(completion.choices[0].message['content'])

projectIdeas(courseraList)
