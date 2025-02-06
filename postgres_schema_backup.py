import subprocess
import datetime
import os
import logging
import json

# Setup logging
log_file = os.path.join(os.getcwd(), "backup_script.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_file,
    filemode="a",
)

def disconnect_drive(drive_name):
    """Disconnect the network drive if it exists."""
    subprocess.run(f'net use {drive_name}: /D /Y', shell=True)

def map_drive(drive_name, drive_user, drive_password):
    """Map the network drive."""
    command = fr'net use {drive_name}: /D'
    subprocess.run(command, shell=True, capture_output=True, text=True)

    command_2 = fr'net use {drive_name}: \\FRNAS02\gaic\GAICImplCommon\{drive_name} /USER:castcorp\{drive_user} {drive_password}'
    result_2 = subprocess.run(command_2, shell=True, capture_output=True, text=True)
    
    if result_2.returncode == 0:
        logging.info(f"{drive_name} Drive mapped successfully!")
    else:
        logging.error(f"Failed to map drive: {result_2.stderr}")


def backup_postgres_schema():
    try:
        current_directory = os.getcwd()

        with open(current_directory + "\\backup_config.json", "r") as config_file:
            config = json.load(config_file)

        host = config["css"]["host"]
        port = config["css"]["port"]
        database = config["css"]["database"]
        user = config["css"]["user"]
        password = config["css"]["password"]
        schema = config["css"]["schema"]
        pg_dump_path = config["css"]["pg_dump_path"]
        backup_dir = config["backup"]["backup_dir"]
        drive_name= config["map_drive"]["name"]
        drive_user = config["map_drive"]["user"]
        drive_password = config["map_drive"]["password"]


        # Disconnect existing drive
        disconnect_drive(drive_name)

        # Map new drive
        map_drive(drive_name, drive_user, drive_password)

        # Ensure backup directory exists
        os.makedirs(backup_dir, exist_ok=True)

        # Generate backup file name with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        backup_file = os.path.join(backup_dir, f"{schema}_backup_{timestamp}.sql")


        # Set environment variable for password
        env = os.environ.copy()
        env["PGPASSWORD"] = password

        # Run pg_dump command to backup schema in plain SQL format
        with open(backup_file, "w") as f:
            command = [
                pg_dump_path,
                "-h", host,
                "-p", str(port),
                "-U", user,
                "-d", database,
                "-n", '"' + schema + '"',
                "-F", "p"  # Plain text SQL format
            ]

            # print(command)
            subprocess.run(command, env=env, stdout=f, stderr=subprocess.PIPE, check=True)

        logging.info(f"Backup successful: {backup_file}")

    except subprocess.CalledProcessError as e:
        logging.error(f"pg_dump process failed: {e.stderr}")
    except KeyError as e:
        logging.error(f"Missing key in configuration: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Error reading configuration file: {e}")
        exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    backup_postgres_schema()
