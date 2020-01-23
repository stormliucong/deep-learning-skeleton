import json
from dotmap import DotMap
import os
import time


def get_config_from_json(json_file):
    """
    Get the config from a json file
    :param json_file:
    :return: config(namespace) or config(dictionary)
    """
    # parse the configurations from the config json file provided
    with open(json_file, 'r') as config_file:
        config_dict = json.load(config_file)

    # convert the dictionary to a namespace using bunch lib
    config = DotMap(config_dict)

    return config, config_dict


def process_config(json_file):
<<<<<<< HEAD
    if json_file == "None":
        json_file = "/home/jl5307/current_research/work/deep-learning-skeleton/experiments/configs.json"

=======
    if json_file == 'None':
        json_file = os.path.join(os.path.abspath('.'),'./experiments/configs.json')
>>>>>>> a3c980c6c002f1448ce43c218205cce1a600df02
    config, _ = get_config_from_json(json_file)
    config.callbacks.tensorboard_log_dir = os.path.join("experiments", time.strftime("%Y-%m-%d/",time.localtime()), config.exp.name, "logs/")
    config.callbacks.checkpoint_dir = os.path.join("experiments", time.strftime("%Y-%m-%d/",time.localtime()), config.exp.name, "checkpoints/")
    return config