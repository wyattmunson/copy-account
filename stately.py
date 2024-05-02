class Stately:
    def __init__(self):
      self.account = None
      self.current_menu = "main"
      self.current_selection = None
      self.current_action = None
      self.prev_menu = None
      self.prev_selection = None
      self.prev_action = None
      self.menu_trail = []
      self.last_action = None

    def set_current_selection(self, input):
      self.current_selection = input
    

    def get_current_state(self):
       return {
          "account": self.account,
          "current_menu": self.current_menu,
          "current_selection": self.current_selection,
          "current_action": self.current_action,
          "prev_menu": self.prev_menu,
          "prev_selection": self.prev_selection,
          "prev_action": self.prev_action,
          "menu_trail": self.menu_trail,
          "last_action": self.last_action
        }

    
    def reset_state(self):
       self.current_menu = "main"
       self.current_selection = None
       self.current_action = None
       self.menu_trail = []
    
    def get_next_action(self):
      print("DEBUG: Getting next action...")
      self.prev_menu = self.current_menu
      self.prev_selection = self.current_selection

      tree = {
         "1": { "type": "menu", "name": "main", "children": {
            "1": { "type": "action", "name": "view_settings"},
            "2": { "type": "action", "name": "update_settings"},
         }},
         "2": { "type": "menu", "name": "get_pipes"}
      }

      mainm = {"1": "system", "2": "get_pipes"}
      systemm = {"1": "view_settings", "2": "update_settings"}
      next_action = None
      if self.current_selection == "x":
         next_action = "back"
      elif self.current_menu == "main":
         next_action = mainm.get(self.current_selection, self.current_selection)
      elif self.current_menu == "system":
         next_action = systemm.get(self.current_selection, self.current_selection)
      else:
         print("ERROR: No matching next action")
         

      self.current_action = next_action
      self.current_menu = next_action
      self.menu_trail.append(self.current_selection)
      print("MENU TRAIL is", self.menu_trail)
      return next_action

         # TODO: reset state here?
    #   next_action = None
    #   if self.current_menu == "main":
    #      next_action = mainm.get(self.current_selection, self.current_selection)
    #      self.current_action = next_action
    #      self.current_menu = next_action
    #      self.menu_trail.append(self.current_selection)
    #      print("MENU TRAIL is", self.menu_trail)
    #      return next_action
    #   elif self.current_menu == "system":
    #      next_action = systemm.get(self.current_selection, self.current_selection)
    #      self.current_action = next_action
    #      self.current_menu = next_action
    #      self.menu_trail.append(self.current_selection)
    #      print("MENU TRAIL is", self.menu_trail)
    #      return next_action
    #   else:
    #      print("ERROR: No matching next action")
    #      # TODO: reset state here?

