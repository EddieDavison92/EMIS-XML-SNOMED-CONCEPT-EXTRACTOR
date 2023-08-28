import os
import configparser

# Get the directory where the script is running
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the absolute path to config.ini
config_path = os.path.join(script_dir, 'config.ini')

# Load config values from config.ini if arguments are not provided
config = configparser.ConfigParser()
config.read(config_path)

xml_directory = config['DEFAULT'].get('xml_directory', '')
database_path = config['DEFAULT'].get('database_path', '')
transitive_closure_db_path = config['DEFAULT'].get('transitive_closure_db_path', '')
history_db_path = config['DEFAULT'].get('history_db_path', '')
output_dir = config['DEFAULT'].get('output_dir', '')
