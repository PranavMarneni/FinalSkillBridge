import openai

def get_skill_set(job_descriptions):
    skills = []
    for desc in job_descriptions:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract key technical skills."},
                {"role": "user", "content": desc}
            ],
            temperature=0,
            max_tokens=150
        )
        extracted = response.choices[0].message['content'].strip().split(", ")
        skills.extend(extracted)
    return list(set(skills))
