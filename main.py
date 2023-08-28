import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, filedialog
from tkinter import messagebox
from directory_functions import *
import os
import subprocess
import logging
import threading
from collections import deque

class TextHandler(logging.Handler):
    def __init__(self, text_widget, max_logs=500):
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

check_log_file_exists

def main():
    # Create the main window
    root = ctk.CTk()
    root.title("EMIS XML SNOMED Concept Extractor")
    root.geometry("1300x460")
    root.resizable(False, False)  # Prevent window from being resized

    # Define the instructions text and its styling
    header = """EMIS XML SNOMED CONCEPT EXTRACTOR
==================================="""
    content = """Extract and categorise SNOMED codes from EMIS search exports as XML.

Features:
- Supports multiple XML files containing many search definitions.
- Produces an Excel workbook for each EMIS search.
- For each workbook, creates tabs for each codeset.
- Extracts child codes used in EMIS, unless excluded.
- Identifies inactive SNOMED concepts; providing updated IDs.

Instructions:
1. Set file paths on the right.
2. Need the 3 Microsoft Access databases? 
Obtain from NHS TRUD: search for 'SNOMED CT UK Data Migration Workbench' subscirbe and choose the latest version.
3. Place XML file(s) from EMIS in the XML directory.
4. Click 'Run'.

Debugging:
If the script is slow, ensure the databases have indexes configured.

Author:
Eddie Davison | eddie.davison@nhs.net | NHS North Central London ICB
"""
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
    header_label = ctk.CTkLabel(instructions_frame, font=("",16), text=header, wraplength=520, justify='left', anchor='nw')
    content_label = ctk.CTkLabel(instructions_frame, text=content, wraplength=520, justify='left', anchor='nw')
    
    header_label.pack(padx=5, pady=(5,0))
    content_label.pack(padx=5, pady=(2,5))

    # Create a frame for the input fields inside the main frame
    input_frame = CustomLabelFrame(main_frame, text="Configuration")
    input_frame.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")

    # Add input fields with default values
    labels = ["XML Input Directory", "DMWB NHS SNOMED.mdb", "DMWB NHS SNOMED Transitive Closure.mdb", "DMWB NHS SNOMED History.mdb", "Output Directory"]
    for i, (label_text, default_value) in enumerate(zip(labels, [xml_directory, database_path, transitive_closure_db_path, history_db_path, output_dir])):
        ctk.CTkLabel(input_frame, text=label_text, anchor='w',).grid(row=i, column=0, sticky="w", padx=5, pady=5)
        entry = ctk.CTkEntry(input_frame, width=320)
        insert_path(entry, default_value.replace('\\\\', '\\'))
        entry.grid(row=i, column=1, padx=5, pady=5)

        btn = ctk.CTkButton(input_frame, text="Browse")
        if label_text.endswith(".mdb"):
            btn.configure(command=lambda e=entry: (lambda: insert_path(e, select_directory(e.get(), file_mode=True).replace('\\\\', '\\')))())
        else:
            btn.configure(command=lambda e=entry: (lambda: insert_path(e, select_directory(e.get()).replace('\\\\', '\\')))())

        btn.grid(row=i, column=2, padx=5, pady=5)

        entries.append(entry)

   # Create a frame for the log display
    log_display_frame = ctk.CTkFrame(input_frame)
    log_display_frame.grid(row=len(labels) + 1, column=0, columnspan=3, padx=5, pady=2, sticky="nsew")
    log_display_frame.grid_rowconfigure(0, weight=1)
    log_display_frame.grid_columnconfigure(0, weight=1)

    # Use basic Text widget from tkinter here, as customtkinter doesn't seem to provide a replacement.
    from tkinter import Text, Scrollbar, ttk
    log_display = Text(log_display_frame, height=13, width=60, wrap=ctk.WORD, state=tk.DISABLED)
    log_display.grid(row=0, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(log_display_frame, orient="vertical", command=log_display.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    log_display.config(yscrollcommand=scrollbar.set)

     # Adjusting the log box and adding a title above it
    log_title_label = ctk.CTkLabel(input_frame, text="Execution Log:")
    log_title_label.grid(row=len(labels), column=0, sticky="w", padx=5, pady=5)
    
    # Initialize logger for GUI
    handler = TextHandler(log_display)
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Add a frame for the "Run" button outside the input frame
    run_frame = ctk.CTkFrame(root, fg_color="transparent")
    run_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=(0,5), sticky="e")
    run_btn = ctk.CTkButton(run_frame, text="Run", command=lambda: run_script(entries))
    run_btn.pack(side="right", padx=5, pady=5)

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
    update_open_log_button_visibility()

    # Create a StringVar for the last entry.
    output_dir_var = tk.StringVar(value=entries[-1].get())
    entries[-1].configure(textvariable=output_dir_var)
    output_dir_var.trace_add("write", lambda *args: update_open_log_button_visibility())

    def execute_subprocess(args):
        # Check if we are on Windows and set creationflags if so
        creation_flags = 0
        if os.name == 'nt':
            creation_flags = subprocess.CREATE_NO_WINDOW

        process = subprocess.Popen(
            args, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            universal_newlines=True,
            creationflags=creation_flags  # Add this line to suppress the terminal window
        )
        
        def read_from_pipe(pipe, log_func):
            for line in iter(pipe.readline, ''):
                log_func(line.strip())
            pipe.close()

        # Start threads for stdout and stderr
        stdout_thread = threading.Thread(target=read_from_pipe, args=(process.stdout, logging.info))
        stderr_thread = threading.Thread(target=read_from_pipe, args=(process.stderr, logging.error))
        stdout_thread.start()
        stderr_thread.start()
        stdout_thread.join()
        stderr_thread.join()

        process.wait()

        if process.returncode != 0:
            logging.error(f"Script failed with error code {process.returncode}.")

        # Check for log file after the script completes
        update_open_log_button_visibility()

    def run_script(entries):
        paths = [entry.get() for entry in entries]
        save_config(*paths)

        # Construct the arguments for the script
        args = [
            "python", "-u",
            script_path,
            "--xml_directory", paths[0],
            "--database_path", paths[1],
            "--transitive_closure_db_path", paths[2],
            "--history_db_path", paths[3],
            "--output_dir", paths[4]
        ]

        # Start the subprocess in a separate thread
        thread = threading.Thread(target=execute_subprocess, args=(args,))
        thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()