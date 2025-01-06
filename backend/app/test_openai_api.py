from services.openai_service import openai  # Adjusted path to match the folder structure
 # Ensure you're importing from your correct service file

def test_openai_api():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, can you confirm you're working?"}
            ]
        )
        print("API Call Successful!")
        print("Response:", response['choices'][0]['message']['content'])
    except Exception as e:
        print("API Call Failed.")
        print("Error:", e)

if __name__ == "__main__":
    test_openai_api()
