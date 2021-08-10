# Mike-Bike battery-box casing, by the Astral_3D Team aboard the Astral Ship, 2021-05-15
# Expecting CQ-Editor 0.2.0 or heigher, Cadquery 2.0.0
# This is version 3.0 of the battery-box design, a third prototype based heavily
# on the amazing work of our team!

import cadquery as cq
from cadquery import exporters
from cadquery import importers

DEBUG_MODE = True;
# Text to be placed on the box - note custom font use, should be in CQ's working path
cut_text_position_x = 180;
cut_text_position_y = 60;
cut_text_angle = 24;
cut_text = "Created By @Astral_3D";
cut_text_font = "Trueno Bold";
cut_text_fontPath = "truenobd.otf"

## ----------- Core variables --------------------------------------------------    ---                     Variable initialisation

##Tolerances
fit_bike_excess = 2; #offset from bike-frame to allow human-fitting
fit_tolerance_casing = 0.1; # offset between meeting-faces to allow for print-error
fit_tolerance_doubled = fit_tolerance_casing * 2;

##Casing creation settings
box_total_width = 70; # Internal height of the box (height of 18650 batteries)
box_corner_fillet = 25; # size of edge-ring filleting
box_wall_thickness = 8; # thickness of casing walls

##Lid creation settings
lid_casing_split_distance = 10;
lid_casing_split_offset = 60;
lid_Lapping_Offset = box_wall_thickness
lid_lapping_Thickness = (box_wall_thickness+fit_tolerance_doubled)/2

##Screw-placement and settings
screw_placement_distance = 60;
screw_thread_diam = 5 - fit_tolerance_casing; # Screw Thread diameter for connecting face-plate to casing
screw_post_diam = screw_thread_diam + box_wall_thickness; # screw-post-width pre-calulation
screw_depth = 40 + box_wall_thickness;   # length of screw-fitting into the box itself
screw_cap_diam = 9 + fit_tolerance_doubled; # Size of screw-cap for recessed fitting
screw_cap_height = 2 + fit_tolerance_casing; # Number of milimemeters to recess the screw-caps
# define per-step differences for screw-hole placement                              --- TODO: generate these according to generative geometary
screw_rising_offset = [56.59558, 25.31681]; # this value should be effectively equal to screw_placement_distance (as a diagnal line)
screw_rising_difference = [-4,3]
screw_falling_offset = [8,screw_placement_distance];


## Point lists for generating geometary                                         ---                     Point Lists

# generate points list from the angle and length of the constraining edges (TODO: should import from svg)
distance_angle_points_list = [
#first edge from 0,0 running along the top of the box.
(507.26, 0),
# second edge moving down the back of the bike-frame
(250, 82.48),
#edge up towards meeting the triangle
(150.52, 209.52)];

screw_placement_points = [
    (distance_angle_points_list[0][0]-(box_corner_fillet) - fit_bike_excess, (box_corner_fillet/2)), # Top Left Corner
    (98, 34), # Top Right corner
    (505, 205)] # Bottom Left Corner

newArray = screw_placement_points + distance_angle_points_list

## calulate maximum enclosing area                                              ---                     Extents Calulations
startx = 0
starty = 0
for x,y in newArray:
    if x > startx: startx = x;
    if y > starty: starty = y;

Maximum_Size = [startx + (box_corner_fillet*2), starty + (box_corner_fillet*2) , box_total_width * 2];

if DEBUG_MODE: log(Maximum_Size);
Xpos = (Maximum_Size[0] / 2) + lid_casing_split_offset;
Ypos = (Maximum_Size[1] / 4)
Bezier_Cut_Points = [
    (Xpos- lid_casing_split_offset, Ypos*1),
    (Xpos, Ypos*2),
    (Xpos- lid_casing_split_offset, Ypos*3)
]

##Cable Hole Settings
Cable_hole_diam = 20; # Size of the cable-hole (20mm is a good fit for cable-plugs)
Cable_hole_position = cq.Vector((box_corner_fillet * 3) + box_wall_thickness, box_total_width/2, Maximum_Size[0]);
Cable_hole_angle = 0;
Cable_hole_Cut_Depth = Maximum_Size[1]/4;

