import sys
import mock_responses
import help_text
import handle_pipelines
import handle_system
from stately import Stately
from ui import UI
from configly import ConfigManager

# TODO: command line argument to get manual input

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
      stately.set_current_selection(user_input)
      next_action = stately.get_next_action()

      if next_action == "system":
         handle_system.system_handler(ui, stately, configger)
         pass
      elif next_action == "get_pipes":
         print("Going to got pipes")
         configs = configger.get_config()
         handle_pipelines.handle_get_pipelines(configs)
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
#         self.stately.set_current_selection(self, user_input)
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