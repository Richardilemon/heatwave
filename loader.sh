#!/bin/bash

# Stop Docker containers if they are running
docker-compose down

# Run Docker Compose file
docker-compose up -d

# Execute Python script
python3 /mnt/c/Users/hp/Desktop/projects/DE_PROJ/weather/load.py

# Check the exit code of the Python script
if [ $? -eq 0 ]; then
    # Script executed successfully, stop the Docker containers
    docker-compose down
else
    # Script failed, print an error message
    echo "Error: Python script execution failed"
fi
