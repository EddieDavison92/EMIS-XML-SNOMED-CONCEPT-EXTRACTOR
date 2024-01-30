import tkinter as tk
import customtkinter as ctk
from directory_functions import initialize_directory_structure, insert_path, select_directory, validate_and_clear_invalid_paths, check_log_file_exists, save_config
from text import header, content
import os
import sys
import subprocess
import threading
import webbrowser
import logging
import shutil
from collections import deque

# Initialize directory
config_file_path, script_path, xml_directory, database_path, transitive_closure_db_path, history_db_path, output_dir = initialize_directory_structure()

# Define an empty list to hold the entries
entries = []

ctk.set_default_color_theme("dark-blue")

class TextHandler(logging.Handler):
    def __init__(self, text_widget, max_logs=5000):
        logging.Handler.__init__(self)
        self.text_widget = text_widget
        self.log_cache = deque(maxlen=max_logs)
        # Start a periodic update of the text widget
        self._schedule_update()

    def _schedule_update(self):
        self.text_widget.after(10, self._update_display)

    def _update_display(self):
        self.text_widget.config(state=tk.NORMAL)
        while self.log_cache:
            log_entry = self.log_cache.popleft()
            self.text_widget.insert(ctk.END, log_entry + '\n')
            self.text_widget.see(ctk.END)
        self.text_widget.config(state=tk.DISABLED)
        self._schedule_update()

    def emit(self, record):
        log_entry = self.format(record)
        self.log_cache.append(log_entry)

