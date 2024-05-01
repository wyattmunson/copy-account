import requests
import mock_responses

## local development
account = "l7bUFStJQKiGVxTaq-eySg"
org = "default"
project = "default_project"

# TODO: pull account/org/project from env variables
# TODO: command line argument to get manual input

def main():
    print("COPY PIPELINES")
    handle_get_pipelines()


def make_api_call(method, url, headers={}, payload=None):
  magic = "pat.l7bUFStJQKiGVxTaq-eySg.66326bbca6e1b52844ca35a5.EhZWc6lkwMOnLaCMCQj3"
  headers["x-api-key"] = magic
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
    print("data:", data)
    return True, data
  except requests.exceptions.RequestException as e:
    print("ERR: Exception raised:", e)
    return False, f"API call failed: {e}"

def handle_get_pipelines():
    print("GET PIPELINES...")
    # account = input("Enter account id:")
    # org = input("Enter org id:")
    # project = input("Enter project id:")

    pipeline_url = f"https://app.harness.io/v1/orgs/{org}/projects/{project}/pipelines?page=0&limit=30"
    print(pipeline_url)
    header = { "Harness-Account": account}

    # GET LIST OF PIPELINES
    print("Getting pipelines...")
    # make_api_call("GET", pipeline_url, header, None)
    # TODO: DEBUG: return mock response
    pipe_list = mock_responses.get_mock_pipeline_list()
    # print(pipe_list)

    if len(pipe_list) == 0:
       print("No pipelines found in this project...")
    
    for x in pipe_list:
    #    if x > 1:
    #       return 
       
       print("Found pipeline:", x["name"])
       identifier = x["identifier"]

       get_pipeline_url = f"https://app.harness.io/v1/orgs/{org}/projects/{project}/pipelines/{identifier}"
       pipe_def = make_api_call("GET", get_pipeline_url, header, None)
       print("PIPE DEF", pipe_def)



main()