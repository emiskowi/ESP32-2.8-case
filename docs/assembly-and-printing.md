# Assembly and printing

## Printable parts

1. `model/ESP32_CYD_front_bezel.stl` — front frame and board cradle.
2. `model/ESP32_CYD_battery_tray.stl` — rear battery bay and separator/bulkhead.
3. `model/ESP32_CYD_battery_lid.stl` — removable rear cover.

The Blender scene also contains a display-surface mockup for visualization; it is not a printed part and is excluded from the STL exports.

## Fasteners

The current model provides four 3.2 mm clearance bores through the tray and lid, aligned with 2.6 mm pilot holes in the front bezel. It is intended for four M3 × 25 mm screws self-tapping into the front part. Screw heads are not countersunk. Test the pilot diameter in scrap of the same filament before assembly; if using machine screws and inserts, revise the pilot holes and bosses accordingly.

The screw positions and hole spacing are part of this prototype and have not been confirmed against board mounting holes; the case uses perimeter fastening rather than relying on the CYD PCB holes.

## Print orientation

- **Front bezel:** place the display/front face flat on the build plate. The board pocket opens upward/rearward.
- **Battery tray:** place the closed separator face on the plate, with the battery pocket opening upward.
- **Lid:** print flat on its broad face.

These are suggested orientations. Inspect the slicer preview for bridging and support needs; material, printer, and slicer settings vary. The current geometry is modeled in millimeters and the STL exports are separate per part.

## Assembly sequence

1. Inspect the board pocket and opening against the actual CYD board. Do not force the display or acrylic protector into a tight fit.
2. Insert the board from the rear of the front bezel so the display faces the front window. Route the cable/connectors without pinching them.
3. Place the battery in the rear pocket only after confirming cell dimensions and polarity/connector compatibility. Keep the lead clear of the lid seam and screw paths.
4. Route the battery lead through the separator pass-through into the board compartment.
5. Align the battery tray with the bezel and attach the lid using the four screws.
6. Before powering, inspect for pinched wires, exposed conductors, and pressure on the LiPo pouch.

The enclosure does not provide strain relief beyond the pass-through and does not add battery charging circuitry. Use the board's intended power/charging path and follow the battery maker's guidance.

## Safety and fit notes

- Do not crush, puncture, bend sharply, or tightly clamp a LiPo pouch cell.
- Preserve room for the protection board, connector, and wiring; capacity alone is not enough to determine the fit.
- Keep screw tips, sharp print edges, and heat sources away from the battery.
- Check clearances with a low-cost draft/fit test before committing to the full enclosure.