class CustomLabelFrame(ctk.CTkFrame):
    def __init__(self, parent, text="", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = ctk.CTkLabel(self, text=text)
        self.label.grid(row=0, column=0, sticky="w", padx=5, pady=2)

class Instructions(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(justify=ctk.LEFT, anchor='nw')

def main():
    # Create the main window
    root = ctk.CTk()
    root.title("EMIS XML SNOMED Concept Extractor")
    root.geometry("1245x560")
    root.resizable(False, False)  # Prevent window from being resized

    # Create a frame for the instructions and input fields
    main_frame = ctk.CTkFrame(root, fg_color="transparent")
    main_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky="nsew")

    # Adjust the weights of the rows inside main_frame
    main_frame.grid_rowconfigure(0, weight=3)  # Make Instructions frame take up more space
    main_frame.grid_rowconfigure(1, weight=1)  # Make Configuration frame take up less space

    # Create a frame for the instructions inside the main frame
    instructions_frame = ctk.CTkFrame(main_frame)
    instructions_frame.grid(row=0, column=0, padx=5, pady=2, sticky='nsew')

    # Style the header and content labels
    header_label = ctk.CTkLabel(instructions_frame, font=("",16), text=header(), wraplength=520, justify='left', anchor='nw')
    content_label = ctk.CTkLabel(instructions_frame, text=content(), wraplength=520, justify='left', anchor='nw')
    
    header_label.pack(padx=5, pady=(5,0))
    content_label.pack(padx=5, pady=(2,5))

    # Create a frame for the input fields inside the main frame
    input_frame = CustomLabelFrame(main_frame, text="Configuration")
    input_frame.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")

     # Add a title above the input boxes in the `input_frame`
    config_title_label = ctk.CTkLabel(input_frame, text="Configuration", font=("",16,"bold"))
    config_title_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=5)
    
    # Add input fields with default values
    labels = ["XML Input Directory", "DMWB NHS SNOMED.mdb", "DMWB NHS SNOMED Transitive Closure.mdb", "DMWB NHS SNOMED History.mdb", "Output Directory"]
    for i, (label_text, default_value) in enumerate(zip(labels, [xml_directory, database_path, transitive_closure_db_path, history_db_path, output_dir])):
        row_num = i + 1  # Start from 1 to leave the 0th row for the title
        ctk.CTkLabel(input_frame, text=label_text, anchor='w',).grid(row=row_num, column=0, sticky="w", padx=5, pady=5)
        entry = ctk.CTkEntry(input_frame, width=320)
        insert_path(entry, default_value.replace('\\\\', '\\'))
        entry.grid(row=row_num, column=1, padx=5, pady=5)

        btn = ctk.CTkButton(input_frame, text="Browse")
        if label_text.endswith(".mdb"):
            btn.configure(command=lambda e=entry: (lambda: insert_path(e, select_directory(e.get(), file_mode=True).replace('\\\\', '\\')))())
        else:
            btn.configure(command=lambda e=entry: (lambda: insert_path(e, select_directory(e.get()).replace('\\\\', '\\')))())

        btn.grid(row=row_num, column=2, padx=5, pady=5)

        entries.append(entry)

    validate_and_clear_invalid_paths(entries)

    # Create a frame for the log display
    log_display_frame = ctk.CTkFrame(input_frame)
    log_display_frame.grid(row=len(labels) + 2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew") # row number changed here
    log_display_frame.grid_rowconfigure(0, weight=1)
    log_display_frame.grid_columnconfigure(0, weight=1)

    # Use basic Text widget from tkinter here, as customtkinter doesn't seem to provide a replacement.
    from tkinter import Text, Scrollbar, ttk
    log_display = Text(log_display_frame, height=18, width=60, wrap=ctk.WORD, state=tk.DISABLED)
    log_display.grid(row=0, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(log_display_frame, orient="vertical", command=log_display.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    log_display.config(yscrollcommand=scrollbar.set)

    def setup_logger(output_dir):
        logger = logging.getLogger("main_logger")
        logger.handlers = []
        handler = TextHandler(log_display)
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        file_handler = logging.FileHandler(os.path.join(output_dir, "log.txt"), encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger

    def clear_log(log_file_path):
        with open(log_file_path, 'w'):
            pass

    # Create and configure logger
    logger = setup_logger(output_dir)

    # Adjusting the log box and adding a title above it
    log_title_label = ctk.CTkLabel(input_frame, text="Execution Log",font=("",16,"bold"))
    log_title_label.grid(row=len(labels) + 1, column=0, sticky="w", padx=5, pady=5)  # row number changed here

    check_log_file_exists()

    # Add a frame for the "Run" button outside the input frame
    run_frame = ctk.CTkFrame(root, fg_color="transparent")
    run_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=(0,5), sticky="e")
    run_btn = ctk.CTkButton(run_frame, text="Run", command=lambda: run_script(entries))
    run_btn.pack(side="right", padx=5, pady=5)

    # Create a frame for the license button 
    license_frame = ctk.CTkFrame(root, fg_color="transparent")
    license_frame.grid(row=2, column=0, padx=5, pady=(0,5), sticky="w")

    def open_license():
        webbrowser.open('https://www.gnu.org/licenses/gpl-3.0.txt')

    license_btn = ctk.CTkButton(license_frame, text="License", command=open_license)
    license_btn.pack(side="left", padx=10, pady=5)

    def get_log_file_path():
        """Return the path to the log file."""
        return os.path.join(entries[-1].get(), "log.txt")

    def open_log_file():
        os.startfile(get_log_file_path())

    def update_open_log_button_visibility():
        if os.path.exists(get_log_file_path()):
            open_log_btn.pack(side="left", padx=10, pady=5)
        else:
            open_log_btn.pack_forget()

    open_log_btn = ctk.CTkButton(run_frame, text="Open Log", command=open_log_file)

    def run_consolidate_workbooks(entries=None):
        def execute_subprocess():
            # Locate an external Python interpreter
            python_interpreter = shutil.which('python')
            if not python_interpreter:
                logger.warning("External Python interpreter not found. Falling back to the current interpreter.")
                python_interpreter = sys.executable

            # Construct the path to your script
            script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'consolidate_workbooks.py')

            # Set source_dir
            source_dir = output_dir

            # Build the full command with arguments
            full_command = [python_interpreter, script_path, '--source_dir', source_dir, '--output_dir', output_dir]

            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            process = subprocess.Popen(
                full_command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                universal_newlines=True,
                creationflags=creation_flags
            )
            logger.info("Consolidate Workbooks subprocess started")

            def stream_output(pipe, log_func):
                for line in iter(pipe.readline, ''):
                    log_func(line.strip())
                pipe.close()

            # Start threads for stdout and stderr
            stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, logger.info))
            stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, logger.error))
            stdout_thread.start()
            stderr_thread.start()

            process.wait()

            if process.returncode != 0:
                logger.error(f"Consolidate Workbooks script failed with error code {process.returncode}.")

            # Check for log file after the script completes
            update_open_log_button_visibility()

        # Start the subprocess in a separate thread
        threading.Thread(target=execute_subprocess).start()

    consolidate_button = ctk.CTkButton(run_frame, text="Consolidate Workbooks", command=run_consolidate_workbooks, width=20)
    
    # Modify this function to update the visibility of the new button
    def update_open_log_button_visibility():
        if os.path.exists(get_log_file_path()):
            open_log_btn.pack(side="left", padx=10, pady=5)
            consolidate_button.pack(side="left", padx=10, pady=5)
        else:
            open_log_btn.pack_forget()
            consolidate_button.pack_forget()

    update_open_log_button_visibility()

    # Create a StringVar for the last entry.
    output_dir_var = tk.StringVar(value=entries[-1].get())
    entries[-1].configure(textvariable=output_dir_var)
    output_dir_var.trace_add("write", lambda *args: update_open_log_button_visibility())

    def get_resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def execute_subprocess(args):
        # Attempt to find an external Python interpreter in the system's PATH
        python_interpreter = shutil.which('python')

        if python_interpreter:
            logger.info(f"Using Python interpreter at: {python_interpreter}")
        else:
            python_interpreter = sys.executable
            logger.warning("No Python interpreter found. Please ensure Python is installed and set in the PATH.")

        # Construct the script path using get_resource_path
        script_path = get_resource_path('emis_xml_snomed_extractor.py')

        # Build the full command
        full_command = [python_interpreter, script_path] + args

        creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        process = subprocess.Popen(
            full_command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            universal_newlines=True,
            creationflags=creation_flags
        )
        logger.info("Subprocess started")

        def read_from_pipe(pipe, log_func):
            for line in iter(pipe.readline, ''):
                log_func(line.strip())
            pipe.close()

        # Start threads for stdout and stderr
        stdout_thread = threading.Thread(target=read_from_pipe, args=(process.stdout, logger.info))
        stderr_thread = threading.Thread(target=read_from_pipe, args=(process.stderr, logger.error))
        stdout_thread.start()
        stderr_thread.start()
        stdout_thread.join()
        stderr_thread.join()

        process.wait()

        if process.returncode != 0:
            logger.error(f"Script failed with error code {process.returncode}.")

        # Check for log file after the script completes
        update_open_log_button_visibility()

        return process.returncode

    def run_script(entries=None):
        if entries:
            paths = [entry.get() for entry in entries]
        else:
            paths = [xml_directory, database_path, transitive_closure_db_path, history_db_path, output_dir]

        save_config(entries)
        clear_log(log_file_path=os.path.join(output_dir, "log.txt"))

        args = [
            "--xml_directory", paths[0],
            "--database_path", paths[1],
            "--transitive_closure_db_path", paths[2],
            "--history_db_path", paths[3],
            "--output_dir", paths[4]
        ]

        thread = threading.Thread(target=execute_subprocess, args=(args,))
        thread.start()

    root.mainloop()

if __name__ == "__main__":

    check_log_file_exists() 

    main()