# Mike-Bike battery-box casing, by the Astral_3D Team aboard the Astral Ship, 2021-05-15
# Expecting CQ-Editor 0.2.0 or heigher, Cadquery 2.0.0
# This is version 3.0 of the battery-box design, a third prototype based heavily
# on the amazing work of our team!

import cadquery as cq
import math as math
from collections import namedtuple
from cadquery import exporters
from cadquery import importers

DEBUG_MODE = True;


## --------------------------- variables
Track_Height = 18
Track_Width = 45
Track_metal_Thickness = 0.5;

Tip_Length = 101;
Tip_Width_Extra = 10;
Tip_Angle_Length = 30;
Tip_Height = Track_Height

Tip_Angle_One = 12;
Tip_Angle_Two = 28.4;

# --------------------------------- precalulated

Tip_Width = Track_Width + Tip_Width_Extra * 2;

## --------------------------- code

Track  = cq.Workplane("XY").moveTo(Tip_Angle_Length,0).box(Tip_Length * 2, Track_Width, Track_Height, centered=[False,False,False])\
    .faces("-Z or -X or +X").shell(-Track_metal_Thickness);

# if DEBUG_MODE == True: debug(Track, name='Track');



#Square_Side = Tip_Length / 2 -Tip_Length/5;

Tip_Block = cq.Workplane("XY").moveTo(0,-Tip_Width_Extra).box(Tip_Length, Tip_Width, Tip_Height, centered=[False,False,False]);

Tip_Cut_One = cq.Workplane("XY").moveTo(0,-Tip_Width_Extra).box(Tip_Length, Tip_Width, Tip_Height, centered=[False,False,False])\
    .rotate([0,-1,0],[0,1,0], -Tip_Angle_Two);
debug(Tip_Cut_One);

Tip_Cut_Two = cq.Workplane("XY").moveTo(0,-Tip_Width_Extra).box(Tip_Length, Tip_Width, Tip_Height, centered=[False,False,False])\
    .rotate([0,-Tip_Width_Extra,-1],[0,-Tip_Width_Extra,1], Tip_Angle_Two);
debug(Tip_Cut_Two);
#Tip_Cut_Box = cq.Workplane("XY").center(Tip_Length/2, 0).box(Tip_Length/2,Tip_Width,Track_Height).cut(Tip_Cut_One);

#Tip_Cut_Two = Tip_Cut_Box.faces("<X").workplane().rect(Tip_Width,Tip_Height)
#if DEBUG_MODE == True: debug(Tip_Cut_Two);

#Tip_Block = cq.Workplane("XY").center(0, 0)\
#    .box(Tip_Length, Tip_Width, Track_Height);

#Auto_Tip = Tip_Block.cut(Track).cut(Tip_Cut_Box);



show_object(Tip_Block, name='Printed_Tip', options=dict(color='#3333CC'));
show_object(Track, name='Profile', options=dict(color='#333333'));
