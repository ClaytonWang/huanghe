import yaml


def convert_yaml_to_dict(file_name: str):
    with open(file_name) as f:
        config = yaml.safe_load(f)
        return config
