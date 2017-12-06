#necessary python imports 
import numpy as np
import glob
import cv2
import os

#a function auto canny wich is a helper function 
#it computes the median of the single channel pixels 
#and then computes the upper and lower bounds depending 
#image statistics computed using the median function of 
#the numpy library.
def find_stats(image, sigma=0.3):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower_bound = int(max(0, (1.0 - sigma) * v)) #compute lower threshold
	upper_bound = int(min(255, (1.0 + sigma) * v)) #compute upper threshold
	edged = cv2.Canny(image, lower_bound, upper_bound)
 
	# return the edged image
	return edged

#main function
def main():
	#get current working directory
	curr = os.getcwd()
	#print curr
	#get all input images from the input image folder
	files = glob.glob(curr+"/Data/OriginalImage/*.jpg")
	#run the algorithm for all the input images
	for i in range(0,len(files)):
		# print files[i]
		#get the input file name
		filename = files[i].split("/")[-1]
		#print "Processing ... " + filename
		image = cv2.imread(files[i])             #reding the input image
		#retrieve the groubd truth segmentation image 
		#which is the averaged out image of for five different 
		#human users who have viewed and annotated the image 
		#to mark the salient boundaries
		gt = cv2.imread(curr+"/Data/GroundTruthSegmentation/"+filename)

		#blur the input image
		blurred = cv2.GaussianBlur(image, (5, 5), 0)

		#find the grayscale image from the threshold image
		gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

		#check various dimensions for debuggging
		#print image.shape
		#print blurred.shape
		#print gt.shape		

		#we compute three different segmentation based on the 
		#different values of the lower and upper thresholds

		#first is the wide range in which the lower threshold is quite low  and the upper one is quite high
		wide = cv2.Canny(gray, 10, 200)
		#convert form gray to BGR to get a three channeled output image 
		wide = cv2.cvtColor(wide, cv2.COLOR_GRAY2BGR)

		#second is the tight range in which the lower threshold is quite high  and the upper one is even higher 
		#but the difference between the two is very small
		tight = cv2.Canny(gray, 225, 250)
		#convert form gray to BGR to get a three channeled output image 
		tight = cv2.cvtColor(tight, cv2.COLOR_GRAY2BGR)

		#third is when the range in which both lower and upper thresholds are determined by the function find_stats
		auto = find_stats(gray)
		#convert form gray to BGR to get a three channeled output image 
		auto = cv2.cvtColor(auto, cv2.COLOR_GRAY2BGR)

		#check various dimensions for debuggging
		#print wide.shape
		#print tight.shape
		#print auto.shape

		# # cv2.imshow("Edges", np.hstack([wide, tight, auto]))
		# # cv2.waitKey(0)
		
		#genrate filenames to be saved
		widefile = curr+"/Data/PredictedSegmentation/wide/"+filename
		tightfile = curr+"/Data/PredictedSegmentation/tight/"+filename
		autofile = curr+"/Data/PredictedSegmentation/auto/"+filename
		new = curr+"/Data/PredictedSegmentation/new/"+filename
		
		#save the three different outputs
		cv2.imwrite(new,auto)
		#cv2.imwrite(widefile,np.hstack([image, gt, wide]))
		#cv2.imwrite(tightfile,np.hstack([image, gt, tight]))
		#cv2.imwrite(autofile,np.hstack([image, gt, auto]))

		#print "Segements generated for ... " + filename 
	#print "DONE"

if __name__ == '__main__':
	main()
