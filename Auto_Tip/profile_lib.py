# This library file will generate any 'length' of the profile
# overriding this should allow for creation of gridshells using
# different profile types.

# Gridshell technology - John Bargman, 2022

import os, sys
import math as math
import cadquery as cq

Track_Height = 18;
Track_Width = 45;
Track_metal_Thickness = 0.5;

# function to generate profile sketch
def profile_sketch():
    profile = cq.Sketch().segment((0,0), (0,Track_Height))\
    .segment((0,Track_Height),(Track_Width, Track_Height))\
    .segment((Track_Width, Track_Height), (Track_Width, 0))\
    .segment((Track_Width, 0),(Track_Width - Track_metal_Thickness, 0))\
    .segment((Track_Width - Track_metal_Thickness, 0),(Track_Width - Track_metal_Thickness, Track_Height - Track_metal_Thickness))\
    .segment((Track_Width - Track_metal_Thickness, Track_Height - Track_metal_Thickness),(Track_metal_Thickness,Track_Height - Track_metal_Thickness))\
    .segment((Track_metal_Thickness,Track_Height - Track_metal_Thickness),(Track_metal_Thickness, 0))\
    .segment((Track_metal_Thickness, 0), (0,0)).assemble();
    return profile;

# function to generate profile of given length.
def profile_gen(length):
    profile = cq.Workplane("YZ").placeSketch(profile_sketch()).extrude(length);
    return profile;

def profile_sizes():
    return (Track_Width, Track_Height);
#debug(profile_gen(100));
