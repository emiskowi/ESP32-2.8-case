"""Validate the saved Blender project and its binary STL exports.

Run with the same Blender Python used for generation, e.g.:
  uv run --python 3.13 --with bpy python tools/validate_project.py
"""
import os
import struct
import sys
from collections import Counter
import bpy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = os.path.join(ROOT, "model")
BLEND = os.path.join(MODEL, "ESP32_CYD_2000mAh_Case.blend")
STL_NAMES = [
    "ESP32_CYD_front_bezel.stl",
    "ESP32_CYD_battery_tray.stl",
    "ESP32_CYD_battery_lid.stl",
]

bpy.ops.wm.open_mainfile(filepath=BLEND)
print("Blender:", bpy.app.version_string)
print("Project:", BLEND)

failed = False
for obj in bpy.context.scene.objects:
    if obj.type != "MESH" or obj.name.startswith("DISPLAY MOCKUP"):
        continue
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.to_mesh()
    edge_uses = Counter()
    for polygon in mesh.polygons:
        vertices = list(polygon.vertices)
        for index, first in enumerate(vertices):
            second = vertices[(index + 1) % len(vertices)]
            edge_uses[tuple(sorted((first, second)))] += 1
    non_manifold_edges = sum(1 for count in edge_uses.values() if count != 2)
    dims = tuple(round(value, 2) for value in obj.dimensions)
    print("Mesh:", obj.name, "dimensions mm:", dims,
          "verts:", len(mesh.vertices), "faces:", len(mesh.polygons),
          "non-manifold edges:", non_manifold_edges)
    if not mesh.polygons or non_manifold_edges:
        failed = True
    evaluated.to_mesh_clear()

for name in STL_NAMES:
    path = os.path.join(MODEL, name)
    if not os.path.isfile(path):
        print("MISSING STL:", path)
        failed = True
        continue
    with open(path, "rb") as stream:
        data = stream.read()
    if len(data) < 84:
        print("INVALID STL (too short):", name)
        failed = True
        continue
    triangles = struct.unpack("<I", data[80:84])[0]
    expected_size = 84 + triangles * 50
    if triangles == 0 or len(data) != expected_size:
        print("INVALID STL size/count:", name, "bytes:", len(data),
              "triangles:", triangles, "expected bytes:", expected_size)
        failed = True
        continue
    coords = []
    offset = 84
    for _ in range(triangles):
        # Skip the 12-byte normal, then read the 3 vertices (9 floats).
        values = struct.unpack_from("<9f", data, offset + 12)
        coords.extend((values[0:3], values[3:6], values[6:9]))
        offset += 50
    mins = tuple(round(min(p[i] for p in coords), 2) for i in range(3))
    maxs = tuple(round(max(p[i] for p in coords), 2) for i in range(3))
    print("STL:", name, "bytes:", len(data), "triangles:", triangles,
          "bounds:", mins, "to", maxs)

if failed:
    sys.exit("Validation failed; inspect Blender meshes and STL exports.")
print("Basic file, triangle-count, bounds, and Blender edge checks passed.")
