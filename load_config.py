import configparser

# Load config values from config.ini if arguments are not provided
config = configparser.ConfigParser()
config.read('config.ini')

xml_directory = config['DEFAULT'].get('xml_directory', '')
database_path = config['DEFAULT'].get('database_path', '')
transitive_closure_db_path = config['DEFAULT'].get('transitive_closure_db_path', '')
history_db_path = config['DEFAULT'].get('history_db_path', '')
output_dir = config['DEFAULT'].get('output_dir', '')
