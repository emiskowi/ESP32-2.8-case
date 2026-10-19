"""Parametric Blender model for an ELEGOO CYD ESP32 2.8-inch display case.

Run with Blender's bundled Python, or from Blender: open this file in the
Scripting workspace and press Run Script. It builds the assembly, saves a .blend
project, and exports separate STL parts beside this script.

Important fit note: the linked YELUFT battery listing identifies a 3.7 V
2000 mAh LiPo, but does not provide verifiable cell dimensions. The battery
pocket is therefore an adjustable nominal bay (72 x 44 x 10.5 mm), not a
verified fit. Adjust BATTERY_BAY_* after measuring the pack including its
protection board and cable exit.
"""
import bpy
import math
import os
from mathutils import Vector

# ---------------------- User-editable dimensions (mm) ----------------------
CASE_W = 98.0
CASE_H = 62.0
FRONT_DEPTH = 14.0
TRAY_DEPTH = 12.3
LID_DEPTH = 2.0
BOARD_W = 86.0
BOARD_H = 50.0
BOARD_CLEARANCE = 0.5
SCREEN_WINDOW_W = 58.8
SCREEN_WINDOW_H = 44.0
BATTERY_BAY_W = 72.0
BATTERY_BAY_H = 44.0
BATTERY_BAY_DEPTH = 10.5
USB_SLOT_W = 12.0
USB_SLOT_H = 6.0
SD_SLOT_LEN = 18.0
SD_SLOT_H = 3.5
SCREW_CLEARANCE_D = 3.2
FRONT_SCREW_PILOT_D = 2.6

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
BLEND_PATH = os.path.join(OUT_DIR, "ESP32_CYD_2000mAh_Case.blend")

# Case thickness axis is Z: screen/front is z=0, rear lid is at max Z.
FRONT_Z0 = 0.0
FRONT_Z1 = FRONT_DEPTH
TRAY_Z0 = FRONT_Z1
TRAY_Z1 = TRAY_Z0 + TRAY_DEPTH
LID_Z0 = TRAY_Z1
LID_Z1 = LID_Z0 + LID_DEPTH
BOARD_CAVITY_W = BOARD_W + 2.0 * BOARD_CLEARANCE
BOARD_CAVITY_H = BOARD_H + 2.0 * BOARD_CLEARANCE
SCREW_X = CASE_W / 2.0 - 4.0
SCREW_Y = CASE_H / 2.0 - 4.0
SCREW_POINTS = [(sx * SCREW_X, sy * SCREW_Y) for sx in (-1, 1) for sy in (-1, 1)]

# ------------------------------- Utilities --------------------------------
def deselect_all():
    bpy.ops.object.select_all(action="DESELECT")


