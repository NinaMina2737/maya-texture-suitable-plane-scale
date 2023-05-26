#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals
import maya.cmds as cmds
import traceback


def check_size():
    objects = cmds.ls(selection=True, long=True)
    shapes = cmds.listRelatives(objects, shapes=True)
    shading_groups = cmds.listConnections(shapes, source=False, destination=True, type="shadingEngine")
    source_nodes = cmds.listConnections(shading_groups, source=True, destination=False)
    materials = cmds.ls(source_nodes, materials=True)
    if not materials:
        cmds.warning("No material found.")
        return
    material_attributes = []
    for material in materials:
        if any(material_type in material for material_type in ["lambert", "phong", "blinn"]):
            material_attributes.append(material + ".color")
        else:
            material_attributes.append(material + ".baseColor")
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
    file_sizes = []
    for file_name in file_names:
        if file_name:
            file_sizes.append((cmds.getAttr(file_name + ".outSizeX"), cmds.getAttr(file_name + ".outSizeY")))
        else:
            file_sizes.append(None)

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
    cmds.undoInfo(openChunk=True)
    for object_, object_size, file_size in zip(objects, object_sizes, file_sizes):
        if file_size:
            cmds.scale(file_size[0] / object_size[0] * ratio, file_size[1] / object_size[1] * ratio, object_, relative=True, xz=True)
    cmds.undoInfo(closeChunk=True)


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
