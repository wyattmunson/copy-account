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
   should_show = True
   while should_show:
    print(stately.get_current_state())
    # print system menu
    ui.print_system_menu()
    user_input = ui.get_input(allowed_values=["1", "2", "x"])
    print("Got input back", user_input)
    #   TODO: handle bad user inpuit
    stately.set_current_selection(user_input)
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
    elif next_action == "back":
        should_show = False
    else:
        print("No action caught: system_handler")

    # reset state to main menu
   print("DEBUG: Resetting state...")
   stately.reset_state()


   # get input, and show next menu or option
