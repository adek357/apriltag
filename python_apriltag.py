# import modulow
import apriltag
import argparse
import cv2
import time
import numpy

def get_distance(p, q):
    """ 
    Return euclidean distance between points p and q
    assuming both to have the same number of dimensions
    """
    # sum of squared difference between coordinates
    s_sq_difference = 0
    for p_i,q_i in zip(p,q):
        s_sq_difference += (p_i - q_i)**2
    
    # take sq root of sum of squared difference
    distance = s_sq_difference**0.5
    return distance



tag_size_cm=11
robot_xyz=(400,400,0)

#opcje dla modulu apriltag
options = apriltag.DetectorOptions(families='tag36h11',
                                 border=1,
                                 nthreads=4,
                                 quad_decimate=1.0,
                                 quad_blur=0.0,
                                 refine_edges=True,
                                 refine_decode=False,
                                 refine_pose=False,
                                 debug=False,
                                 quad_contours=True)
detector = apriltag.Detector(options)


camera_params=(3156.71852, 3129.52243, 359.097908, 239.736909)
tag_size=0.0762

#stworzenie okienka

cv2.namedWindow("preview")
video_cap = cv2.VideoCapture(0)
video_cap.set(3,800)
video_cap.set(4,800)

#sprawdzenie czy okienko istnieje

if video_cap.isOpened(): # proba pobrania pierwszej klatki
	rval, frame = video_cap.read()
else:
	rval = False

while rval:
	cv2.imshow("preview", frame)
	rval, frame = video_cap.read()
	key = cv2.waitKey(20)
	if key == 27: # exit on ESC
		break

	time.sleep(0.001) #opoznienie bo cvtColor byl pusty

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #zmiana klatki na szary color

	print("[INFO] detecting AprilTags...")
	results = detector.detect(gray) #detekcja apriltaga
	print("[INFO] {} total AprilTags detected".format(len(results)))

	# loop over the AprilTag detection results
	for r in results:
		# extract the bounding box (x, y)-coordinates for the AprilTag
		# and convert each of the (x, y)-coordinate pairs to integers
		(ptA, ptB, ptC, ptD) = r.corners
		ptB = (int(ptB[0]), int(ptB[1]))
		ptC = (int(ptC[0]), int(ptC[1]))
		ptD = (int(ptD[0]), int(ptD[1]))
		ptA = (int(ptA[0]), int(ptA[1]))

		#add print to output corners
		print(ptA,ptB,ptC,ptD)

		# draw the bounding box of the AprilTag detection
	#	cv2.line(frame, ptA, ptB, (0, 255, 0), 2)
	#	cv2.line(frame, ptB, ptC, (0, 255, 0), 2)
	#	cv2.line(frame, ptC, ptD, (0, 255, 0), 2)
	#	cv2.line(frame, ptD, ptA, (0, 255, 0), 2)
		# draw the center (x, y)-coordinates of the AprilTag
		(cX, cY) = (int(r.center[0]), int(r.center[1]))
	#	cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
		# draw the tag family on the image
	#	tagFamily = r.tag_family.decode("utf-8")
	#	cv2.putText(frame, tagFamily, (ptA[0], ptA[1] - 15),
	#		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
	#	print("[INFO] tag family: {}".format(tagFamily))
		tag_xyz=(cX,cY,)
		tag_size_px = numpy.sqrt((ptB[0]-ptA[0])**2+(ptD[0]-ptC[0])**2)
		print(tag_size_px)
		distance=get_distance(robot_xyz,tag_xyz)
		print(distance)

video_cap.release()
cv2.destroyWindow("preview")

