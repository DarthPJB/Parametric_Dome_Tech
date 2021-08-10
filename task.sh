#!/bin/sh
python ./full_model_generation.py
if (( $? ))
  then figlet "FAILED" ;
else fstl ./output/casing0.stl;
fi
