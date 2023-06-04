import argparse
import os
import shutil
import logging
import tempfile

from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name="wt-util")
logger.setLevel(logging.DEBUG)


currdir=os.path.dirname(os.path.abspath(__file__))
options = {
        "original_settings_filepath" : "",
        "backup_dir":os.path.join(currdir,"backup")
}

def parse_cmd_arguments():
    parser = argparse.ArgumentParser(prog="wt-util",
                                     description="Script to update windows terminal settings json",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s","--settings",
                        type=str,
                        help="full path to windows terminal settings.json",
                        required=True)
    return parser.parse_args()

def set_options(cmd_options):
    options["original_settings_filepath"] = cmd_options.settings

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
    return "{}_{}_{}_{}_{}_{}".format(date.day,date.month,date.year,
                                    time.hour,time.minute,time.second)

def check_options():
    if(not os.path.isfile(options["original_settings_filepath"])):
        raise FileNotFoundError("Incorrect settings json path")

def get_backup_filepath():
    os.makedirs(options["backup_dir"],exist_ok=True)
    backup_filepath = os.path.join(options["backup_dir"],
                                   "settings_bk_{}.json".format(get_timestr()))
    return backup_filepath

def main():
    cmd_options = parse_cmd_arguments()
    set_options(cmd_options)
    check_options()
    create_backup_settings(get_backup_filepath())

if __name__ == "__main__":
    main()
    #test()
