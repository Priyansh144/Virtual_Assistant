"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import google.generativeai as genai
from config import apikey

genai.configure(api_key=apikey)

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 2048,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.0-pro-001",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "essay on ai\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "**Artificial Intelligence: Transforming the Modern Landscape**\n\nIn the ever-evolving realm of technology, Artificial Intelligence (AI) has emerged as a transformative force, revolutionizing industries, reshaping society, and redefining the boundaries of human capabilities. AI refers to the simulation of human intelligence in machines that are programmed to perform complex tasks and make intelligent decisions.\n\n**Economic Implications**\n\nAI has significant economic implications, creating new industries, automating tasks, and enhancing productivity. AI-powered systems automate repetitive and time-consuming processes, freeing up human workers to focus on more creative and strategic tasks. Furthermore, AI enables businesses to analyze vast amounts of data, identify patterns, and make informed decisions that optimize operations and increase profitability.\n\n**Healthcare Advancements**\n\nAI is also making significant strides in healthcare. AI algorithms can analyze patient data to identify at-risk individuals, diagnose diseases with greater accuracy, and tailor treatment plans. Medical imaging technologies powered by AI assist doctors in diagnosing and treating complex conditions like cancer and neurological disorders. Additionally, AI-enabled robotic surgery systems offer greater precision and reduced recovery times.\n\n**Autonomous Systems**\n\nOne of the most visible applications of AI is in the development of autonomous systems, such as self-driving cars and drones. AI-powered algorithms enable machines to navigate complex environments, make decision",
      ],
    },
  ]
)

response = chat_session.send_message("email on resignation")

print(response)
'''
response:
GenerateContentResponse(
    done=True,
    iterator=None,
    result=protos.GenerateContentResponse({
      "candidates": [
        {
          "content": {
            "parts": [
              {
                "text": "Dear [Manager's name],\n\nPlease accept this email as my formal resignation from my position as [Your position] at [Company name], effective two weeks from today, [Last date of employment].\n\nI want to express my sincere gratitude for the opportunity to work at [Company name] for the past [Number] years. I have learned and grown both professionally and personally during my time here. I appreciate the valuable experience and guidance I have received from you and my colleagues.\n\nDuring my tenure, I have had the privilege of working on several challenging and rewarding projects that have contributed to the success of the company. I am particularly proud of my work on [Specific project or accomplishment], which resulted in [Quantifiable results].\n\nI have carefully considered my decision to resign, and it was not made lightly. I have recently been offered a position at another company that aligns more closely with my long-term career goals. This new opportunity will allow me to further develop my skills and contribute to a different industry.\n\nI am committed to ensuring a smooth transition during my notice period. I will do everything I can to assist with the handover of my responsibilities and support the team in any way possible.\n\nThank you again for the incredible opportunity to work at [Company name]. I wish you and the company all the best in the future.\n\nSincerely,\n[Your name]"
              }
            ],
            "role": "model"
          },
          "finish_reason": "STOP",
          "index": 0,
          "safety_ratings": [
            {
              "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
              "probability": "NEGLIGIBLE"
            },
            {
              "category": "HARM_CATEGORY_HATE_SPEECH",
              "probability": "NEGLIGIBLE"
            },
            {
              "category": "HARM_CATEGORY_HARASSMENT",
              "probability": "NEGLIGIBLE"
            },
            {
              "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
              "probability": "NEGLIGIBLE"
            }
          ]
        }
      ],
      "usage_metadata": {
        "prompt_token_count": 275,
        "candidates_token_count": 278,
        "total_token_count": 553
      }
    }),
)

'''