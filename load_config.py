import configparser

# Load config values from config.ini if arguments are not provided
config = configparser.ConfigParser()
config.read('config.ini')

xml_directory = config['DEFAULT']['xml_directory']
database_path = config['DEFAULT']['database_path']
transitive_closure_db_path = config['DEFAULT']['transitive_closure_db_path']
history_db_path = config['DEFAULT']['history_db_path']
output_dir = config['DEFAULT']['output_dir']