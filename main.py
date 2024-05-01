import requests
import os
import yaml
import mock_responses

## local development
account = "l7bUFStJQKiGVxTaq-eySg"
org = "default"
project = "default_project"

# TODO: pull account/org/project from env variables
# TODO: command line argument to get manual input

class Stately:
    def __init__(self):
      self.account = None
      self.current_menu = "main"
      self.current_selection = None
      self.current_action = None

    def update_input(self, input):
      self.current_selection = input
    #   mainm = {"1": "system", "2": "get_pipes"}
    #   if self.current_menu == "main":
    #      self.current_action = mainm.get(input, input)
    
    def get_next_action(self):
      print("INFO: Getting next action...")
    #   print("INFO: Current Menu: {self.current_menu}, selection: {self.current_selection}")
    #   print("INFO: Current Menu:", self.current_menu, "selection:", self.current_selection)
      mainm = {"1": "system", "2": "get_pipes"}
      if self.current_menu == "main":
         next_action = mainm.get(self.current_selection, self.current_selection)
         print("got next action", next_action)
    #   if self.current_menu == "main" and self.current_selection == 1:
    #      pass
    #      # TODO: render next settings
    #   elif self.current_menu == "main" and self.current_selection == 2:
    #      self.current_action = "get_pipes"
    #      print("Should show ")
    #   else:
    #      print("ERR: No next action found")
    

    # def get_next_menu(self):


class UI:
    def get_main_menu():
       print("=== MAIN MENU ===")
       print("1. See config")
       print("2. Copy pipelines")
    
    def get_input(prompt="Select an option: "):
      user_input = input(prompt)
      return user_input


class ConfigManager:
    def __init__(self):
        self.source_account = None


def main():
   print("RUNNING MAIN")
   ui = UI()
   stately = Stately()
   while True:
      UI.get_main_menu()
      user_input = UI.get_input()
      #   TODO: handle bad user inpuit
      stately.update_input(user_input)
      next_action = stately.get_next_action()
      print("Next action: ", next_action)


    # tester = innie.get_input("somthing meaningful:")
    # print("COPY PIPELINES")
    # handle_get_pipelines()
#    innie.get_input()


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


def write_to_file(filename, content):
    # create output directory
    # TODO: this python script must be executed from the same directory
    os.makedirs("output", exist_ok=True)

    # Write to file, overwrite
    with open(filename, 'w') as f:
        yaml.dump(content, f)


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

    # Check if project has no pipelines
    # TODO: EXIT when no pipelines are found
    if len(pipe_list) == 0:
       print("No pipelines found in this project...")
    
    for x in pipe_list:
    #    if x > 1:
    #       return 
       
        print("Found pipeline:", x["name"])

        # get current pipeline and assemble URL
        identifier = x["identifier"]
        get_pipeline_url = f"https://app.harness.io/v1/orgs/{org}/projects/{project}/pipelines/{identifier}"

        ################ GET PIPELINE DEFINITION ################
        # DEBUG: Turn this back on
        # pipe_def = make_api_call("GET", get_pipeline_url, header, None)
        pipe_def = mock_responses.mock_pipeline_definition()
        # print("PIPE DEF", pipe_def)

        ################ WRITE TO FILE #############
        # Get pipeline YAML
        pipeline_yaml = pipe_def["pipeline_yaml"]

        # Check if YAML exists
        if pipeline_yaml is None:
           raise KeyError(f"Unable to find element: {pipeline_yaml}")
        
        # Write to file
        # TODO: possibly upload entire pipeline definition as it may be needed for create pipeline API
        file_name = f"output/{identifier}.yaml"
        print(f"Writing YAML for {identifier} to {file_name}")
        write_to_file(file_name, pipeline_yaml)








main()