def make_cube(name, dims, loc):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def make_cylinder(name, radius, depth, loc, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    return obj


def rounded_box(name, dims, loc, bevel=1.5):
    obj = make_cube(name, dims, loc)
    if bevel > 0:
        mod = obj.modifiers.new("Soft outside corners", "BEVEL")
        mod.width = bevel
        mod.segments = 4
        mod.limit_method = "ANGLE"
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return obj


def boolean_apply(target, cutter, operation="DIFFERENCE"):
    bpy.context.view_layer.objects.active = target
    mod = target.modifiers.new("CAD boolean", "BOOLEAN")
    mod.operation = operation
    mod.solver = "EXACT"
    mod.object = cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def cut_box(target, name, dims, loc):
    cutter = make_cube(name, dims, loc)
    boolean_apply(target, cutter, "DIFFERENCE")


def cut_cylinder(target, name, radius, depth, loc):
    cutter = make_cylinder(name, radius, depth, loc)
    boolean_apply(target, cutter, "DIFFERENCE")


def add_bevel(obj, width=0.35):
    mod = obj.modifiers.new("Print-safe edge easing", "BEVEL")
    mod.width = width
    mod.segments = 2
    mod.limit_method = "ANGLE"
    mod.angle_limit = math.radians(35)
    mod2 = obj.modifiers.new("Weighted corner normals", "WEIGHTED_NORMAL")
    mod2.keep_sharp = True


def set_material(obj, name, color, roughness=0.4):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.roughness = roughness
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def apply_modifiers(obj):
    bpy.context.view_layer.objects.active = obj
    for modifier in list(obj.modifiers):
        bpy.ops.object.modifier_apply(modifier=modifier.name)

# ------------------------------- Build ------------------------------------
# Clear the default scene.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# Front bezel: open-back tray that retains the display board behind the fascia.
front = rounded_box("01 Front bezel and board cradle",
                    (CASE_W, CASE_H, FRONT_DEPTH),
                    (0, 0, FRONT_DEPTH / 2.0), bevel=2.0)
# Board cavity is open at the rear, leaving a 2.2 mm front fascia.
front_plate = 2.2
cut_box(front, "Board pocket cutter",
        (BOARD_CAVITY_W, BOARD_CAVITY_H, FRONT_DEPTH - front_plate + 0.25),
        (0, 0, (FRONT_DEPTH + front_plate) / 2.0))
# Display opening through the front fascia.
cut_box(front, "Display window cutter",
        (SCREEN_WINDOW_W, SCREEN_WINDOW_H, front_plate + 1.0),
        (0, 0, front_plate / 2.0))
# Four small internal ledges carry the PCB at its corners (board sits screen-side forward).
for i, (sx, sy) in enumerate(SCREW_POINTS):
    # Ledge positions track just inside the board's four corners.
    px = sx * (BOARD_W / 2.0 - 2.5) / SCREW_X
    py = sy * (BOARD_H / 2.0 - 2.2) / SCREW_Y
    pad = make_cube("PCB support ledge %02d" % (i + 1), (5.0, 4.4, 1.2),
                    (px, py, 4.4))
    # Fuse each ledge into the bezel so the exported mesh is a single solid.
    boolean_apply(front, pad, "UNION")
    front.name = "01 Front bezel and board cradle"
# USB-C access on the lower short edge and a microSD access slot on the right side.
cut_box(front, "USB-C side opening cutter",
        (USB_SLOT_W, 5.0, USB_SLOT_H),
        (0, -CASE_H / 2.0, 8.0))
cut_box(front, "microSD side opening cutter",
        (5.0, SD_SLOT_LEN, SD_SLOT_H),
        (CASE_W / 2.0, 0, 8.4))
# Clearance channels through the front section for M3 screws (self-tapping into plastic).
for i, (x, y) in enumerate(SCREW_POINTS):
    cut_cylinder(front, "Front screw pilot %02d" % i,
                 FRONT_SCREW_PILOT_D / 2.0, FRONT_DEPTH - front_plate + 0.2,
                 (x, y, (FRONT_DEPTH + front_plate) / 2.0))
add_bevel(front, 0.25)

# Battery tray/bulkhead: solid front separator, adjustable rear-facing battery pocket.
tray = rounded_box("02 Battery tray and separator",
                   (CASE_W - 2.0, CASE_H - 2.0, TRAY_DEPTH),
                   (0, 0, TRAY_Z0 + TRAY_DEPTH / 2.0), bevel=1.2)
separator = 1.8
bay_depth = min(BATTERY_BAY_DEPTH, TRAY_DEPTH - separator)
# Pocket opens from the rear; leave a 1.8 mm separator at the front.
cut_box(tray, "Battery pocket cutter",
        (BATTERY_BAY_W, BATTERY_BAY_H, bay_depth + 0.8),
        (0, 0, TRAY_Z0 + separator + (bay_depth + 0.8) / 2.0))
# Cable notch through the separator, near the lower edge. Route/size can be edited if needed.
cut_box(tray, "Battery lead pass-through",
        (6.0, 3.2, separator + 1.0),
        (0, -BATTERY_BAY_H / 2.0 + 2.0, TRAY_Z0 + separator / 2.0))
# Align screw bores through the tray.
for i, (x, y) in enumerate(SCREW_POINTS):
    cut_cylinder(tray, "Tray screw bore %02d" % i,
                 SCREW_CLEARANCE_D / 2.0, TRAY_DEPTH + 1.0,
                 (x, y, TRAY_Z0 + TRAY_DEPTH / 2.0))
# Continue the USB edge opening into the tray wall so the connector remains accessible.
cut_box(tray, "USB-C continuation cutter",
        (USB_SLOT_W, 4.0, USB_SLOT_H),
        (0, -(CASE_H - 2.0) / 2.0, TRAY_Z0 + 2.0))
add_bevel(tray, 0.25)

# Rear lid, with a shallow locating tongue and through holes.
lid = rounded_box("03 Removable battery lid",
                  (CASE_W - 2.0, CASE_H - 2.0, LID_DEPTH),
                  (0, 0, LID_Z0 + LID_DEPTH / 2.0), bevel=1.0)
for i, (x, y) in enumerate(SCREW_POINTS):
    cut_cylinder(lid, "Lid screw bore %02d" % i,
                 SCREW_CLEARANCE_D / 2.0, LID_DEPTH + 1.0,
                 (x, y, LID_Z0 + LID_DEPTH / 2.0))
add_bevel(lid, 0.2)

# Presentation materials and object metadata.
set_material(front, "Warm light-grey polymer", (0.76, 0.79, 0.82))
set_material(tray, "Deep slate polymer", (0.22, 0.27, 0.31))
set_material(lid, "Deep slate polymer", (0.30, 0.35, 0.39))
# Non-printable display surface makes the front aperture easy to see in Blender.
screen_preview = make_cube("DISPLAY MOCKUP - not a printable part",
                           (57.6, 43.2, 0.15), (0, 0, 2.18))
set_material(screen_preview, "Display glass preview", (0.025, 0.20, 0.31), 0.18)
front["part"] = "Front bezel and PCB cradle"
front["board_fit_mm"] = "86 x 50 board; pocket has 0.5 mm clearance per side"
tray["part"] = "Battery tray; rear opening"
tray["battery_bay_mm"] = "%g x %g x %g (nominal; confirm physical battery size)" % (BATTERY_BAY_W, BATTERY_BAY_H, bay_depth)
lid["part"] = "Removable battery lid"

# Scene settings: mm-scale geometry, organized collection, useful camera view.
scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 0.001  # Blender unit corresponds to one millimetre.
scene.unit_settings.length_unit = "MILLIMETERS"

# Add a simple camera and lights for an immediately inspectable project file.
def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()

bpy.ops.object.camera_add(location=(145, -170, -135))
cam = bpy.context.object
cam.name = "Case overview camera"
point_at(cam, (0, 0, 14))
cam.data.type = "ORTHO"
cam.data.ortho_scale = 190
scene.camera = cam

for name, location, power, size in [
    ("Key softbox", (40, -90, 130), 12000, 90),
    ("Fill softbox", (-100, -5, 80), 8000, 75),
    ("Rim softbox", (15, 100, 100), 10000, 70),
]:
    bpy.ops.object.light_add(type="AREA", location=location)
    light = bpy.context.object
    light.name = name
    light.data.energy = power
    light.data.shape = "DISK"
    light.data.size = size
    point_at(light, (0, 0, 13))

scene.render.engine = "CYCLES"
scene.cycles.samples = 32
scene.render.resolution_x = 1200
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.join(OUT_DIR, "ESP32_CYD_Case_preview.png")
scene.view_settings.view_transform = "AgX"
scene.world.color = (0.035, 0.045, 0.06)

# Select only the printable parts for STL export and save native Blender project.
for obj in bpy.context.scene.objects:
    obj.select_set(False)
for obj in (front, tray, lid):
    obj.select_set(True)
bpy.context.view_layer.objects.active = front

# Save native .blend file.
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)

# Export each physical part as a separate STL (evaluates bevel modifiers).
for obj, filename in [
    (front, "ESP32_CYD_front_bezel.stl"),
    (tray, "ESP32_CYD_battery_tray.stl"),
    (lid, "ESP32_CYD_battery_lid.stl"),
]:
    deselect_all()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.stl_export(filepath=os.path.join(OUT_DIR, filename), export_selected_objects=True)

# Restore the assembly selection and save after export.
deselect_all()
for obj in (front, tray, lid):
    obj.select_set(True)
bpy.context.view_layer.objects.active = front
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
bpy.ops.render.render(write_still=True)
print("Created Blender project:", BLEND_PATH)
print("Exported front bezel, battery tray, and lid STL parts.")
print("Nominal battery bay (mm): %.1f x %.1f x %.1f; confirm actual battery dimensions before printing." % (BATTERY_BAY_W, BATTERY_BAY_H, bay_depth))
