import os

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
        self.source_pat = check_var("MY_HARNESS_PAT", "Enter PAT TOKEN for SOURCE account: ")
        self.target_account = os.environ.get('TARGET_HARNESS_ACCOUNT')
        self.target_org = os.environ.get('TARGET_HARNESS_ORG')
        self.target_project = os.environ.get('TARGET_HARNESS_PROJECT')
        self.target_pat = os.environ.get('TARGET_HARNESS_PAT')

    def get_config(self):
       return {
          "source_account": self.source_account,
          "source_org": self.source_org,
          "source_project": self.source_project,
          "source_pat": self.source_pat
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
