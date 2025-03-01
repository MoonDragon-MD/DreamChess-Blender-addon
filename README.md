# DreamChess-Blender-addon
Addon for Blender that allows you to export DCM for [DreamChess](https://github.com/dreamchess/dreamchess) Game

### Description:

First of all, I will explain why it does not work optimally:

1) When it was created a very old version of Blender was used (I estimate it to be version 2.3)

2) “mesh.tessfaces” and “face.vertices” were used.

3) Differences between Blender 2.3 and modern Blender:

Here is how the two systems handle mesh data:

Blender 2.3 (old):

Used mesh.tessfaces to get the triangulated mesh faces.

For each face, face.vertices returned the vertex indices (in order).

UV coordinates were accessible via face.uv, a list of tuples (x, y) for each face vertex, in the same order as the vertices.


Modern Blender (post-2.80):

mesh.tessfaces has been removed; mesh.polygons is now used on a triangulated mesh.

poly.vertices returns the indices of the vertices of a polygon.

UVs are obtained via uv_layer.data[loop_index].uv, where loop_index comes from poly.loop_indices, respecting the order of the loops in the mesh.


The main difference is in the way vertices and uv are associated. 

In the old system, the order was implicit and direct (face.vertices and face.uv were aligned). 

In the modern system, the data are organized in “loops,” which connect vertices, UVs, and normals in a specific order. 

If the script does not respect this order, the resulting DCM file will have triangles with mismatched UVs or indices, causing distortions.

Here is a screenshot of the game, the pawn on Blender is a cube now is this strange figure

![alt text](https://github.com/MoonDragon-MD/DreamChess-Blender-addon/blob/main/img.jpg?raw=true)

*Could you help me to make it work?*

### Installation

[Download the add-on](https://github.com/MoonDragon-MD/DreamChess-Blender-addon/releases/tag/V1) 

Install it in Blender (tested on version 2.82 and 2.83.20)

Go to the folder

/home/USER/.config/blender/2.82/scripts/addons/io_dreamchess_exporter

(Change according to your user and version of blender)

and give the per execution to the dcmstrip file

Note: only on Gnu/Linux

### Manual installation

Downloading the sources

inside the "project" folder you will find the instructions in the file “instructions.txt”

NB: The "dcmstrip.cpp" file comes from [here](https://github.com/dreamchess/dreamchess-tools/blob/master/src/dcmstrip.cpp) 

Those who would like to see the old version of the addon here it is: [dcm_export.py](https://github.com/dreamchess/dreamchess-tools/blob/master/src/dcm_export.py) 
