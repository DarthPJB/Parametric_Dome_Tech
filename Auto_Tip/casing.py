# Gridshell technology - John Bargman, 2022

import os, sys
sys.path.append(os.getcwd());

import cadquery as cq
import math as math

import profile_lib as prolib

from collections import namedtuple
from cadquery import exporters
from cadquery import importers

DEBUG_MODE = True;


## --------------------------- variables
Profile_Size = prolib.profile_sizes();

Tip_Length = 101;
Tip_Width_Extra = 10;
Tip_Angle_Length = 30;
Tip_Width = Profile_Size[0] + Tip_Width_Extra*2;
Tip_Height = Profile_Size[1];

Tip_Front_Angle = 12;
Tip_Top_Angle = 28.4;

## --------------------------- code

Track  = prolib.profile_gen(Tip_Length*2).translate((Tip_Angle_Length,0,0));

#if DEBUG_MODE == True: debug(Track, name='Track');


Tip_Cut_Block = cq.Workplane("XY").moveTo(0,-Tip_Width_Extra).box(Tip_Length, Tip_Width, Tip_Height, centered=[False,False,False]);

Tip_Front_Cut = cq.Workplane("XY").moveTo(-Tip_Length,-Tip_Width_Extra).box(Tip_Length, Tip_Width*2, Tip_Height, centered=[False,False,False])\
    .rotate([0,-Tip_Width_Extra,-1],[0,-Tip_Width_Extra,1], -Tip_Front_Angle);


Tip_Block = Tip_Cut_Block.cut(Track).cut(Tip_Front_Cut);

Cut_Edge = Tip_Block.vertices("(<<X[-2] or <<X) and <Z");

debug(Cut_Edge, name='cut edge');

show_object(Tip_Block, name='Printed_Tip', options=dict(color='#3333CC'));
show_object(Track, name='Profile', options=dict(color='#333333'));
