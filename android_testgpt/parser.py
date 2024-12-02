from . import config
from . import uiautomator
from enum import Enum

class Point:
    def __init__(self, point=None):
        if point is not None:
            self.X = point[0]
            self.Y = point[1]
        else:
            self.X = 0
            self.Y = 0

def calculate_screen_coordinates(raw_x_hex, raw_y_hex):
    raw_x = int(raw_x_hex.replace('0x', ''), 16)
    raw_y = int(raw_y_hex.replace('0x', ''), 16)
    scale_factor_x = config.SCREEN_WIDTH / config.MAX_RAW_X
    scale_factor_y = config.SCREEN_HEIGHT / config.MAX_RAW_Y
    screen_x = int(raw_x * scale_factor_x)
    screen_y = int(raw_y * scale_factor_y)
    return screen_x, screen_y



class ParserState(Enum):
    IDLE = 0
    READING_STRING = 1
    READING_MOUSE_INPUT = 2

def parse(parsed_logs, ui):
    state = ParserState.IDLE
    current_string = ''
    p = Point()
    index = 0
    total_entries = len(parsed_logs)

    while index < total_entries:
        entry = parsed_logs[index]
        device_name = entry['device_name']
        command = entry['command']
        actual_command = entry['actual_command']
        parameter = entry['parameter']

        if state == ParserState.IDLE:
            if device_name == config.KEYBOARD_DEVICE:
                state = ParserState.READING_STRING
                continue
            elif device_name == config.MOUSE_DEVICE:
                state = ParserState.READING_MOUSE_INPUT
                continue

        elif state == ParserState.READING_STRING:
            if device_name == config.KEYBOARD_DEVICE:
                if parameter == 'DOWN':
                    key = config.KEY_MAPPING.get(actual_command, config.DEFAULT_KEY_VALUE)
                    # Handle special keys or append to string as needed
                    if key == 'ENTER':
                        print(f"Collected string 1: {current_string}")
                        ui.add_text_input(current_string + "\n")
                        current_string = ''
                        state = ParserState.IDLE
                    elif len(key) == 1:
                        current_string += key
                    else:
                        print(f"Special Key Pressed: {key}")
            elif device_name == config.MOUSE_DEVICE:
                # Transition to mouse input
                print(f"Collected string 2: {current_string}")
                ui.add_text_input(current_string)
                current_string = ''
                state = ParserState.READING_MOUSE_INPUT
                continue

        elif state == ParserState.READING_MOUSE_INPUT:
            if device_name == config.MOUSE_DEVICE:
                if command == 'EV_ABS':
                    if actual_command == 'ABS_MT_POSITION_X':
                        p.X = parameter
                    elif actual_command == 'ABS_MT_POSITION_Y':
                        p.Y = parameter
                        # Calculate screen coordinates
                        p.X, p.Y = calculate_screen_coordinates(p.X, p.Y)
                        print(f"Mouse click at: ({p.X}, {p.Y})")
                        ui.add_point_access(p.X, p.Y)
                elif command == 'EV_SYN' and actual_command == 'SYN_REPORT':
                    # End of mouse event
                    pass
            elif device_name == config.KEYBOARD_DEVICE:
                # Transition back to reading string
                state = ParserState.READING_STRING
                continue

        index += 1



