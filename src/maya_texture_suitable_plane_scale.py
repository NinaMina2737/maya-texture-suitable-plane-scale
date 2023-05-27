#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import maya.cmds as cmds
import traceback


def check_size():
    """Check the size of the selected objects and the size of the texture maps"""
    # Get the selected objects
    objects = cmds.ls(selection=True, long=True)
    # Check if there is any object selected
    if not objects:
        cmds.warning("Nothing selected.")
        return
    # Get the shapes of the selected objects
    shapes = cmds.listRelatives(objects, shapes=True)
    # Check if there is any shape
    if not shapes:
        cmds.warning("No shape found.")
        return
    # Get the shading groups of the shapes
    shading_groups = cmds.listConnections(shapes, source=False, destination=True, type="shadingEngine")
    # Check if there is any shading group
    if not shading_groups:
        cmds.warning("No shading group found.")
        return
    # Get the materials of the shading groups
    source_nodes = cmds.listConnections(shading_groups, source=True, destination=False)
    if not source_nodes:
        cmds.warning("No source node found.")
        return
    materials = cmds.ls(source_nodes, materials=True)
    if not materials:
        cmds.warning("No material found.")
        return
    # Create a list of material attributes to check for texture maps
    material_attributes = []
    for material in materials:
        # Check if the material is a lambert, phong or blinn
        if any(material_type in material for material_type in ["lambert", "phong", "blinn"]):
            material_attributes.append(material + ".color")
        else:
            material_attributes.append(material + ".baseColor")
    # Create a list of file names for each material attribute
    file_names = []
    for attribute in material_attributes:
        source_nodes = cmds.listConnections(attribute, source=True, destination=False)
        if source_nodes:
            file_ = cmds.ls(source_nodes, type="file")
            if file_:
                if len(file_) > 2:
                    cmds.warning("More than one file node connected to %s" % attribute)
                    file_names.append(None)
                elif len(file_) == 0:
                    cmds.warning("No file node connected to %s" % attribute)
                    file_names.append(None)
                else:
                    file_names.append(file_[0])
            else:
                file_names.append(None)
        else:
            file_names.append(None)
    # Get the size of each texture map
    file_sizes = []
    for file_name in file_names:
        if file_name:
            file_sizes.append((cmds.getAttr(file_name + ".outSizeX"), cmds.getAttr(file_name + ".outSizeY")))
        else:
            file_sizes.append(None)

    # Get the size of each selected object
    object_sizes = []
    for object_, file_name in zip(objects, file_names):
        if file_name:
            bounding_box = cmds.exactWorldBoundingBox(object_)
            width = abs(bounding_box[3] - bounding_box[0])
            height = abs(bounding_box[5] - bounding_box[2])
            object_sizes.append((width, height))
        else:
            object_sizes.append(None)

    return objects, object_sizes, file_sizes

def match_size(objects, object_sizes, file_sizes, ratio=0.01):
    """Match the size of the selected objects to the size of the texture maps"""
    for object_, object_size, file_size in zip(objects, object_sizes, file_sizes):
        if file_size:
            cmds.scale(file_size[0] / object_size[0] * ratio, file_size[1] / object_size[1] * ratio, object_, relative=True, xz=True)

def execute():
    try:
        # Open an undo chunk
        cmds.undoInfo(openChunk=True)
        # Execute the script
        objects, object_sizes, file_sizes = check_size()
        match_size(objects, object_sizes, file_sizes)
    except Exception as e:
        # Print the error message
        cmds.warning("An error occurred: {}".format(str(e)))
        # Print the traceback
        cmds.warning(traceback.format_exc())
    finally:
        # Close the undo chunk
        cmds.undoInfo(closeChunk=True)

if __name__ == "__main__":
    # Execute the script
    execute()
