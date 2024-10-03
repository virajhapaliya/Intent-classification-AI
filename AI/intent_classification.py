# import requests
# from langchain.llms.base import LLM
# from typing import Optional, List

# class TogetherAI(LLM):
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         self.endpoint = "https://api.together.xyz/api/v1/generate"

#     def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
#         headers = {
#             "Authorization": f"Bearer 119f7604f4af63820030eb010ff7f1c6582ee7aa31795d6e0b285f538301b11b",
#             "Content-Type": "application/json"
#         }

#         data = {
#             "model": "together/opt-13b",  # You can specify the model here
#             "prompt": prompt,
#             "max_tokens": 100  # Adjust max tokens based on your requirements
#         }

#         response = requests.post(self.endpoint, json=data, headers=headers)
#         if response.status_code == 200:
#             return response.json()['generated_text']
#         else:
#             raise Exception(f"Failed to generate text: {response.status_code}, {response.text}")

#     @property
#     def _identifying_params(self) -> dict:
#         return {"api_key": self.api_key}

#     @property
#     def _llm_type(self) -> str:
#         return "together"  # Specify the type of LLM

# # Example Usage
# if __name__ == "__main__":
#     api_key = "119f7604f4af63820030eb010ff7f1c6582ee7aa31795d6e0b285f538301b11b"
#     llm = TogetherAI(api_key=api_key)

#     prompt = "Write a short story about a brave knight."
#     print(llm(prompt))
import os
import requests
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

os.environ["TOGETHER_API_KEY"] = os.getenv('TOGETHER_API_KEY')
API_ENDPOINT = os.getenv('API_ENDPOINT')
# from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain.prompts import PromptTemplate

from langchain_together import ChatTogether
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.pydantic_v1 import BaseModel, Field
from prompt import PROMPT
from pydantic import BaseModel, Field, model_validator
from api_handler import api_request

payload_data = {
        'add-student': ['first_name','last_name','student_id'],
        'update-score':['first_name','last_name','subject_name','score'],
        'get-subject-info-stundet':['first_name','last_name'],
        'calculate-score':['subject_name']
    }

class IntentParser(BaseModel):
    """Pydantic parser for AI response formating

    Args:
        BaseModel 
    """
    intent: str = Field(description="Intent of user query")
    first_name: str = Field(description='name of the student')
    last_name: str = Field(description='name of the student')
    subject_name: str = Field(description='subject of student')
    student_id: str = Field(description='students ID')
    score: str = Field(description='student score')
    api_endpoint: str = Field(description='student score')


def check_api_body_requirements(response):
    """ Before making API request we make sure the payload requirement satiesfied.

    Args:
        response (dict): AI response alogn with required fields

    Returns:
        str: Response from the AI
    """
    required_fields = []
    ai_response = "Unable to understand your query professor, please provide detailed description..."
    if response['api_endpoint'] in payload_data.keys():
        body_data = payload_data[response['api_endpoint']]
        for each_comp in body_data:
            if not response[each_comp]:
                required_fields.append(each_comp)
                break
        if len(required_fields)>0:
            ai_response = f"please profressor provide this all this fields to performe above task. fields : {" ".join(body_data)}"
            return ai_response
        else:
            is_success,ai_response,json_response = api_request(url_slug=response['api_endpoint'],ai_response=response)

    return ai_response




def prepare_endpoints():
    """ API endpoints along with description

    Returns:
        str: Structured String to add inside prompt
    """
    endpoints = {
        'add-student':"This endpoints used to add new student in db.",
        'update-score':"This endpoints is used to update the score of particular users.",
        'get-subject-info-stundet':"This endpoints is used to get information aboue the subjects particular has opted for",
        'calculate-score': "This endpoint is used to calculate score for particular subject or provide information about particular subject opted by different student along with score."
    }
    count = 1
    structure_endpoints = ""
    for each_endpoint, desc in endpoints.items():
        structure_endpoints = structure_endpoints +f"\n{count}. {each_endpoint}\n - {desc}\n"
        count += 1
    return structure_endpoints


def generate_chain():
    """Generate LLM Chain for conversation

    Returns:
        LLMChain: RAG chain to ask query and get response
    """
    api_endpoint = prepare_endpoints()
    parser = JsonOutputParser(pydantic_object=IntentParser) 

    llm = ChatTogether(
            model="meta-llama/Llama-3-70b-chat-hf",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            )
    prompt_template = PromptTemplate(input_variables=["input"], 
                            template=PROMPT,
                            partial_variables={"format_instructions": parser.get_format_instructions(),
                                            "api_endpoint":api_endpoint}) 
    
    chain = prompt_template | llm | parser

    return chain

if __name__ == "__main__":
    
    llm_chain = generate_chain()
    while True:
        user_query = input("Professor :  ")
        response = llm_chain.invoke(user_query)
        print(response)
        ai_response = check_api_body_requirements(response)
        print(f"AI : {ai_response}")
        print('------------------------------------------')

