# POSTGRES SCHEMA BACKUP

## Overview
The postgres_schema_backup project is a Python-based script designed to automate the backup of a PostgreSQL database schema. It connects to a PostgreSQL database, maps a network drive, and performs a backup using the pg_dump utility.

## Features
- Connects to a PostgreSQL database using configuration settings.
- Maps a network drive for storing backup files.
- Generates a timestamped backup file in plain SQL format.
- Logs the backup process for monitoring and troubleshooting.

## Prerequisites
- Python 3.x installed on your system.
- PostgreSQL client tools, specifically pg_dump, must be available in the specified path.
- Access to the network drive where backups will be stored.

## Installation
1. Clone the repository or download the files.
2. Install the required Python packages listed in requirements.txt:

	```bash
	`pip install -r requirements.txt`
	```

## Configuration
Before running the backup script, you need to configure the backup_config.json file. Here’s a breakdown of the configuration options:


```json
{
    "css": {
        "host": "tooling3",                // Database host
        "port": 2284,                       // Database port
        "database": "postgres",             // Database name
        "user": "operator",                 // Database user
        "password": "",                     // Database password (if required)
        "schema": "Imaging_Indicator",      // Schema to backup
        "pg_dump_path": "C:\\Program Files\\Cast\\CastStorageService4\\bin\\pg_dump.exe" // Path to pg_dump
    },
    "backup": {
        "backup_dir": "R:\\IN\\ImagingInidicators\\Backup" // Directory to store backups
    },
    "map_drive": {
        "name": "R",                        // Drive letter to map
        "user": "gaicuser",                 // Username for mapping the drive
        "password": ""                       // Password for mapping the drive (if required)
    }
}
```

## Usage
To run the backup script, execute the following batch file:

```bash
postgres_schema_backup.bat
```

This will:

1. Change the directory to where the script is located.
2. Execute the postgres_schema_backup.py script.

## Logging
The script logs its operations to a file named backup_script.log located in the current working directory. This log file contains information about the success or failure of the backup process.

## Error Handling
The script includes error handling for various scenarios, including:

- Issues with the pg_dump process.
- Missing configuration keys.
- Errors reading the configuration file.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
PostgreSQL for providing the database management system.
Python for the scripting capabilities.