#Holes along diagnal edges                                                          ---     Filling point lists with screw-placements
for risingpoints in range(1,8):
    if risingpoints < 6:
        screw_placement_points.append((\
        screw_placement_points[1][0] + screw_rising_offset[0] * risingpoints ,\
        screw_placement_points[1][1] + screw_rising_offset[1] * risingpoints));
    else: #Second diagnal edge requires some tweaking.
        screw_placement_points.append((\
        (screw_placement_points[1][0] + screw_rising_offset[0] * risingpoints) + screw_rising_difference[0] * (risingpoints-5)  ,\
        (screw_placement_points[1][1] + screw_rising_offset[1] * risingpoints) + screw_rising_difference[1] * (risingpoints-5) ));

#Holes at 60mm intervals along top-edge
for top_edge_points in range(1,7):
        screw_placement_points.append((\
        screw_placement_points[0][0] - (screw_placement_distance * top_edge_points ), screw_placement_points[0][1]));

for fallingpoints in range(1,4):
    screw_placement_points.append((\
    screw_placement_points[2][0] - screw_falling_offset[0] * fallingpoints , screw_placement_points[2][1] - screw_falling_offset[1] * fallingpoints));

# ---------- Generate Core Geometary -------------------------------------------    ---                     MESH GENERATION

# place workplane in correct location                                               ---                 Generate Text Inverse volumes
text = cq.Workplane("XY").transformed(
    offset=cq.Vector(cut_text_position_x,cut_text_position_y, box_total_width + box_wall_thickness/2),
    rotate=cq.Vector(0,0,180 + cut_text_angle))\
.text(cut_text, 10, box_wall_thickness/2, font=cut_text_font, fontPath=cut_text_fontPath);              #generate text for the lid
# place workplane in correct location                                               ---         TODO: Mirror this using the mirror-function
text2 = cq.Workplane("XY").transformed(
    offset=cq.Vector(cut_text_position_x,cut_text_position_y, -box_wall_thickness / 2),
    rotate=cq.Vector(180,0, -cut_text_angle))\
.text(cut_text, 10, box_wall_thickness/2, font=cut_text_font, fontPath=cut_text_fontPath) ; #generate text for the base

text_cut_volume = text.union(text2);
if DEBUG_MODE: debug(text_cut_volume, name='text-cutting volume');

# Generate the Spline-bezier cut and repepeat to creat lapping pannels              ---                     Creating lapping pannel Inverse-Geometary
Cut_Volume = cq.Workplane("XY").workplane(-lid_lapping_Thickness*2).center(lid_Lapping_Offset,0)\
.lineTo(Maximum_Size[0]/2, 0).spline(Bezier_Cut_Points,includeCurrent=True).lineTo(0,Maximum_Size[1]/2).close()\
.extrude(lid_lapping_Thickness);

Cut_Volume2 = cq.Workplane("XY").workplane(lid_lapping_Thickness + box_total_width).center(lid_Lapping_Offset,0)\
.lineTo(Maximum_Size[0]/2, 0).spline(Bezier_Cut_Points,includeCurrent=True).lineTo(0,Maximum_Size[1]/2).close()\
.extrude(lid_lapping_Thickness);

Cut_Volume3 = cq.Workplane("XY").workplane(-(lid_lapping_Thickness + fit_bike_excess))\
.lineTo(Maximum_Size[0]/2, 0).spline(Bezier_Cut_Points,includeCurrent=True).lineTo(0,Maximum_Size[1]/2).close()\
.extrude(box_total_width + lid_lapping_Thickness * 3 + fit_tolerance_doubled);

Cut_Volume = Cut_Volume.union(Cut_Volume3).union(Cut_Volume2);

if DEBUG_MODE : debug(Cut_Volume, name='bezier-seperation volume');
#Generate Inverse Geometary                                                         ---                     Creating opposite lapping pannel Inverse-Geometary
Inverse_Cut_Volume = cq.Workplane("XY").workplane(-box_wall_thickness*2).center(Maximum_Size[0]/2,Maximum_Size[1]/2)\
.rect(Maximum_Size[0], Maximum_Size[1], centered=True).extrude(Maximum_Size[2])\
.cut(Cut_Volume.translate(cq.Vector(fit_tolerance_doubled,0,0)));

