import os
import yaml
from chep_utils.logger import get_logger

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def parse_yaml(filepath):
    """
    Parse a YAML file and return dictionary
    Args:
        filepath: Path to the YAML file to be parsed.
    """
    if not os.path.isfile(filepath):
        get_logger().critical("YAML file %s does not exist.", filepath)
    with open(filepath) as f:
        return yaml.safe_load(f)

def yaml_from_dict(to_yaml, path):
    with open(path, "w") as f:
        yaml.safe_dump(to_yaml, f, default_flow_style=False, allow_unicode=False)

def print_dict(to_be_printed, indent=0, skip=None):
    for key, value in to_be_printed.items():
        if isinstance(skip, list) and key in skip:
            continue
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            print_dict(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))
