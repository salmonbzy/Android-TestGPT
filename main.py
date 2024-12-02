from android_testgpt import io, parser
from android_testgpt import config
from android_testgpt.uiautomator import uiautomator
import sys
import argparse
import time
import uiautomator2 as u2

if __name__ == "__main__":  
    command_parser = argparse.ArgumentParser(description='Generate auto-testing for Android Applications')
    command_parser.add_argument('--log', type=str, help='Path to log file')
    command_parser.add_argument('--app', type=str, help='Application Name')
    command_parser.add_argument('--out', type=str, help='File to store uiautomator2 command')
    args = command_parser.parse_args()

    ui = uiautomator()
    # Parse the log file
    parsed_logs = io.parse_log_file(args.log)
    instructions = parser.parse(parsed_logs, ui)
    ui.write_to_stdout()
    d = u2.connect(config.DEVICE_NAME)
    d.app_stop(args.app)
    time.sleep(5)
    d.app_start(args.app)
    time.sleep(10)
    ui.exec(d)
    ui.write_to_file(args.out)


