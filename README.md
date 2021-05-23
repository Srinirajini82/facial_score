Program to find the Facial beauty score of the person:
======================================================

- face.py is implemeted to plote the different feature of the face

- a input file boy.png is used in this program for an experiment purpose

- boy2.png is written back on the filesystem with plotting as asked in the question.

Dependencies to execute the program:
------------------------------------
1) numPy
2) Pillow
3) face_recogition
4) dlib

How to start the program:
-------------------------
python3 face.py -i boy.png


Limitation:
-----------
currently the program only identifies the facial features and compute the ratio, and also the following three checks as asked in question are implemented, but it did not compute the score based on the computed ratio and check .

following three check are implemented:
1) computing the Height to Width ration and check for the idle ratio which is 1.6
2) distance between the intersects which is the distacne from 1) forehead to eye lid, 2) distance from eyelid to nose and 3) distance from nose to chin. The check to identify all these three distance are equal is implemented.
3) distance between the eys and the width of the is compute to check they are equal , similarly the length of the nose and the lenth of the ears is compared to check they are equal


TODO:
----
Computation of "coefficient of variations" using scipy to return the beauty score
