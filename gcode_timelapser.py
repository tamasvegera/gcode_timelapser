park_pos_x  = 0             # mm
park_pos_y  = 160.9           # mm
retract_length  = 15        # mm

push_length =   1           # mm
push_time = 100             # in ms
shutter_time = 1000          # in ms

gcode_raw = "EBHME_v1.2"     # .gcode
gcode_new = gcode_raw + "_timelapse"

gcode_file = gcode_raw + ".gcode"
gcode_file_new = gcode_new + ".gcode"

g = open(gcode_file, "r")
g_new = open(gcode_file_new, "w")

last_g1 = ""

while True:
    line = g.readline()
    if not line:
        break

    if "G1" in line:
        last_g1 = line

    if ";LAYER:" in line and ";LAYER:0" not in line:
        g_new.write(";TimeLapse\n")

        # RETRACT
        last_extruder_pos = float(last_g1[(last_g1.find("E") + 1):])
        retracted_extruder = str(round(last_extruder_pos - retract_length, 5))
        g_new.write("G1 F4200 E" + retracted_extruder + "\n")

        # parking
        g_new.write("G1 F9000 X" + str(park_pos_x) + " Y" + str(park_pos_y) + " ; Push button\n")
        g_new.write("MP400 ;Wait for move\n")
        g_new.write("G4 P" + str(push_time) + " ;Wait for push time\n")
        g_new.write("G1 F9000 Y" + str(park_pos_y-push_length) + "\n")      # pushed back from button a little bit
        g_new.write("G4 P" + str(shutter_time) + " ;Wait for shutter\n")

        # back to prev pos
        g_new.write(last_g1.split(" E")[0] + "\n")      # write only before E part

        # unretract
        g_new.write("G1 F4200 E" + str(last_extruder_pos) + "\n")

    g_new.write(line)
