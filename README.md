# Copy Account

## Setup

```bash
python3 -m venv <venv_name>
source <venv_name>/bin/activate

# when finished, deactivate the virtual environment
deactivate

# populated commands
python3 -m venv homestead
source homestead/bin/activate
pip install -r requirements.txt
```

## Environment Variables

```bash
export MY_HARNESS_ACCOUNT="123"
export MY_HARNESS_ORG="234"
export MY_HARNESS_PROJECT="345"
export MY_HARNESS_PAT="SOME_KEY"
export TARGET_HARNESS_ACCOUNT="678"
export TARGET_HARNESS_ORG="789"
export TARGET_HARNESS_PROJECT="890"
export TARGET_HARNESS_PAT="SOME_KEY"
```

## Flow

1. Main starts
1. Get user input for main menu, returned a number
1. Call get_next_action(), this will trigger the state update and return the next menu
   1. Checks current_menu to find the dict with the correct options
   1. Returns next action based on `current_selection`
   1. Get next action from the dict (`get_pipes`)
   1. Update `current_menu` to that action - right now there are no sub-menus so this is unnecessary
   1. Update `current_action` to that action
   1. Return `current_action` (e.g., `get_pipes`) to end the function call
