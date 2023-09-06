# BeamNG-Modding-Tools
        This is a tool that generates main.materials.json files for BeamNG.drive.
        This version;
            *Only handles level content, files; ".dae" and ".dds". 
            *Sets the "name", "mapTo" and "colorMap" 
            *Is only useful for batch processing material slots.
            *Uses gui exclusively          
            
        Usage:
        1. Format your texture or material names. They should match or atleast be simular.
            *The script will attempt to match the name of your materials with the name of your texture files.
            *Direct matches will result in faster generation times.
            *Non direct matches will use difflib. For example, "wood" and "wood_wall". 
            *If the names are not simular, they will be excluded from the .json.
            *Characters after "." in the texture names will be ignored.
            
        2. Format your folder structure so that all texture files are within the subfolders of your directory. For example,
           Your root directory: C:/Users/"name"/AppData/Local/BeamNG.drive/"version"/mods/unpacked/"mod"/levels/"mapname"/art/shapes
           The folder containg your textures .../shapes/materials/wood/wood.color.dds
           The folder containg your main.materials.json .../shapes
           The script will find any colladas within the root and subfolders
             *Your directory must contain; levels subpath, at least 1 collada and 1 texture for the process to attempt matching.
             
        3. Enter the root directory.
            *Warning, this script will overwrite any existing main.material.json in the directory. Make backups before proceeding. 
            
        4. Click the "Process" button to generate the JSON file.
        
        5. Done. You can now analyse your results. 
           *If any materials are with no matches. A list will be available in a window.  

        Author: Camubish
