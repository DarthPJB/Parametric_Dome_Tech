# Mike-Bike battery-box casing, by the Astral_3D Team aboard the Astral Ship, 2021-05-15
# Expecting CQ-Editor 0.2.0 or heigher, Cadquery 2.0.0
# This is version 3.0 of the battery-box design, a third prototype based heavily
# on the amazing work of our team!

import cadquery as cq
import math as math
from cadquery import exporters
from cadquery import importers

DEBUG_MODE = True;


## --------------------------- variables
Track_Height = 18
Track_Width = 45
Track_Steel_Width = 0.5;

Tip_Length = 101;
Tip_Width_Extra = 10;
Tip_Height = Track_Height

Tip_Angle_One = 12;
Tip_Angle_Two = 28.4;

# --------------------------------- precalulated

Tip_Width = Track_Width + Tip_Width_Extra;

## --------------------------- code

Track = cq.Workplane("XY").center(-Tip_Length/5,0).box(Tip_Length - Tip_Length/5, Track_Width, Track_Height)\
    .faces("-Z or -X or +X").shell(-Track_Steel_Width);

# if DEBUG_MODE == True: debug(Track, name='Track');


Square_Side = Tip_Length / 2 -Tip_Length/5;


Tip_Cut_One = cq.Workplane("XY").workplane(Track_Height/2).center(Tip_Length/5, 0)\
    .moveTo(0, Tip_Width/2 +1)\
    .lineTo(0, -Tip_Width/2 - 1)\
    .lineTo(Square_Side, - Tip_Width/2 - 1)\
    .polarLine(Tip_Width + 10, 90 + Tip_Angle_One).close().extrude(-Track_Height);

Tip_Cut_Box = cq.Workplane("XY").center(Tip_Length/2, 0).box(Tip_Length/2,Tip_Width,Track_Height).cut(Tip_Cut_One);

Tip_Cut_Two = Tip_Cut_Box.faces("<X").workplane().rect(Tip_Width,Tip_Height)
if DEBUG_MODE == True: debug(Tip_Cut_Two);

Tip_Block = cq.Workplane("XY").center(0, 0)\
    .box(Tip_Length, Tip_Width, Track_Height);

Auto_Tip = Tip_Block.cut(Track).cut(Tip_Cut_Box);



show_object(Auto_Tip, name='Printed_Tip', options=dict(color='#3333CC'));
show_object(Track, name='Profile', options=dict(color='#333333'));
