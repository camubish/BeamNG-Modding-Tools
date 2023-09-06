
import os
import tkinter as tk 
import difflib
import re
import json
from tkinter import filedialog, ttk
from tqdm import tqdm
from collada import Collada
import sys
import webbrowser
import time

def restart_script():
    python = sys.executable
    os.execl(python, python, *sys.argv)

    
if __name__ == "__main__":
    
    Version = 1.2
    def open_about_window():
        about_text = '''
        Version = {Version}
        This is a tool that generates main.materials.json files for BeamNG.drive.
        This version;
            *Lacks features like; Settings
            *Handles files; ".dae", ".dds" and ".png". 
            *Sets the "name", "mapTo" and "colorMap" 
            *Is only usefull for batch processing material slots.             
            
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
             
        3. Choose you content type to set the keyword using the radio buttons.
             
        4. Enter the root directory.
            *Warning, this script will overwrite any existing main.material.json in the directory. Make backups before proceeding. 
            
        5. Click the "Process" button to generate the JSON file.
        
        6. Done. You can now analyse your results. 
           *If any materials are with no matches. A list will be available in a window.  

        Author: Camubish
        
        '''        
            
        about_window = tk.Toplevel(main_window)
        about_window.title("About")

        about_label = tk.Label(about_window, text=about_text, justify=tk.LEFT)
        about_label.pack(padx=10, pady=10)

        close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
        close_button.pack()
    
    def update_keyword():
        global Keyword
        Keyword = keyword_var.get()
        print(f"Selected Keyword: {Keyword}")


    def check_output_file_exists(event=None):
        root_directory = root_dir_entry.get()
        output_file_path = os.path.join(root_directory, output_file)
        
        if os.path.isfile(output_file_path):
            # File exists, show a label
            output_file_label.config(text=f"Warning: Existing {output_file} in the root directory")
            output_file_label.place(x=5, y=25)  # Show the label and set its position
        else:
            # File doesn't exist, hide the label
            output_file_label.place_forget()

    def update_window_height(event=None):
        # Calculate the required height based on the widgets placed using .pack()
        pack_height = main_frame.winfo_reqheight()

        # Calculate the required height based on the widgets placed using .place()
        max_place_bottom = 0
        for widget in main_frame.place_slaves():
            widget_bottom = widget.winfo_y() + widget.winfo_height()
            if widget_bottom > max_place_bottom:
                max_place_bottom = widget_bottom

        # Calculate the maximum height required for both .pack() and .place() widgets
        new_height = max(pack_height, max_place_bottom)

        main_window.geometry(f"{window_width}x{new_height}")
    def close_windows():
        main_window.destroy()
        unmatched_window.destroy()
        about_window.destroy()
    # Get the directory where the script is located
    script_directory = os.path.dirname(__file__)

    # File path to store the last used root directory
    last_directory_file = os.path.join(script_directory, "last_directory.json")

    root_directory = ""
    #
    output_file = "main.materials.json"
    #
    collada = None  # Define the collada object at a higher scope
    progress_bar = None  # Add this line
    progress_label = None  # Add this line
    # Create the complete output file path in the root directory
    json_output_path = os.path.join(root_directory, output_file)

    def save_last_directory(directory):
        with open(last_directory_file, "w") as file:
            json.dump({"last_directory": directory}, file)

    def load_last_directory():
        if os.path.isfile(last_directory_file):
            with open(last_directory_file, 'r') as file:
                try:
                    data = json.load(file)
                    return data.get('last_directory', '')
                except json.JSONDecodeError:
                    print("Error: Invalid JSON data in last_directory.json")
        else:
            # Create the JSON file with an empty directory if it doesn't exist
            save_last_directory('')
            return ''

    def gather_texture_file_names(root_dir):
        texture_file_names = []
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".dds") or file.endswith(".png"):
                    texture_file_names.append(os.path.join(root, file))
        return texture_file_names
        
    



    def display_unmatched_materials(unmatched_materials):
        # Create a new tkinter window
        unmatched_window = tk.Tk()
        unmatched_window.title("Unmatched Materials")
        
        # Create a label to display the unmatched materials
        label = tk.Label(unmatched_window, text="Unmatched Materials:")
        label.pack()
        
        # Create a text widget to display the list of unmatched materials
        text_widget = tk.Text(unmatched_window, wrap=tk.WORD, width=50)
        text_widget.pack()
        
        # Insert each unmatched material into the text widget
        for material in unmatched_materials:
            text_widget.insert(tk.END, material + "\n")
        
        # Calculate the number of lines in the list
        num_lines = len(unmatched_materials)
        
        # Calculate the height of the text widget based on the number of lines
        text_widget_height = min(20, num_lines)  # Limit the height to a maximum of 20 lines
        
        # Set the height of the text widget
        text_widget.config(height=text_widget_height)
        
        # Create a button to close the window
        close_button = tk.Button(unmatched_window, text="Close", command=unmatched_window.destroy)
        close_button.pack()
        
        unmatched_window.mainloop()


    def get_close_matches(text, words):
        # Split the text by "/" and take the last part
        last_prefix = text.split("/")[-1]

        # Split each word in the list by "/" and take the last part
        last_prefix_words = [word.split("/")[-1] for word in words]

        # Use difflib's get_close_matches on the last prefixes
        return difflib.get_close_matches(last_prefix, last_prefix_words, n=3)
        

    def browse_and_set_directory(entry_widget):
        initial_directory = entry_widget.get()
        directory = filedialog.askdirectory(initialdir=initial_directory)
        if directory:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, directory)
            save_last_directory(directory) 
    
    def clear_root_dir_entry():
        root_dir_entry.delete(0, tk.END)
    
    

    
    def write_json(material_texture_dict, unmatched_materials, total_materials, start_time):
        global progress_bar
        global main_window
        global main_frame
        # Create the complete output file path in the root directory
        json_output_path = os.path.join(root_directory, output_file)
        texture_file_names = gather_texture_file_names(root_directory)
        with open(json_output_path, "w") as output:
            output.write("{")
            counter = 0
            for material_name, texture_name in material_texture_dict.items():
                texture_name_with_extension = None
                folder_name = None

                for texture_path in texture_file_names:
                    if texture_name in os.path.basename(texture_path):
                        texture_name_with_extension = os.path.basename(texture_path)
                        folder_name = os.path.dirname(texture_path)
                        break

                if texture_name_with_extension:
                    index = folder_name.find(Keyword)
                    if index != -1:
                        folder_name = folder_name[index:].replace("\\", "/")
                        output.write(f'\n   "{material_name}": {{')
                        output.write(f'\n     "name": "{material_name}",')
                        output.write(f'\n     "mapTo": "{material_name}",')
                        output.write(f'\n     "class": "Material",')
                        output.write(f'\n     "Stages": [')
                        output.write(f'\n       {{"colorMap": "/{folder_name}/{texture_name_with_extension}"}},')
                        output.write(f'\n       {{}},')
                        output.write(f'\n       {{}},')
                        output.write(f'\n       {{}}')
                        output.write(f'\n     ],')
                        output.write(f'\n     "alphaRef": 69,')
                        output.write(f'\n     "alphaTest": true,')
                        output.write(f'\n     "doubleSided": true,')
                        output.write(f'\n     "translucentBlendOp": "None"')
                        output.write('\n   },')
                    #print(f"    {material_name} added to json")
                    counter += 1
                    progress_bar["value"] = counter
                    progress_label.config(text=f"Writing JSON: {counter}/{total_materials} materials processed")
                    progress_label.update_idletasks()
            output.write("\n}")
            progress_label.config(text=f"Done. {counter} materials mapped to JSON")
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"---Done in {elapsed_time} seconds---")
            elapsed_time_label = tk.Label(main_frame, text=f"Elapsed Time: {elapsed_time:.2f} seconds")
            elapsed_time_label.pack()
            restart_button = tk.Button(main_frame, text="Next", command=restart_script, width=12 )
            restart_button.pack()
            close_button = tk.Button(main_frame, text="Done", command=close_windows, width=12 )
            close_button.pack()
            progress_bar.pack_forget()
            main_window.update_idletasks()
        if unmatched_materials:
            View_button = tk.Button(main_frame, text="View Unmatched", command=lambda: display_unmatched_materials(unmatched_materials), width=12)
            View_button.pack()
            main_window.update_idletasks()
        update_window_height(None)
        main_window.update()
    #


    last_used_directory = load_last_directory()
    main_window = tk.Tk()
    main_frame = tk.Frame(main_window)
    keyword_var = tk.StringVar()
    main_window.title("BeamNG main.material.json Generator")
    window_width = 320
    window_height = 170
    main_window.geometry(f"{window_width}x{window_height}")



    progress_bar = ttk.Progressbar(main_frame, mode='determinate', length=250)
    result_label = tk.Label(main_frame, text="")
    progress_label = tk.Label(main_frame, text="")
    matched_label = tk.Label(main_frame, text="")
    close_match_label = tk.Label(main_frame, text="")
    warning_label = tk.Label(main_frame, text="")

    def process_files():
        global root_directory
        global progress_bar
        global progress_label
        global root_dir_entry  
        global browse_button  
        global process_button  
        global main_window
        global root_dir_label
        close_match_displayed = False  # Flag to track if close_match_label has been displayed
        no_match_displayed = False 
        # Hide the root entry, browse button, and process button
        root_dir_label.place_forget()
        root_dir_entry.place_forget()
        browse_button.place_forget()
        process_button.place_forget()
        clear_button.place_forget()
        open_explorer_button.place_forget()
        output_file_label.place_forget()
        about_button.place_forget()
        keyword1_radio.place_forget()
        keyword2_radio.place_forget()
        
        progress_bar.pack()
        result_label.pack()
        progress_label.pack()
        matched_label.pack()
        
        start_time = time.time()
        
        main_window.update()
        update_keyword()
        root_directory = root_dir_entry.get()
        print(f"Keyword: {Keyword}")
        
        root_folder_names = []
        root_directory = root_dir_entry.get()
        index = root_directory.find(Keyword)
        
        update_window_height(None)
        main_window.update_idletasks()
        
        if index != -1:
            subpath = root_directory[index:].replace("\\", "/")
            result_label.config(text=f"{subpath}/{output_file}")
            update_window_height(None)
            main_window.update()
        else:
            result_label.config(text=f"{Keyword} not found in the root directory")
            restart_button = tk.Button(main_frame, text="Okay", command=restart_script, width=12 )
            restart_button.pack()
            progress_bar.pack_forget()
            matched_label.pack_forget()
            update_window_height(None)
            main_window.update()
            return
        
        main_window.update()
        # Gather texture file names from root directory and subdirectories
        texture_file_names = gather_texture_file_names(root_directory)
        total_texture_files = len(texture_file_names)
        print(f"Total texture files found: {total_texture_files}")
        
        if total_texture_files > 0:
            matched_label.config(text=f"Total texture files found: {total_texture_files}")  
            update_window_height(None)
            main_window.update()
        else:
            progress_label.config(text=f"No texture files found in the subfolders.")
            restart_button = tk.Button(main_frame, text="Okay", command=restart_script, width=12 )
            restart_button.pack()
            progress_bar.pack_forget()
            matched_label.pack_forget()
            update_window_height(None)
            main_window.update()
            return
        
        # Create the complete output file path in the root directory
        json_output_path = os.path.join(root_directory, output_file)

        
        with open(json_output_path, "w") as output:
            output.write("{")
            counter = 0
            match_count = 0
            no_match = 0
            close_match = 0
            collada_count = 0
            material_texture_dict = {}
            unmatched_materials = []
            
            total_colladas = 0
            for root, _, files in os.walk(root_directory):
                total_colladas += sum(1 for file in files if file.lower().endswith(".dae"))
            print(f"Found: {total_colladas} Collada files in root directory.")
            progress_bar["maximum"] = total_colladas
            progress_bar["value"] = 0
            progress_bar.update()  # Refresh the progress bar
            
            if not total_colladas > 0:
                result_label.config(text=f"No collada files found.")
                restart_button = tk.Button(main_frame, text="Okay", command=restart_script, width=12 )
                restart_button.pack()
                progress_bar.pack_forget()
                matched_label.pack_forget()
                update_window_height(None)
                main_window.update()
                return
        
            
            # Count the number of total materials and collect material names and COLLADA file paths
            unique_material_names = set()
            material_name_to_collada = {}  # Mapping from material name to COLLADA file path
            for root, _, files in os.walk(root_directory):
                for file in files:
                    if file.lower().endswith(".dae"):
                        collada_count += 1
                        collada_file_path = os.path.join(root, file)
                        collada = Collada(collada_file_path)
                        for material in collada.materials:
                            material_name_dirty = material.name
                            material_name, sep, tail = material_name_dirty.partition('-')
                            unique_material_names.add(material_name)
                            material_name_to_collada[material_name] = collada_file_path
                            counter += 1
                            progress_label.config(text=f"Found:{total_colladas} Colladas. Finding materials...{counter}")
                            progress_bar["value"] = collada_count
                            main_window.update_idletasks()
            
            total_materials = len(unique_material_names)
            print(f"Found: {total_materials} Materials slots in colladas.")
            # Create a progress bar
            progress_bar["maximum"] = total_materials
            progress_bar["value"] = 0
            progress_bar.update()  # Refresh the progress bar

            # Reset the progress labels
            progress_label.config(text=f"Matching: 0/{total_materials} materials processed")

            # Set to keep track of processed material names
            processed_materials = set()
            
            # Iterate through the unique material names and process materials
            for material_name in unique_material_names:
                if material_name not in processed_materials:
                    #print(f"Processing material: {material_name}")  # Debugging line
                    matching_texture = None
                    last_prefix = material_name.split("/")[-1]

                    for texture_name in texture_file_names:
                        texture_name_clean = os.path.basename(texture_name).split(".", 1)[0]
                        if last_prefix in texture_name_clean:
                            matching_texture = texture_name_clean
                            match_count += 1
                            break

                    if matching_texture:
                        material_texture_dict[material_name] = matching_texture
                    else:
                        close_matches = get_close_matches(material_name, [os.path.basename(file_path).split('.')[0] for file_path in texture_file_names])
                        print(f"  No matching texture found, close matches: {close_matches}")

                    if not matching_texture:
                        close_matches = get_close_matches(material_name, [os.path.basename(file_path).split('.')[0] for file_path in texture_file_names])
                        if close_matches:
                            close_match += 1
                            matching_texture = close_matches[0]
                            material_texture_dict[material_name] = matching_texture
                            print(f"  Using closest match: {matching_texture}")
                        else:
                            no_match += 1
                            unmatched_materials.append(material_name)  # Add unmatched material to the list
                            print(f"  No matching texture found")

                    # Add the processed material name to the set
                    processed_materials.add(material_name)
                
                    progress_bar["value"] = len(processed_materials)
                    progress_label.config(text=f"Matching: {len(processed_materials)}/{total_materials} materials processed")
                    matched_label.config(text=f"{match_count} exact name matched.")
                    close_match_label.config(text=f"{close_match} closest named matched.")
                    warning_label.config(text=f"Warning: {no_match} with no matching texture!")
                    main_window.update_idletasks()
                    if close_match > 0 and not close_match_displayed:
                        close_match_displayed = True
                        close_match_label.pack()
                        update_window_height(None)
                        main_window.update()
                    if no_match > 0 and not no_match_displayed:
                        no_match_displayed = True
                        warning_label.pack()    
                        update_window_height(None)
                        main_window.update()
            

    
            progress_label.config(text=f"{counter} materials processed .")
            write_json(material_texture_dict, unmatched_materials, total_materials, start_time)
            update_window_height(None)
            main_window.update()
    def open_in_explorer():
        directory = root_dir_entry.get()  # Get the current directory from the entry field
        if directory:
            try:
                webbrowser.open(directory)
            except Exception as e:
                print(f"Error opening the directory: {str(e)}")
                

    main_frame.pack(fill=tk.BOTH, expand=True)
    
    title_label = tk.Label(main_frame, text=f"BeamNG main.material.json Generator v{Version}", font=("Helvetica", 10, "bold"))
    root_dir_label = tk.Label(main_frame, text="Root Directory:")
    root_dir_entry = tk.Entry(main_frame, width=50)
    root_dir_entry.insert(0, last_used_directory)  # Set the initial value to the last used directory
    browse_button = tk.Button(main_frame, text="Choose Folder", command=lambda: browse_and_set_directory(root_dir_entry),width=12)
    process_button = tk.Button(main_frame, text="Process", command=process_files, width=26)
    clear_button = tk.Button(main_frame, text="Clear", command=clear_root_dir_entry, width=12)
     
    open_explorer_button = tk.Button(main_frame, text="Open in Explorer", command=open_in_explorer, width=12)
    output_file_label = tk.Label(main_frame, text="")
    
    keyword1_radio = tk.Radiobutton(main_frame, text="Levels", variable=keyword_var, value="levels", command=update_keyword)
    keyword2_radio = tk.Radiobutton(main_frame, text="Vehicles", variable=keyword_var, value="vehicles", command=update_keyword)
    keyword_var.set("levels")
    
    about_button = tk.Button(main_frame, text="About", command=open_about_window, width=12)
    about_button.place(x=200, y=102)
    
    keyword1_radio.place(x=100,y=130)
    keyword2_radio.place(x=5,y=130)
    
    output_file_label.place(x=102, y=26)
    title_label.pack(pady=5)
    root_dir_label.place(x=5, y=26)
    root_dir_entry.place(x=5, y=50)
    browse_button.place(x=5, y=75) 
    clear_button.place(x=200, y=75)
    process_button.place(x=5, y=102)
    open_explorer_button.place(x=102, y=75)    

    check_output_file_exists()
    
    root_dir_entry.bind("<KeyRelease>", check_output_file_exists)
    main_frame.bind("<Configure>", update_window_height)
    

    main_window.mainloop()
    
        

