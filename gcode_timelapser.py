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

    if ("G1" in line or "G0" in line) and ("X" in line or "Y" in line):
        temp_line = line.split(" X")[1]
        if " " in temp_line:
            last_x_pos = float(temp_line[:temp_line.find(" ")])
        else:
            last_x_pos = float(temp_line[:temp_line.find("\n")])

        temp_line = line.split(" Y")[1]
        if " " in temp_line:
            last_y_pos = float(temp_line[:temp_line.find(" ")])
        else:
            last_y_pos = float(temp_line[:temp_line.find("\n")])

    if ";" not in line and "E" in line and "G1" in line:
        temp_line = line.split(" E")[1]
        if " " in temp_line:
            last_e_pos = float(temp_line[:temp_line.find(" ")])
        else:
            last_e_pos = float(temp_line[:temp_line.find("\n")])
        #last_e_pos = float(line[(line.find("E") + 1):])

    if ";LAYER:" in line and ";LAYER:0" not in line:
        g_new.write(";TimeLapse\n")

        # RETRACT
        retracted_extruder = str(round(last_e_pos - retract_length, 5))
        g_new.write("G1 F4200 E" + retracted_extruder + "\n")

        # parking
        g_new.write("G1 F9000 X" + str(park_pos_x) + " Y" + str(park_pos_y) + " ; Push button\n")
        g_new.write("MP400 ;Wait for move\n")
        g_new.write("G4 P" + str(push_time) + " ;Wait for push time\n")
        g_new.write("G1 F9000 Y" + str(park_pos_y-push_length) + "\n")      # pushed back from button a little bit
        g_new.write("G4 P" + str(shutter_time) + " ;Wait for shutter\n")

        # back to prev pos
        g_new.write("G1 F9000 X" + str(last_x_pos) + " Y" + str(last_y_pos) + "\n")

        # unretract
        g_new.write("G1 F4200 E" + str(last_e_pos) + "\n")

    g_new.write(line)
