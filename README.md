# BeamNG-Modding-Tools
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
   - Your directory must contain a "levels" subpath, at least one Collada, and one texture for the process to attempt matching.

3. Choose your content type by setting the keyword using the radio buttons.

4. Enter the root directory.
   - Warning: This script will overwrite any existing main.material.json in the directory. Make backups before proceeding.

5. Click the "Process" button to generate the JSON file.

6. Done. You can now analyze your results.
   - If any materials are without matches, a list will be available in a window.

Author: Camubish
