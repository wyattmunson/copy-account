class Stately:
    def __init__(self):
      self.account = None
      self.current_menu = "main"
      self.current_selection = None
      self.current_action = None
      self.prev_menu = None
      self.prev_selection = None
      self.prev_action = None

    def update_input(self, input):
      self.current_selection = input
    #   mainm = {"1": "system", "2": "get_pipes"}
    #   if self.current_menu == "main":
    #      self.current_action = mainm.get(input, input)
    
    def reset_state(self):
       self.current_menu = "main"
       self.current_selection = None
       self.current_action = None
    
    def get_next_action(self):
      print("DEBUG: Getting next action...")
      mainm = {"1": "system", "2": "get_pipes"}
      systemm = {"1": "view_settings", "2": "update_settings"}
      if self.current_menu == "main":
         next_action = mainm.get(self.current_selection, self.current_selection)
         self.current_action = next_action
         self.current_menu = next_action
         return next_action
      elif self.current_menu == "system":
         next_action = systemm.get(self.current_selection, self.current_selection)
         self.current_action = next_action
         self.current_menu = next_action
         return next_action
      else:
         print("ERROR: No matching next action")
         # TODO: reset state here?

