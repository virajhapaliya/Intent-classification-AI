import os
import requests
from dotenv import load_dotenv
load_dotenv()

API_ENDPOINT = os.getenv('API_ENDPOINT')

# class ApiRequests():
#     def __init__(self) -> None:
#         self.url_slug = ""
#         self.ai_response = ""
    


# def api_request(url_slug,ai_response):
    

#     url = f"{API_ENDPOINT}/{url_slug}/"

#     payload = {key: '' for key in payload_data[url_slug]}
#     for key,value in payload.items():
#         payload[key] = ai_response[key]

#     response = requests.request("POST", url, headers={}, data=payload)

#     print(response.text)

    
def make_request(url,payload):
    """ Perform API request using give URL and payload 

    Args:
        url (str): Based on url slug make API request
        payload (dict): request body data

    Returns:
                is_success(bool): To check response is correct or not

        ai_response(str): Message to display in output
        
        json_response(dict): API response dictionary
    """
    try:
        response = requests.request("POST", url, headers={}, data=payload)
        json_response = response.json()
        if response.status_code==200:
            return True,json_response['result']['message'],json_response
        else:
            return False, json_response['result']['message'],json_response
    except Exception as e:
        print(response.content)
        return False,'Request error try again'  ,{}  


def api_request(url_slug,ai_response):
    """ Based url slug decide which API call to make

    Args:
        url_slug (str): URL endpoint
        ai_response (dict): AI response in formatted manner

    Returns:
        is_success(bool): To check response is correct or not

        ai_response(str): Message to display in output
        
        json_response(dict): API response dictionary
    """
    url = f"{API_ENDPOINT}/{url_slug}/"

    if url_slug == 'add-student':
       payload = {'first_name':ai_response['first_name'],
                'last_name':ai_response['last_name'],
                'student_id':ai_response['student_id'],
                
                }
       is_success,ai_response,json_response = make_request(url,payload)
       
    elif url_slug == 'update-score':
        payload = {'first_name':ai_response['first_name'],
                'last_name':ai_response['last_name'],
                'subject_name':ai_response['subject_name'],
                'score':ai_response['score']
                }
        is_success,ai_response,json_response = make_request(url,payload)
    elif url_slug == 'get-subject-info-stundet':
        payload = {'first_name':ai_response['first_name'],
                'last_name':ai_response['last_name'],
                'student_id':ai_response['student_id'],    
                }
        first_name = ai_response['first_name']
        is_success,ai_response,json_response = make_request(url,payload)
        if is_success:
            data = json_response['result']['data']
            subjects = ",".join([each_subject['subject_name'] for each_subject in data])
            ai_response = f"Here is the subject of student name {first_name} : {subjects}"

    elif url_slug == 'calculate-score':
        payload = {'subject_name':ai_response['subject_name']}
        subject_name = ai_response['subject_name']
        is_success,ai_response,json_response = make_request(url,payload)
        if is_success:
            data = json_response['result']['data']
            ai_response = f"Score for each student who have opted for {subject_name} : \n"
            for each_student in data:
                ai_response = ai_response + f"\t Student {each_student['student_name']} : {each_student['score']} Marks \n"
    return is_success,ai_response,json_response

    

    

    