if DEBUG_MODE : debug(Inverse_Cut_Volume, name='inverse bezier-seperation volume');

#initial workplane generation                                                       ---           ****** Casing Generation ******
perimeter = cq.Workplane("XY");

# Generate plane containing wire-loop                                               ---                     WIRE LOOP
for point in distance_angle_points_list:
    perimeter = perimeter.polarLine(point[0],point[1])
perimeter.close();

# shrink the wire-loop to handle tolerance and wall box_wall_thickness
casing_edge = perimeter.edges().offset2D(-(fit_bike_excess + box_wall_thickness))
# Extrude edge to make casing shape                                                 ---                     Casing Geometary Extrude
casing_geometry = casing_edge.extrude(box_total_width);
# fillet edges to make for nice-curved ends
casing_geometry = casing_geometry.edges("|Z").fillet(box_corner_fillet);
# Shell the casing to make the inside hollow.                                       ---                     Shell Casing
casing_geometry = casing_geometry.shell(box_wall_thickness,"arc");

# In the bottom box, add the screw-posts                                            ---                     Bottom casing Post placement
#casing_geometry = casing_geometry.faces(">Z").workplane().pushPoints(screw_placement_points).circle(screw_post_diam/2).extrude(-box_total_width);

# Position a workplane above the edges that need cutting                            ---                     Casing Cable Cut
casing_cable_cut = cq.Workplane("YZ").transformed(
    offset=Cable_hole_position,
    rotate=cq.Vector(0, Cable_hole_angle,0));
# Create a cylinder to represent the material to be removed by the cut.
casing_cable_cut = casing_cable_cut.circle(Cable_hole_diam/2).extrude(-Cable_hole_Cut_Depth)
if DEBUG_MODE : debug(casing_cable_cut, name='cable-hole cut volume');
# Subtract the resulting geometary.
casing_geometry = casing_geometry.cut(casing_cable_cut);

# In the top plate, cut holes for the screws to enter the casing through.           ---                     screw hole cutting
#debug(casing_geometry.faces(">Z").workplane().pushPoints(screw_placement_points).circle(screw_thread_diam/2))
#casing_geometry =  casing_geometry.faces(">Z").workplane().pushPoints(screw_placement_points).circle(screw_thread_diam/2).cutBlind(-screw_depth + box_wall_thickness);
# In the top plate, sink holes for the screw-heads to be recessed slighty.
#casing_geometry =  casing_geometry.faces(">Z").workplane().pushPoints(screw_placement_points).circle(screw_cap_diam/2).cutBlind(-screw_cap_height);

#   Cut casing Text from the case parts                                             ---                     Cut casing text
casing_geometry = casing_geometry.cut(text_cut_volume);

# Split the casing into two parts                                                   ---                     Seperate left and right halves of the casing
casing_geometry_Left = casing_geometry.intersect(Cut_Volume)
casing_geometry_Right = casing_geometry.intersect(Inverse_Cut_Volume)

# Split casing_geometry into top and bottom parts, this will result in four total parts.
# (top being the thin lid, bottom being the box-casing itself)                      ---                     Casing Split
casing_top_Left = casing_geometry_Left.faces(">Z").workplane(-(box_wall_thickness+lid_casing_split_distance)).split(keepTop=True)
casing_bottom_Left = casing_geometry_Left.faces(">Z").workplane(-(box_wall_thickness+lid_casing_split_distance)).split(keepTop=False,keepBottom=True);
casing_top_Right = casing_geometry_Right.faces(">Z").workplane(-(box_wall_thickness+lid_casing_split_distance)).split(keepTop=True)
casing_bottom_Right = casing_geometry_Right.faces(">Z").workplane(-(box_wall_thickness+lid_casing_split_distance)).split(keepTop=False,keepBottom=True);

## Render resulting geometary                                                       ---                 Render Results
show_object(casing_top_Left, name='casing_lid_left', options=dict(color='#5555ee'));
show_object(casing_top_Right, name='casing_lid_right', options=dict(color='#ee5555'));
show_object(casing_bottom_Right, name='casing_right', options=dict(color='#3333cc'));
show_object(casing_bottom_Left, name='casing_left', options=dict(color='#cc3333'));
