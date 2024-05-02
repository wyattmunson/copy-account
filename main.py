import requests
import os
import sys
import yaml
import mock_responses
import help_text
from stately import Stately
from ui import UI

## local development
account = "l7bUFStJQKiGVxTaq-eySg"
org = "default"
project = "default_project"

# TODO: pull account/org/project from env variables
# TODO: command line argument to get manual input







class ConfigManager:
    def __init__(self):
        print("DEBUG: Initlizating config...")
        print()

        def check_var(var, prompt):
           res = os.environ.get(var)
           if res is None:
              print(f"ERROR: Environment variable {var} not supplied")
              res = input(prompt)
           else:
            print(f"INFO: Got {var} from environment variable")
           return res

        # CHECK FOR ENV VARS ON STARTUP
        # self.source_account = "os.environ.get('MY_HARNESS_ACCOUNT') if not KeyError else None"
        # self.source_org = "os.environ.get('MY_HARNESS_ORG') if not KeyError else None"
        # self.source_project = "os.environ.get('MY_HARNESS_PROJECT') if not KeyError else None"
        # self.source_account = os.environ.get('MY_HARNESS_ACCOUNT') if not KeyError else None
        self.source_account = check_var("MY_HARNESS_ACCOUNT", "Enter ACCOUNT ID for SOURCE account: ")
        self.source_org = check_var("MY_HARNESS_ORG", "ENTER ORG ID for SOURCE account: ")
        self.source_project = check_var("MY_HARNESS_PROJECT", "Enter PROJECT ID for SOURCE account: ")
        self.target_account = os.environ.get('TARGET_HARNESS_ACCOUNT')
        self.target_org = os.environ.get('TARGET_HARNESS_ORG')
        self.target_project = os.environ.get('TARGET_HARNESS_PROJECT')
        self.target_api_key = os.environ.get('TARGET_HARNESS_API_KEY')

    def get_config(self):
       return {
          "source_account": self.source_account,
          "source_org": self.source_org,
          "source_project": self.source_project
       }
    
    def update_config(self, config_name, value):
       print(config_name)
       if hasattr(self, config_name):
          setattr(self, config_name, value)
       else:
        print(f"Error: Attribute '{config_name}' does not exist.")
    
    def get_current_settings(self):
       # check source configs are all set
       source_set = True if all([self.source_account, self.source_org, self.source_project]) else False
       print("SOURCE ACCOUNT SET:\t", source_set)
       target_set = True if all([self.target_account, self.target_org, self.target_project]) else False
       print("TARGET ACCOUNT SET:\t", target_set)
       
       # system configs
       current_dir = os.getcwd()
       print("CURRENT DIR:\t\t", current_dir)
       code_dir = os.path.dirname(os.path.realpath(__file__))
       print("CODE PATH:\t\t", code_dir)
       # check dir mismatch
       if current_dir != code_dir:
          print(f"WARN: This code is being executed from a different directory. Execute this code in {code_dir}")
       
       res = {
          "source_account": self.source_account,
          "source_org": self.source_org,
          "source_project": self.source_project,
          "target_account": self.target_account,
          "target_org": self.target_org,
          "target_project": self.target_project,
       }
       return res
    def get_current_configs(self):
       res = {
          "source_account": self.source_account,
          "source_org": self.source_org,
          "source_project": self.source_project,
          "target_account": self.target_account,
          "target_org": self.target_org,
          "target_project": self.target_project,
       }
       return res



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



def process_arguments():
   print("DEBUG: Processing system arguments...")
   if len(sys.argv) < 2:
      print("DEBUG: No system args provided")
    #   return
   else:
    first = sys.argv[1]
    # check for help
    if first in ["-h", "help"]:
        help_text.render_help_text()


def update_settings(ui, configger):
   ui.print_menu_title("Update Settings")
   print()
   print("The SOURCE account is the account to DOWNLOAD configurations from")
   print("The TARGET account is the account to UPLOAD configrations to")
   print()
   print("")
   
   existing_configs = configger.get_current_configs()
   def get_input(prompt, var_name):
      existing_value = existing_configs[var_name]
      usr_input = input(f"Enter {prompt} [{existing_configs[var_name]}]: ")
      if len(usr_input) == 0 and existing_value is not None:
         print("INFO: Value did not change, original kept")
         # value does not change
         pass
      else:
         # update value
         pass
         configger.update_config(var_name, usr_input)
         configger.get_config()


#    msg = f"Enter source account id [{existing_configs['source_account']}]: "
   get_input("source account id", "source_account")
   get_input("source org id", "source_org")
   get_input("source project id", "source_project")
   get_input("target account id", "target_account")
   get_input("target org id", "target_org")
   get_input("target project id", "target_project")
   print("\nINFO: Configs updated successfully. New configs below.")
   print(configger.get_current_configs())

   hold = input("\nSUCCESS. Hit ENTER to CONTINUE.")
#    source_account = 

def system_handler(ui, stately, configger):
   # print system menu
   ui.print_system_menu()
   user_input = ui.get_input(allowed_values=["1", "2"])
   print("Got input back", user_input)
   #   TODO: handle bad user inpuit
   stately.update_input(user_input)
   next_action = stately.get_next_action()

   if next_action == "view_settings":
    #   print("\n== CURRENT SETTINGS ==")
      ui.print_menu_title("CURRENT SETTINGS")
      print(configger.get_current_settings())
      hold = input("\nPress ENTER to CONTINUE.")
      pass
   elif next_action == "update_settings":
      print("Updating settings screen rendering...")
      update_settings(ui, configger)
   else:
      print("No action caught: system_handler")

    # reset state to main menu
   print("DEBUG: Resetting state...")
   stately.reset_state()


   # get input, and show next menu or option


def show_current_configs():
   print("CURRENT SETTINGS")
   print()

def main():
   print("RUNNING MAIN")
   process_arguments()
   ui = UI()
   stately = Stately()
   configger = ConfigManager()

   ui.print_welcome_screen()

   while True:
      ui.get_main_menu()
      user_input = ui.get_input(allowed_values=["1", "2"])
      stately.update_input(user_input)
      next_action = stately.get_next_action()

      if next_action == "system":
         system_handler(ui, stately, configger)
         pass
      elif next_action == "get_pipes":
         print("Going to got pipes")
      else:
         print("No action caught")


# class App:
#     def __init__(self):
#       self.stately = Stately
#       self.ui = UI
#       process_arguments()
    

#     def run(self):
#       while True:
#         self.ui.get_main_menu()
#         user_input = UI.get_input(allowed_values=["1", "2"])
#         #   TODO: handle bad user inpuit
#         print("Got input back", user_input)
#         self.stately.update_input(self, user_input)
#         next_action = self.stately.get_next_action(self)
#         print("Next action: ", next_action)

#         if next_action == "system":
#             pass
#         elif next_action == "get_pipes":
#             print("Going to got pipes")
#         else:
#             print("No action caught")
#     #   pass



# if __name__ == "__main__":
#    app = App()
#    app.run()
   

main()