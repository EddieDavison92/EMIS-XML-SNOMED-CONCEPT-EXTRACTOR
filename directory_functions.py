import os
import configparser
import sys
import logging
import tkinter as tk
from tkinter import filedialog

# Create logger object
logger = logging.getLogger("main_logger")

def determine_application_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.info(f"Folder {folder_path} created.")
    else:
        logger.info(f"Folder {folder_path} already exists.")

def load_config(config_file_path):
    config = configparser.ConfigParser()
    try:
        config.read(config_file_path)
        return config
    except Exception as e:
        logger.error(f"An error occurred while loading config: {e}")
        return None

def save_config(entries):
    config['DEFAULT'] = {
        'xml_directory': entries[0].get(),
        'database_path': entries[1].get(),
        'transitive_closure_db_path': entries[2].get(),
        'history_db_path': entries[3].get(),
        'output_dir': entries[4].get()
    }

    with open(config_file_path, 'w') as config_file:
        config.write(config_file)
    logger.info(f"Saved config to {config_file_path}")

# Initialize directory and load config at file load
application_path = determine_application_path()
config_file_path = os.path.join(application_path, 'config.ini')
config = load_config(config_file_path)

def initialize_directory_structure():
    global xml_directory, database_path, transitive_closure_db_path, history_db_path, output_dir
    
    # Determine the script path dynamically
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)
    script_path = os.path.join(application_path, 'emis_xml_snomed_extractor.py')
    
    # Paths for your specific needs, initialized from config if available
    config_file_path = config.get('DEFAULT', 'config_file_path', fallback=os.path.join(application_path, 'config.ini'))
    xml_directory = config.get('DEFAULT', 'xml_directory', fallback=os.path.join(application_path, 'xml_directory'))
    database_path = config.get('DEFAULT', 'database_path', fallback=os.path.join(application_path, 'database'))
    transitive_closure_db_path = config.get('DEFAULT', 'transitive_closure_db_path', fallback=os.path.join(database_path, 'transitive_closure'))
    history_db_path = config.get('DEFAULT', 'history_db_path', fallback=os.path.join(database_path, 'history'))
    output_dir = config.get('DEFAULT', 'output_dir', fallback=os.path.join(application_path, 'output'))
    
    for path in [os.path.dirname(config_file_path), script_path, xml_directory, database_path, transitive_closure_db_path, history_db_path, output_dir]:
        create_folder(path)

    return config_file_path, script_path, xml_directory, database_path, transitive_closure_db_path, history_db_path, output_dir

initialize_directory_structure()

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

def check_log_file_exists():
    global log_file_exists
    log_file_path = os.path.join(output_dir, "script_log.txt")
    if os.path.exists(log_file_path):
        log_file_exists = True
