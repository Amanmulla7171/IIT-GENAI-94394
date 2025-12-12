import requests
import json

api_url = " https://nilesh-g.github.io/learn-web/data/novels.json"


def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None


def save_to_json(data, output_file):
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)


data_placeholder = fetch_data(api_url)
