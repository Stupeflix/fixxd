import yaml
import os

FIXXD_CONFIG_FILENAME = ".fixxd"

FIXXD_DEFAULT_CONFIG = {"path": {"tests": "./", "results": "./tmp/results/", "builds":
                                 "./tmp/builds/"}, "compatibility": ["iphone"], "hardware": ["device", "simulator"]}


def get_config(current_dir):
    """
    The function will go through parent directories until it found a .fixxd yaml and read it.
    For params not defined in the .fixxd it will use the `FIXXD_DEFAULT_CONFIG` values.
    """
    values = {}

    values["config_path"] = get_config_path(current_dir)
    if not values["config_path"]:
        raise Exception("No .fixxd found in parent folders from {0}".format(current_dir))

    config_dir = os.path.dirname(values["config_path"])
    values["config_dict"] = get_config_values(values["config_path"])
    if not values["config_dict"]:
        raise Exception("Wrong yaml at path {0}".format(values["config_path"]))

    # Mandatory
    values["app_name"] = values["config_dict"]["app_name"]
    path_values = values["config_dict"].get("path")
    default_path_values = FIXXD_DEFAULT_CONFIG["path"]

    values["tests_dir"] = get_dir_value(config_dir, path_values, default_path_values, "tests")
    values["results_dir"] = get_dir_value(config_dir, path_values, default_path_values, "results")
    values["builds_dir"] = get_dir_value(config_dir, path_values, default_path_values, "builds")

    values["compatibility"] = values["config_dict"].get("compatibility") or FIXXD_DEFAULT_CONFIG["compatibility"]
    values["hardware"] = values["config_dict"].get("hardware") or FIXXD_DEFAULT_CONFIG["hardware"]

    return values


def get_dir_value(base_dir, dictionnary, default_dict, key):
    if dictionnary:
        path = dictionnary.get(key) or default_dict[key]
    else:
        path = default_dict[key]

    if os.path.isabs(path):
        return path

    return os.path.abspath(os.path.join(base_dir, path))


def get_config_path(current_dir):
    file_path = os.path.join(current_dir, FIXXD_CONFIG_FILENAME)

    if os.path.exists(file_path):
        return file_path

    if os.path.ismount(current_dir):
        return None

    parent = os.path.abspath(os.path.join(current_dir, "../"))
    if os.path.exists(parent):
        return get_config_path(parent)

    return None


def get_config_values(config_path):
    stream = open(config_path, 'r')
    return yaml.load(stream)
