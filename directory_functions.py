import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, filedialog
from tkinter import messagebox
import os
import configparser
import sys
import subprocess
import logging
import threading

# Global variables
logger = logging.getLogger('') 
config = configparser.ConfigParser()

if getattr(sys, 'frozen', False):
    config_file_path = os.path.join(sys._MEIPASS, 'config.ini')
else:
    config_file_path = 'config.ini'

config.read(config_file_path)
print(config.has_option('DEFAULT', 'xml_directory'))

if getattr(sys, 'frozen', False):
    script_path = os.path.join(sys._MEIPASS, 'EMIS XML SNOMED CONCEPT EXTRACTOR.py')
else:
    script_path = 'EMIS XML SNOMED CONCEPT EXTRACTOR.py'

xml_directory = config.get('DEFAULT', 'xml_directory')
for section in config.sections():
    print(f"[{section}]")
    for option in config.options(section):
        print(f"{option} = {config.get(section, option)}")
print(os.path.abspath('config.ini'))

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

# Call validate_paths before running the script in run_script function
def run_script(entries):
    validate_paths(entries)
    paths = [entry.get() for entry in entries]

# Default Configuration Values
user_profile = os.environ['USERPROFILE']
xml_directory = config.get('DEFAULT', 'xml_directory')
database_path = config.get('DEFAULT', 'database_path')
transitive_closure_db_path = config.get('DEFAULT', 'transitive_closure_db_path')
history_db_path = config.get('DEFAULT', 'history_db_path')
output_dir = config.get('DEFAULT', 'output_dir')

# Store all entries in a list for easy access
entries = []

def save_config(xml_directory, database_path, transitive_closure_db_path, history_db_path, output_dir):
    config['DEFAULT']['xml_directory'] = xml_directory
    config['DEFAULT']['database_path'] = database_path
    config['DEFAULT']['transitive_closure_db_path'] = transitive_closure_db_path
    config['DEFAULT']['history_db_path'] = history_db_path
    config['DEFAULT']['output_dir'] = output_dir

    # Save to the config_file_path variable
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)

def check_log_file_exists():
    global log_file_exists
    log_file_path = os.path.join(output_dir, "script_log.txt")
    if os.path.exists(log_file_path):
        log_file_exists = True
