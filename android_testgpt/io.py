import re
import sys

def parse_log_file(file_path):
    """
    Parse a log file to extract device name, actual command, and parameter.

    Args:
        file_path (str): Path to the log file.

    Returns:
        list of dict: A list of parsed log entries.
    """
    log_entries = []

    # Define the regex pattern to extract the required fields
    pattern = re.compile(
        r"^\[.*?\]\s+(/dev/input/\S+):\s+(\S+)\s+(\S+)\s+(\S+)"
    )

    # Read the log file and parse each line
    try:
        with open(file_path, 'r') as log_file:
            for line in log_file:
                line = line.strip()  # Remove leading/trailing whitespace
                if not line or line.startswith("#"):  # Skip empty lines or comments
                    continue

                match = pattern.match(line)
                if match:
                    device_name = match.group(1)
                    command = match.group(2)
                    actual_command = match.group(3)
                    parameter = match.group(4)

                    log_entries.append({
                        "device_name": device_name,
                        "command": command,
                        "actual_command": actual_command,
                        "parameter": parameter
                    })
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    return log_entries

def main():
    # Ensure a file path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python io.py <log_file>")
        sys.exit(1)

    # Get the log file path from the command-line arguments
    log_file_path = sys.argv[1]

    # Parse the log file
    parsed_logs = parse_log_file(log_file_path)

    # Print the parsed logs
    for entry in parsed_logs:
        print(f"Device: {entry['device_name']}, Command: {entry['command']}, "
              f"Actual Command: {entry['actual_command']}, Parameter: {entry['parameter']}")

if __name__ == "__main__":
    main()
