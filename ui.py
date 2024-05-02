class UI:
    def __init__(self):
       self.ui_on = True

    
    def get_input(self, prompt="Select an option: ", allowed_values=[]):
      is_valid_input = False
      # error handling
      while is_valid_input is False:
        user_input = input(prompt)
        if len(allowed_values) == 0:
            is_valid_input = True
            return user_input
        else:
            # print("DEBUG: Checking allowed values")
            if user_input in allowed_values:
                # print("DEBUG: Input is valid")
                is_valid_input = True
            
                return user_input
            print("ERROR: Input rejected. Select a valid value.")
            print()
    
    
    def print_welcome_screen(self):
       print()
       print("====================================================================")
       print(" HARNESS PIPELINE COPY TOOL ")
       print(" Move Harness resources (pipelines, services, ect.) between account")
       print()
       print(" Harness (C) 1974 - Punched Card and Magnetic Tape Division")
       print("====================================================================")
    
    def print_menu_title(self, title):
       header_len = len(title) + 4
       print()
       print("=" * header_len)
       print("=", title, "=")
       print("=" * header_len)
       

    def print_menu_options(self, title, options, exit_option=True, main_menu_option=True, help_option=False):
       self.print_menu_title(title)
       for index, x in enumerate(options):
          print(f"{index + 1}.", x)
       
       if help_option: print("h. Help")
       if main_menu_option: print("m. Main menu")
       if exit_option: print("x. Exit / back")


    def print_system_menu(self):
       menu_options = ["View current settings", "Update configs"]
       self.print_menu_options("SYSTEM SETTINGS", menu_options)
       print()


    def get_main_menu(self):
       menu_options = ["Settings", "Copy pipelines"]
       self.print_menu_options("MAIN MENU", menu_options)
       print()
    #    print("=== MAIN MENU ===")
    #    print("1. See config")
    #    print("2. Copy pipelines")
    #    print()