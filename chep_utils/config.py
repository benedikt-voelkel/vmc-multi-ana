import yaml
from pkg_resources import resource_stream
from chep_utils.io import parse_yaml

def make_config(yaml_path=None, **overwrite):
    # Load defaults
    stream = resource_stream("chep_utils.data", "run_config.yaml")
    config = yaml.safe_load(stream)
    # Load user
    user_config = {}
    if yaml_path is not None:
        user_config = parse_yaml(yaml_path)
    # User config overwrites defaults
    for k in list(config.keys()):
        config[k] = user_config.get(k, config[k])
    # Additional keywords take highest priority and overwrite
    for k in list(overwrite.keys()):
        if overwrite[k] is None:
            del overwrite[k]
    for k in list(config.keys()):
        config[k] = overwrite.get(k, config[k])

    return config



