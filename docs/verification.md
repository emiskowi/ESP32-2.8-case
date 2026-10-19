# Generation and verification record

## Generation

- Native CAD: Blender `.blend` scene generated with Blender 5.2.2 LTS / `bpy`.
- Generator: `model/esp32_cyd_case_generator.py`.
- Scene parts: front bezel/cradle, battery tray/separator, removable lid, and a non-printable display mockup.
- Exports: separate binary STL for each printable part.

## Checked outputs

The saved `.blend` was reopened successfully in Blender 5.2.2 LTS. The three printable mesh object dimensions in the scene were:

| Object | Dimensions (mm) |
|---|---:|
| Front bezel/cradle | 98 × 62 × 14 |
| Battery tray/separator | 96 × 60 × 12.3 |
| Rear lid | 96 × 60 × 2 |

The Blender meshes had zero edges used by anything other than exactly two faces in the edge-use check. The STL files were confirmed to exist, have valid binary file lengths, contain non-zero triangle counts, and have the following bounds:

| STL | File size | Triangles | Bounding box (mm) |
|---|---:|---:|---|
| `ESP32_CYD_front_bezel.stl` | 174,484 bytes | 3,488 | 98 × 62 × 14 |
| `ESP32_CYD_battery_tray.stl` | 152,084 bytes | 3,040 | 96 × 60 × 12.3 |
| `ESP32_CYD_battery_lid.stl` | 131,084 bytes | 2,620 | 96 × 60 × 2 |

A render was generated and inspected for the front opening and overall assembly. These checks verify file generation, scene dimensions, basic edge-use topology, and exported bounds. They do **not** prove absence of self-intersections, physical fit, dimensional accuracy of the linked hardware, or success on a particular printer. No physical print has been made.

## Known follow-up checks

- Measure and set the battery pocket from the exact LiPo pack, including protection board and leads.
- Verify the exact CYD revision, USB-C and microSD coordinates, board thickness, and acrylic-protector clearance.
- Inspect/repair any intersecting or non-manifold mesh regions if the target slicer reports issues.
- Print a test coupon, then revise clearances based on actual printer/material tolerances.
