import requests

try:
    url = "https://github.com/Amanmulla7171/IIT-GENAI-94394/blob/main/Assignment/Day01/data.json"
    response = requests.get(url)
    print("status code:", response.status_code)
  
    data = response.json()
    print("resp data: ", data)
except:
    print("Some error occured.")