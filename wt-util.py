import argparse
import os
import shutil
import logging
import tempfile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name="wt-util")
logger.setLevel(logging.DEBUG)


options = {}

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(prog="wt-util",
                                     description="Script to update windows terminal settings json",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s","--settings",
                        type=str,
                        help="full path to windows terminal settings.json",
                        required=True)
    return parser.parse_args()

def backup_settings(backup_filepath):
    logger.debug("Creating backup of settings json")
    shutil.copy2(options["original_settings_filepath"],
                 backup_filepath)
    logger.debug("Successfully created backup of settings json")


def test_backup():
    with tempfile.TemporaryDirectory() as tempdir:
        backup_file = os.path.join(tempdir, "settings_bk.json")
        logger.debug(backup_file)
        backup_settings(backup_file)
        original_file_lines = 0
        backup_file_lines = 0
        with open(options["original_settings_filepath"], 'r') as f:
            original_file_lines = len(f.readlines())

        with open(backup_file, 'r') as f:
            backup_file_lines = len(f.readlines())

        assert original_file_lines == backup_file_lines


def test():
    test_backup()


if __name__ == "__main__":
    cmd_options = parse_cmd_arguments()
    options["original_settings_filepath"] = cmd_options.settings
    #test()
