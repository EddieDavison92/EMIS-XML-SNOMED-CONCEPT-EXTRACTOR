# clear_config.py
import configparser

def clear_config_paths():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    config.set('DEFAULT', 'xml_directory', '')
    config.set('DEFAULT', 'database_path', '')
    config.set('DEFAULT', 'transitive_closure_db_path', '')
    config.set('DEFAULT', 'history_db_path', '')
    config.set('DEFAULT', 'output_dir', '')
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    clear_config_paths()
