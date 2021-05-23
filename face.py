import argparse, os
from argparse import ArgumentParser
import face_recognition
import math
from PIL import Image, ImageDraw
import numpy as np
import argparse

def validate_file(f):
    if not os.path.exists(f):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError(f"{f} does not exist")
    return f

def load_image(path):
	return face_recognition.load_image_file(path)

def get_height_width_ratio(point):
	height = point[8][1] - point[len(point) -1][1]
	width = point[15][0] - point[1][0]
	return float(height / width)


def plotRegions(data,xCoordi, yCoordi):
	data[int(xCoordi),int(yCoordi)] = 255
	data[int(xCoordi - 1),int(yCoordi)] = 255
	data[int(xCoordi + 1),int(yCoordi)] = 255
	data[int(xCoordi - 2),int(yCoordi)] = 255
	data[int(xCoordi + 2),int(yCoordi)] = 255
	data[int(xCoordi),int(yCoordi + 1)] = 255
	data[int(xCoordi),int(yCoordi - 1)] = 255
	data[int(xCoordi),int(yCoordi + 2)] = 255
	data[int(xCoordi),int(yCoordi - 2)] = 255

def draw_line_fromPoint(data, p1,p2, run=60):
	c1,r1 = p1
	c2,r2 = p2

	for i in range(run):
		data[int(r1),int((c1-run) + i)] = 255
		data[int(r2),int(c2 + i)] = 255

def nose_length(data,p):
	plotRegions(data, p[33][1], p[33][0])
	plotRegions(data, p[27][1], p[27][0])
	return p[33][1] - p[27][1]

def plot_jaw_forehead(data,p):
	plotRegions(data, p[68][1], p[68][0])
	plotRegions(data, p[8][1], p[8][0])

def plot_eye_tip(data,p):
	plotRegions(data, p[0][1], p[0][0])
	plotRegions(data, p[16][1], p[16][0])

def plot_ear(data,p):
	plotRegions(data, p[17][1], p[17][0])
	plotRegions(data, p[26][1], p[26][0])
	draw_line_fromPoint(data, p[17],p[26])
	c1,r1 = p[32]
	c2,r2 = p[2]
	c3,r3 = p[14]
	c4,r4 = p[34]
	draw_line_fromPoint(data, (c2,r1),(c3,r4), 40)
	return r4 - p[26][1]

def plot_eye(data,p):
	c1,r1 = p[39]
	c2,r2 = p[42]
	c3,r3 = p[45]
	plotRegions(data,r1,c1)
	plotRegions(data,r2,c2)
	plotRegions(data,r3,c3)
	return c3 - c2

def length_betweenEyes(data,p):
	return p[42][0]- p[39][0]

def find_intercest_distance(data,p):
	length_forehead_2_eye = p[45][1] - p[68][1]
	length_eye_2_nose = p[33][1] - p[45][1]
	length_nose_2_chin = p[8][1] - p[33][1]
	return (length_forehead_2_eye, length_eye_2_nose, length_nose_2_chin)

def checkB_IntersectsEqual(f):
	features = list(f)
	return all(element == features[0] for element in features)

def checkA_fHWr_1_6(h,w):
	return True if float(h/w) == 1.6 else False

def checkC_nose_2_ear_eye_width(faceFeature):
	return faceFeature['wEye'] == faceFeature['dEye'] if faceFeature['nose'] == faceFeature['ear'] else False

def find_facialScore(filePath):
    image = load_image(filePath)
    landmarks = face_recognition.api._raw_face_landmarks(image)
    landmarks_as_tuples = [(p.x, p.y) for p in landmarks[0].parts()]
    #appending the forehead at the last position 68th index with the assumption 50 rows above the eyebrow
    landmarks_as_tuples.append((landmarks_as_tuples[8][0], landmarks_as_tuples[24][1]-50))
	
    #image = Image.open('boy.png').convert('L')
    data = np.array(image)
    plot_jaw_forehead(data, landmarks_as_tuples)
    plot_eye_tip(data, landmarks_as_tuples)
    nose_len = nose_length(data,landmarks_as_tuples)
    print("Nose length : ",nose_len)
    ear_length = plot_ear(data, landmarks_as_tuples)
    print("Ear length : ",ear_length)
    eye_width = plot_eye(data, landmarks_as_tuples)
    print("Width of the eye : ", eye_width)
    len_bew_eye = length_betweenEyes(data, landmarks_as_tuples)
    print("distance between eye : ", len_bew_eye)
    image2 = Image.fromarray(data)
    image2.save('boy2.png', format='PNG')

    print("Height to width ration : ",get_height_width_ratio(landmarks_as_tuples))
    distance_tuple = find_intercest_distance(data,landmarks_as_tuples)
    print("length between intersects : ", distance_tuple)
    print("does the hight-to-width ratio is idle ? ", checkA_fHWr_1_6(landmarks_as_tuples[8][1] - landmarks_as_tuples[68][1] ,landmarks_as_tuples[15][0] - landmarks_as_tuples[1][0] ))
    print("does the distance in interscets are same ? : ", checkB_IntersectsEqual(distance_tuple))
    print("does the ear and node equal ? : ", checkC_nose_2_ear_eye_width({'nose':nose_len, 'ear': ear_length, 'wEye' : eye_width, 'dEye':len_bew_eye }))

if __name__ == '__main__':
	parser = ArgumentParser(description="File to parse beauty index")
	parser.add_argument("-i", "--input", dest="filename", required=True,type=validate_file,help="input file", metavar="FILE")
	args = parser.parse_args()
	find_facialScore(args.filename)
