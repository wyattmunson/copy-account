import os
import yaml
import api 

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
    res, pipe_list = api.make_api_call("GET", pipeline_url, header, None)
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
        res_status, pipe_def = api.make_api_call("GET", get_pipeline_url, header, None)
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