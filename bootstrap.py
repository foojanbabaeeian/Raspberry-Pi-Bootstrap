
# Imports
import mediapipe as mp
import cv2
from picamera2 import Picamera2
import time


# Initialize the pi camera
pi_camera = Picamera2()
# Convert the color mode to RGB
config = pi_camera.create_preview_configuration(main={"format": "RGB888"})
pi_camera.configure(config)


# Start the pi camera and give it a second to set up
pi_camera.start()
time.sleep(1)

def draw_pose(image, landmarks):
	''' 
	TODO Task 1
	
	Code to this fucntion to draw circles on the landmarks and lines
	connecting the landmarks then return the image.
	
	Use the cv2.line and cv2.circle functions.

	landmarks is a collection of 33 dictionaries with the following keys
		x: float values in the interval of [0.0,1.0]
		y: float values in the interval of [0.0,1.0]
		z: float values in the interval of [0.0,1.0]
		visibility: float values in the interval of [0.0,1.0]
		
	References:
	https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html
	https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
	'''

	# copy the image
	landmark_image = image.copy()
	
	# get the dimensions of the image
	height, width, _ = image.shape
	
	for landmark in landmarks.landmark:
		x, y = int(landmark.x * width), int(landmark.y * height)
		cv2.circle(landmark_image, (x, y), 5, (199, 5, 61), -1)
	return landmark_image
	
def main():
	''' 
	TODO Task 2
		modify this fucntion to take a photo uses the pi camera instead 
		of loading an image

	TODO Task 3
		modify this function further to loop and show a video
	'''
	
	while True:
		# Get a image frame as a numpy array
		image = pi_camera.capture_array()


		# display the image
		cv2.imshow("Video", image)


		# This waits for 1 ms and if the 'q' key is pressed it breaks the loop	 
		if cv2.waitKey(1) == ord('q'):
			break

		# Create a pose estimation model 
		mp_pose = mp.solutions.pose
	
		# start detecting the poses
		with mp_pose.Pose(
				min_detection_confidence=0.5,
				min_tracking_confidence=0.5) as pose:


			#image = cv2.imread("person.png")

			# To improve performance, optionally mark the image as not 
			# writeable to pass by reference.
			image.flags.writeable = False
		
			# get the landmarks
			results = pose.process(image)
		
			if results.pose_landmarks != None:
				result_image = draw_pose(image, results.pose_landmarks)
				#cv2.imwrite('output.png', result_image)
				cv2.imshow("annotated", result_image)
				#print(results.pose_landmarks)
			else:
				print('No Pose Detected')


if __name__ == "__main__":
	main()
	print('done')

    
# Close all the windows
#cv2.destroyAllWindows()


