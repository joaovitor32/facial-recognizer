import sys,yaml

def yaml_data():
    with open('./src/facial_recognizer.yaml', 'r') as stream:
        try:
            input_data = yaml.safe_load(stream)
            return input_data
        except yaml.YAMLError as error:
            print("[ERROR] Error processing YAML file:", error)
            sys.exit(1)