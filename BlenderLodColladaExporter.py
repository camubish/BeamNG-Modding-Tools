import bpy
import bmesh
import random
import time

def enter_edit_mode(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action='DESELECT')

def exit_edit_mode():
    bpy.ops.object.mode_set(mode="OBJECT")

def process_and_export(selected_object):
    
    # Create a list to store objects to delete
    objects_to_delete = []

    # Iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
        # Check if the object shares the same data as the selected object
        if obj.data == selected_object.data and obj != selected_object:
            objects_to_delete.append(obj)

    # Delete the objects in the list
    for obj in objects_to_delete:
        bpy.data.objects.remove(obj)

    # Set the rotation and location of the selected object to (0, 0, 0)
    selected_object.location = (0, 0, 0)
    selected_object.rotation_euler = (0, 0, 0)

    # Create a new collection named after the mesh data name
    mesh_data_name = selected_object.data.name
    collection_name = mesh_data_name.split("/")[-1].split(".")[0]  # Extract the desired name
    new_collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(new_collection)

    # Move the selected object to the new collection
    new_collection.objects.link(selected_object)

    # Create a new empty object (plain axes) in the new collection and name it "base00"
    base00 = bpy.data.objects.new("base00", None)
    new_collection.objects.link(base00)

    # Create a new empty object (plain axes) in the new collection and name it "start01"
    start01 = bpy.data.objects.new("start01", None)
    new_collection.objects.link(start01)

    # Parent "start01" and "bb_autobillboard2" to "base00"
    start01.parent = base00
    bb_autobillboard2 = bpy.data.objects.new("bb_autobillboard2", None)
    new_collection.objects.link(bb_autobillboard2)
    bb_autobillboard2.parent = base00

    # Rename the selected object to "r21_a150" and parent it to "start01"
    selected_object.name = "r21_a150"
    selected_object.parent = start01

    # Create a copy of the renamed object and name it "it r21_a25" and parent it to "start01"
    copy_object = selected_object.copy()
    copy_object.data = selected_object.data.copy()  # Make the data single-user
    copy_object.name = "r21_a25"
    new_collection.objects.link(copy_object)
    copy_object.parent = start01

    # Add a Decimate modifier with a 0.5 collapse ratio to "it r21_a25"
    decimate_modifier = copy_object.modifiers.new("Decimate", 'DECIMATE')
    decimate_modifier.decimate_type = 'COLLAPSE'
    decimate_modifier.ratio = 0.5

    # Apply the Decimate modifier to "it r21_a25"
    bpy.context.view_layer.objects.active = copy_object
    bpy.ops.object.modifier_apply(modifier="Decimate")

    # Create a copy of "it r21_a25" and name it "Colmesh-1" and parent it to "start01"
    colmesh_1 = copy_object.copy()
    colmesh_1.data = copy_object.data.copy()  # Make the data single-user
    colmesh_1.name = "Colmesh-1"
    new_collection.objects.link(colmesh_1)
    colmesh_1.parent = start01


    # Switch to Edit Mode
    enter_edit_mode(selected_object)
    
    # Check if we are in Edit Mode
    if bpy.context.object.mode == 'EDIT':
        # Deselect all vertices
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Get the material index for "rocks_vegetation" material
        material_index = selected_object.data.materials.find("rocks_vegetation")

        # Check if the material index is valid (-1 means the material is not found)
        if material_index != -1:
            # Create a new BMesh to work with
            bm = bmesh.from_edit_mesh(selected_object.data)
            
            # Create a list to store vertices to delete
            vertices_to_delete = []

            # Iterate through vertices and select those connected to faces with the material index
            for vert in bm.verts:
                if any(face.material_index == material_index for face in vert.link_faces):
                    vertices_to_delete.append(vert)

            # Delete the selected vertices in the BMesh
            for vert in vertices_to_delete:
                bm.verts.remove(vert)

            # Update the BMesh and mesh data
            bmesh.update_edit_mesh(selected_object.data)

    exit_edit_mode()
    
    for obj in new_collection.objects:
        obj.select_set(True)

    # Set the collection as the active collection
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[collection_name]

    # Set the export path
    export_path = "D:/Blender/Outlands Map Project/LODMODELPROCESSED/" + collection_name + ".dae"

    # Configure Collada export settings
    bpy.ops.wm.collada_export(filepath=export_path, selected=True)

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    bpy.data.collections.remove(new_collection)
    

collection_name = "Rocks"  # Replace with the actual name of your collection
collection = bpy.data.collections.get(collection_name)

# Loop through objects in the "Rocks" collection
while collection and collection.objects:
    # Get a random object from the collection
    selected_object = random.choice(collection.objects)
    
    # Process and export the selected object
    process_and_export(selected_object)
    
    # Remove the processed object from the collection
    collection.objects.unlink(selected_object)
