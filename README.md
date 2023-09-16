# BeamNG-Modding-Tools
managedItemData.json.py: Creates the json file for your forest meshes using specified directories of your .dae's 

BlenderLodColladaExporter.py: Auto exports all in a collection with LOD's. Put this script in blender edit the script to your needs 

BlenderForestDataExporter.py: Creates a json for every object mesh data type. formats their position and rotation. Names them after the mesh name.

Main Material json generator:
This is a tool that generates main.materials.json files for BeamNG.drive. 

This version:
- Handles files: ".dae", ".dds", and ".png".
- Sets the "name", "mapTo", and "colorMap".
- Is only useful for batch processing material slots.

Usage:
1. Format your texture or material names. They should match or at least be similar.
   - The script will attempt to match the name of your materials with the name of your texture files.
   - Direct matches will result in faster generation times.
   - Non-direct matches will use difflib. For example, "wood" and "wood_wall".
   - If the names are not similar, they will be excluded from the .json.
   - Characters after "." in the texture names will be ignored.

2. Format your folder structure so that all texture files are within the subfolders of your directory. For example:
   - Your root directory: C:/Users/"name"/AppData/Local/BeamNG.drive/"version"/mods/unpacked/"mod"/levels/"mapname"/art/shapes
   - The folder containing your textures .../shapes/materials/wood/wood.color.dds
   - The folder containing your main.materials.json .../shapes
   - The script will find any Colladas within the root and subfolders.
   - Your directory must contain the selected keyword, at least one Collada, and one texture for the process to attempt matching.

3. Choose your content type by setting the keyword using the radio buttons.

4. Enter the root directory.
   - Warning: This script will overwrite any existing main.material.json in the directory. Make backups before proceeding.

5. Click the "Process" button to generate the JSON file.

6. Done. You can now analyze your results.
   - If any materials are without matches, a list will be available in a window.

Author: Camubish

<img width="484" alt="readmepic" src="https://github.com/camubish/BeamNG-Modding-Tools/assets/144230011/ac7a2e52-38db-42c7-a6f2-9b975ee1f600">
