import requests

#First I define the API endpoint URL
url = 'https://flask-api-sah3.onrender.com/mutant'

#Then I define the request body
dna_data = {
    'dna': ["ATGCGT", "AAGTGT", "ATGATT", "AGATGT", "GCGTAA", "TCACTT"]
}

#This snippet sends the POST request
try:
    response = requests.post(url, json=dna_data)
    
    #Finally it prints the status code and response
    if response.status_code == 200:
        print("Success: Mutant DNA detected")
    elif response.status_code == 403:
        print("Forbidden: Human DNA detected")
    elif response.status_code == 402:
        print("Error:", response.json().get("error", "Unknown error"))
    else:
        print(f"Unexpected status code: {response.status_code}")
        print("Response:", response.text)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
