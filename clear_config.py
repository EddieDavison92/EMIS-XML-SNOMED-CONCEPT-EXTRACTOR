import os
import configparser
from directory_functions import save_config, load_config

# The path to the config.ini file
config_file_path = "config.ini"

# Initialize configparser and read existing config file
config = configparser.ConfigParser()
config.read(config_file_path)

# Set all values in [DEFAULT] to blank
config['DEFAULT']['xml_directory'] = ''
config['DEFAULT']['database_path'] = ''
config['DEFAULT']['transitive_closure_db_path'] = ''
config['DEFAULT']['history_db_path'] = ''
config['DEFAULT']['output_dir'] = ''

# Write the changes back to config.ini
with open(config_file_path, 'w') as configfile:
    config.write(configfile)

print("Reset all config values to default.")