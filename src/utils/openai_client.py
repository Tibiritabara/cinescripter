import openai
import os

openai.organization = "org-czXc4M0WuVvsw2uD75ZTa4Z1"
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text):
  response = openai.Embedding.create(
    model="text-embedding-ada-002",
    input=text
  )
  return response.data[0].embedding

def generate_video_script(user_question, script_prompt, tone):
  system_prompt=f'''
    You are an assistant that generates a youtube video script in a "{tone}" tone to answer questions about "{user_question}" \

    Generate the script content based on the answers provided by the user and following steps: \

    1. Greet the audience \
    2. Introduce the topic \ 
    3. Explain the topic in 3000 words \
    4. Specify video transitions \
    5. Wrap up the video \ 
    6. Invite to subscribe to the youtube channel \
  '''

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": script_prompt},
      ]
  )
  return response["choices"][0]["message"]["content"]
