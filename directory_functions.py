import tkinter as tk
from tkinter import filedialog
import os
import configparser
import sys
import logging

# Global variables
logger = logging.getLogger('') 
config = configparser.ConfigParser()

# Determine where the config.ini and script files should be
if getattr(sys, 'frozen', False):
    config_file_path = os.path.join(sys._MEIPASS, 'config.ini')
    script_path = os.path.join(sys._MEIPASS, 'EMIS XML SNOMED CONCEPT EXTRACTOR.py')
else:
    config_file_path = os.path.abspath('C:/Users/eddie/OneDrive/Documents/Projects/EMIS-XML-SNOMED-CONCEPT-EXTRACTOR/config.ini')
    script_path = os.path.abspath('EMIS XML SNOMED CONCEPT EXTRACTOR.py')

# Debugging logs
logger.info(f"sys._MEIPASS: {getattr(sys, '_MEIPASS', 'N/A')}")
logger.info(f"Current Working Directory: {os.getcwd()}")
logger.info(f"Config file path: {config_file_path}")
logger.info(f"Script path: {script_path}")

# Read the configuration
config.read(config_file_path)

def select_directory(current_value="", file_mode=False):
    """Open a dialog to select a directory or file."""
    initial_dir = os.path.dirname(current_value) if file_mode and current_value else current_value
    if not initial_dir:
        initial_dir = os.getcwd()  # default to current working directory if no initial directory is provided

    if file_mode:
        path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Access Database", "*.mdb"), ("All Files", "*.*")])
    else:
        path = filedialog.askdirectory(initialdir=initial_dir)
    
    return path if path else current_value  # Return the current value if the user cancels the dialog

def insert_path(entry, path):
    """Insert the path into the entry and move the cursor to the end."""
    entry.delete(0, tk.END)
    entry.insert(0, path)
    entry.xview_moveto(1)  # Move the internal view to the end

def validate_paths(entries):
    for entry in entries:
        path = entry.get()
        if not os.path.exists(path):
            entry.delete(0, tk.END)

def validate_and_clear_invalid_paths(entry_widgets):
    for entry in entry_widgets:
        path = entry.get()
        if not os.path.exists(path):
            entry.delete(0, tk.END)

# Function to save the configuration
def save_config(xml_directory, database_path, transitive_closure_db_path, history_db_path, output_dir):
    config['DEFAULT']['xml_directory'] = xml_directory
    config['DEFAULT']['database_path'] = database_path
    config['DEFAULT']['transitive_closure_db_path'] = transitive_closure_db_path
    config['DEFAULT']['history_db_path'] = history_db_path
    config['DEFAULT']['output_dir'] = output_dir

    with open(config_file_path, 'w') as configfile:
        config.write(configfile)

# Store all entries in a list for easy access
entries = []

# Load config values for the first time
xml_directory = config.get('DEFAULT', 'xml_directory', fallback='')
database_path = config.get('DEFAULT', 'database_path', fallback='')
transitive_closure_db_path = config.get('DEFAULT', 'transitive_closure_db_path', fallback='')
history_db_path = config.get('DEFAULT', 'history_db_path', fallback='')
output_dir = config.get('DEFAULT', 'output_dir', fallback='')

def check_log_file_exists():
    global log_file_exists
    log_file_path = os.path.join(output_dir, "script_log.txt")
    if os.path.exists(log_file_path):
        log_file_exists = True


def load_config(entries=None):
    global xml_directory, database_path, transitive_closure_db_path, history_db_path, output_dir
    if os.path.exists(config_file_path):
        logger.info(f"Config file exists at {config_file_path}")
        config.read(config_file_path)
        xml_directory = config.get('DEFAULT', 'xml_directory', fallback='')
        database_path = config.get('DEFAULT', 'database_path', fallback='')
        transitive_closure_db_path = config.get('DEFAULT', 'transitive_closure_db_path', fallback='')
        history_db_path = config.get('DEFAULT', 'history_db_path', fallback='')
        output_dir = config.get('DEFAULT', 'output_dir', fallback='')
    else:
        logger.error(f"Config file not found at {config_file_path}")
        # Use the values from the Tkinter entries as fallbacks if available
        if entries:
            xml_directory = entries[0].get()
            database_path = entries[1].get()
            transitive_closure_db_path = entries[2].get()
            history_db_path = entries[3].get()
            output_dir = entries[4].get()
    logger.info(f"Loading config from {config_file_path}")  # Debugging line

