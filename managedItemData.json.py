import os
import json

# Specify the directories to search for Collada files
directories_to_search = [
    "C:\\Users\\acorn\\AppData\\Local\\BeamNG.drive\\0.29\\mods\\unpacked\\CB_HL2Jalopy\\levels\\ridingshotgun\\art\\shapes\\trees",
    "C:\\Users\\acorn\\AppData\\Local\\BeamNG.drive\\0.29\\mods\\unpacked\\CB_HL2Jalopy\\levels\\ridingshotgun\\art\\shapes\\rocks",
    # Add more directories as needed
]

# Create a dictionary to store the JSON data
json_data = {}

# Define the base directory where "levels" starts
base_directory = "C:\\Users\\acorn\\AppData\\Local\\BeamNG.drive\\0.29\\mods\\unpacked\\CB_HL2Jalopy"

# Iterate through the specified directories
for directory in directories_to_search:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".dae"):
                collada_name = os.path.splitext(file)[0]  # Get the name without extension
                collada_path = os.path.relpath(os.path.join(root, file), base_directory)  # Get the relative path from "levels"
                collada_path = collada_path.replace("\\", "/")
                # Create a JSON entry for the Collada file
                json_data[collada_name] = {
                    "name": collada_name,
                    "internalName": collada_name,
                    "class": "TSForestItemData",
                    "persistentId": "01099ef5-bd21-4018-b3b9-24e05bd6cdd0",
                    "__parent": "DataBlockGroup",
                    "shapeFile": collada_path,
                }

# Save the JSON data to a file
with open("managedItemData.json", "w") as json_file:
    json.dump(json_data, json_file, indent=2)

print("JSON file generated successfully.")