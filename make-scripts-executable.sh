#!/bin/bash

# first make this script executable
# chmod +x make-scripts-executable.sh
# then run it 
# ./make-scripts-executable.sh

# Define the directories to be checked
directories=(
    "/scripts/installers"
    # Add more directories as necessary
)

# Iterate over each directory and find .sh files, then set executable permission
for dir in "${directories[@]}"; do
  echo "Processing directory: $dir"
  for file in "$dir"/*.sh; do
    if [ -f "$file" ]; then
      echo "Setting +x on: $file"
      chmod +x "$file"
    fi
  done
done

echo "Script execution completed."