import argparse
import json
import logging
import os
import shutil
import sys
import tempfile

from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name="wt-util")
logger.setLevel(logging.DEBUG)


currdir = os.path.dirname(os.path.abspath(__file__))
options = {
    "original_settings_filepath": "",
    "backup_dir": os.path.join(currdir, "backup")
}


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(prog="wt-util",
                                     description="Script to update windows terminal settings json",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--settings",
                        type=str,
                        help="full path to windows terminal settings.json",
                        required=True)
    parser.add_argument("-p", "--profile",
                        type=str,
                        help="wt profile name",
                        required=True)
    parser.add_argument("-k", "--key",
                        type=str,
                        help="settings key in the given profile to be updated",
                        required=True)
    parser.add_argument("-v", "--value",
                        type=str,
                        help="new value to be updated for the given key",
                        required=True)
    parser.add_argument("-o", "--output-file",
                        type=str,
                        help="Updated settings will be written to this file.If not given original settings file will be overwritten",
                        default="")
    return parser.parse_args()


def set_options(cmd_options):
    options["original_settings_filepath"] = cmd_options.settings
    options["profile_name"] = cmd_options.profile
    options["settings_key"] = cmd_options.key
    options["settings_value"] = cmd_options.value
    if (cmd_options.output_file != ""):
        options["output_file"] = cmd_options.output_file
    else:
        options["output_file"] = cmd_options.settings


def create_backup_settings(backup_filepath):
    logger.debug("Creating backup of settings json")
    shutil.copy2(options["original_settings_filepath"],
                 backup_filepath)
    logger.debug("Successfully created backup of settings json")


def test_backup():
    with tempfile.TemporaryDirectory() as tempdir:
        backup_file = os.path.join(tempdir, "settings_bk.json")
        logger.debug(backup_file)
        create_backup_settings(backup_file)
        original_file_lines = 0
        backup_file_lines = 0
        with open(options["original_settings_filepath"], 'r') as f:
            original_file_lines = len(f.readlines())

        with open(backup_file, 'r') as f:
            backup_file_lines = len(f.readlines())

        assert original_file_lines == backup_file_lines


def test():
    test_backup()


def get_timestr():
    now = datetime.today()
    date = now.date()
    time = now.time()
    return "{}_{}_{}_{}_{}_{}".format(date.day, date.month, date.year,
                                      time.hour, time.minute, time.second)


def check_options():
    if (not os.path.isfile(options["original_settings_filepath"])):
        raise FileNotFoundError("Incorrect settings json path")


def get_backup_filepath():
    os.makedirs(options["backup_dir"], exist_ok=True)
    backup_filepath = os.path.join(options["backup_dir"],
                                   "settings_bk_{}.json".format(get_timestr()))
    return backup_filepath


def load_json(filepath: str) -> dict:
    with open(filepath, 'r') as file:
        return json.load(file)


def write_json(d: dict, json_filepath: str):
    with open(json_filepath, 'w') as file:
        json.dump(d, file, indent=4)


def get_profile_idx(profiles_list: list, profile_name: str) -> int:
    for idx, profile in enumerate(profiles_list):
        if (profile["name"] == profile_name):
            return idx
    raise ValueError("There is no profile in settings with name %(name)s" % {
                     "name": profile_name})


def get_updated_settings() -> dict:
    settings_dict = load_json(options["original_settings_filepath"])
    profile_idx = get_profile_idx(
        settings_dict["profiles"]["list"], options["profile_name"])
    sys.stdout.write("Profile: {}\n".format(options["profile_name"]))
    sys.stdout.write("Key: {}\n".format(options["settings_key"]))
    sys.stdout.write("Previous value: {}\n".format(
        settings_dict["profiles"]["list"][profile_idx].get(options["settings_key"], '""')))
    sys.stdout.write("New value: {}\n".format(options["settings_value"]))

    settings_dict["profiles"]["list"][profile_idx][options["settings_key"]] = options["settings_value"]
    return settings_dict


def write_settings(settings_dict: dict):
    write_json(settings_dict, options["output_file"])
    sys.stdout.write("Settings updated successfully\n")


def main():
    cmd_options = parse_cmd_arguments()
    set_options(cmd_options)
    check_options()
    create_backup_settings(get_backup_filepath())
    new_settings = get_updated_settings()
    write_settings(new_settings)


if __name__ == "__main__":
    main()
    # test()
