# Design and fit notes

## Scope

This project packages the ESP32 CYD display board and a single LiPo battery in a three-part printed case. It is based on the product links supplied for the ELEGOO 2.8-inch touch display and YELUFT battery. It does not add charging, protection, or power-conversion electronics; the battery's protection is part of the linked battery pack listing.

## Hardware evidence and assumptions

| Item | Listing / known details | Model treatment |
|---|---|---|
| Display board | ELEGOO ESP32 2.8-inch ILI9341 touch display (CYD family). Product specifications identify an approximately 86 × 50 mm module. | Board pocket is 87 × 51 mm, giving 0.5 mm nominal clearance on each side. Confirm the exact board revision, overall thickness, and mechanical drawing. |
| Display area | 2.8-inch, 240 × 320 display; common active-area figure is about 57.6 × 43.2 mm. | Window is 58.8 × 44 mm. Confirm the actual viewable area and the supplied acrylic protector before printing. |
| USB-C / microSD | Board listing indicates USB-C and a microSD/TF interface; exact connector coordinates were not measured from a mechanical drawing. | Lower-edge USB-C and right-side microSD openings are assumptions. Verify the orientation and adjust the generator if your revision differs. |
| Battery | YELUFT listing identifies a 3.7 V, 2000 mAh LiPo with JST 1.25 connector. The listing does not provide a verified physical size in the accessible specifications. | Pocket is currently 72 × 44 × 10.5 mm as a placeholder. This is **not a confirmed fit**. Measure the pack, protection board, wire exit, and connector. |

A capacity value such as 2000 mAh does not determine battery length, width, or thickness. Multiple cells with the same capacity can have different shapes. Do not infer a fit from capacity or connector alone.

## Current CAD dimensions

All dimensions below are in millimeters.

| Parameter | Value | Note |
|---|---:|---|
| Overall case envelope | 98 × 62 × 28.3 | Derived from assembled part depths and largest perimeter |
| Front bezel/cradle | 98 × 62 × 14 | Open at rear for board insertion; 2.2 mm fascia |
| Board cavity | 87 × 51 | 0.5 mm clearance per side around 86 × 50 nominal outline |
| Display window | 58.8 × 44 | Rectangular opening through the fascia |
| Battery tray | 96 × 60 × 12.3 | Includes 1.8 mm separator wall |
| Nominal battery cavity | 72 × 44 × 10.5 | Placeholder dimensions, must be revised from measurement |
| Rear lid | 96 × 60 × 2 | Removable cover |
| USB-C slot | 12 × 6 | Assumed lower-edge location |
| microSD slot | 18 × 3.5 | Assumed right-side location |
| Battery lead pass-through | 6 × 3.2 | Routes the lead through the separator |

## Editable parameters

Open `model/esp32_cyd_case_generator.py` and edit the named millimeter values near the top. At minimum, revise `BATTERY_BAY_W`, `BATTERY_BAY_H`, and `BATTERY_BAY_DEPTH` after measuring your battery. Check the board outline, display opening, and side-access positions against the exact board. Then run the script in Blender's Scripting workspace. It saves a `.blend`, three separate STL files, and a preview beside the script.

The non-printable object named `DISPLAY MOCKUP - not a printable part` is only present so the aperture is visible in the scene/render. The STL exporter selects only the front bezel, battery tray, and lid.

## Fit validation needed

The model has been generated and opened in Blender, but no physical print or fit test has been performed. Before a final print:

- measure the actual board and battery;
- check port/slot center coordinates and protrusion depths;
- check whether the acrylic protector needs extra clearance;
- print a small port/fit test or a low-cost draft;
- adjust clearances for the printer, material, and intended assembly method.
