import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = "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"


def generate_study_plan(resume_text, skills):
    """
    Generate a study plan using OpenAI's GPT model.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the user's resume and match it with the provided skills list. "
                               "Create a personalized study plan with 3-5 key topics, their descriptions,and where to study them "
                },
                {
                    "role": "user",
                    "content": f"Resume: {resume_text}\nSkills: {', '.join(skills)}"
                }
            ],
            temperature=0.5,
            max_tokens=1000
        )
        # Parse and structure the response
        plan = response['choices'][0]['message']['content']
        
        # Assuming the LLM returns a structured JSON string (you may need to fine-tune this part)
        import json
        return json.loads(plan) if plan else {"error": "LLM returned an empty plan."}
    
    except openai.error.AuthenticationError as e:
        print(f"OpenAI Authentication error: {e}")
        return {"error": "Failed to authenticate with OpenAI API"}
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return {"error": "Failed to generate study plan via OpenAI API"}
    except json.JSONDecodeError as e:
        print(f"JSON Parse Error: {e}")
        return {"error": "Failed to parse the study plan from LLM response."}
