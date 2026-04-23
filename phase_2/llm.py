#llm access for real world data through api
# groq api used 
import os # to get api key securely
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )

 #print(os.getenv("GROQ_API_KEY"))  # check whether your api working or not 
