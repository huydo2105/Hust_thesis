#!/bin/bash

# Parse command line arguments
while getopts "f:r:" opt
do
  case $opt in
    f) yaml_file=$OPTARG;;
    r) requirement=$OPTARG;;
  esac
done

# Check if yaml file exists
if [ ! -f "$yaml_file" ]; then
  echo "YAML file not found: $yaml_file"
  exit 1
fi

# Add requirement field to YAML file
yq w -i "$yaml_file" 'requirement' "$requirement"

echo "Requirement field added to $yaml_file with value $requirement"
