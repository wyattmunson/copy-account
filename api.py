import requests 

def make_api_call(method, url, headers={}, payload=None):
  try:
    response = None
    if method == "GET":
        response = requests.get(url, headers=headers)
        print("INFO: GET request successful:", url)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=payload)
        print("INFO: POST request successful:", url)
    else:
       print("ERR: Unsupported HTTP method:", method)
       return False, f"Unsupported HTTP method provided: {method}"
    response.raise_for_status()  # Raise an exception for unsuccessful status codes
    print("INFO: Status code:", response.status_code)

    # extract JSON payload
    data = response.json()
    # print("data:", data)
    return True, data
  except requests.exceptions.RequestException as e:
    print("ERR: Exception raised:", e)
    return False, f"API call failed: {e}"
