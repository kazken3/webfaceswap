#!/bin/sh

predictor_path = "./shape_predictor_68_face_landmarks.dat"

if [ -e $predictor_path ]; then
  wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 
  bzip2 -d ./shape_predictor_68_face_landmarks.dat.bz2
fi
