import requests
import os
import sys
import yaml
import mock_responses
import help_text
from stately import Stately
from ui import UI
from configly import ConfigManager

## local development
account = "l7bUFStJQKiGVxTaq-eySg"
org = "default"
project = "default_project"

# TODO: pull account/org/project from env variables
# TODO: command line argument to get manual input










def make_api_call(method, url, headers={}, payload=None):
#   magic = "pat.l7bUFStJQKiGVxTaq-eySg.66326bbca6e1b52844ca35a5.EhZWc6lkwMOnLaCMCQj3"
#   headers["x-api-key"] = magic

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


def write_to_file(filename, content):
    # create output directory
    # TODO: this python script must be executed from the same directory
    os.makedirs("output", exist_ok=True)

    # Write to file, overwrite
    with open(filename, 'w') as f:
        yaml.dump(content, f)


def handle_get_pipelines(configs):
    print("\n== GETTING PIPELINES ==\n")
    account = configs['source_account']
    org = configs['source_org']
    project = configs['source_project']
    pat = configs['source_pat']

    pipeline_url = f"https://app.harness.io/v1/orgs/{org}/projects/{project}/pipelines?page=0&limit=3"
    print(pipeline_url)
    header = { "Harness-Account": account, "x-api-key": pat}

    # GET LIST OF PIPELINES
    print("\n++ Getting list of pipelines... ++")
    res, pipe_list = make_api_call("GET", pipeline_url, header, None)
    # TODO: DEBUG: return mock response
    # pipe_list = mock_responses.get_mock_pipeline_list()

    # Check if project has no pipelines
    # TODO: EXIT when no pipelines are found
    if len(pipe_list) == 0:
       print("No pipelines found in this project...")
    
    for x in pipe_list:

        identifier = x["identifier"]
        print(f"\n++ Getting pipeline definition for {identifier} ++")
        # print("Found pipeline:", x["name"])

        # get current pipeline and assemble URL
        get_pipeline_url = f"https://app.harness.io/v1/orgs/{org}/projects/{project}/pipelines/{identifier}"

        ################ GET PIPELINE DEFINITION ################
        # DEBUG: Turn this back on
        res_status, pipe_def = make_api_call("GET", get_pipeline_url, header, None)
        # pipe_def = mock_responses.mock_pipeline_definition()

        ################ WRITE TO FILE #############
        # Get pipeline YAML
        pipeline_yaml = pipe_def["pipeline_yaml"]

        # Check if YAML exists
        if pipeline_yaml is None:
        #    raise KeyError(f"Unable to find element: {pipeline_yaml}")
           print(f"ERROR: No YAML found for {identifier}. Skipping.")
        else:
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
         configs = configger.get_config()
         handle_get_pipelines(configs)
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