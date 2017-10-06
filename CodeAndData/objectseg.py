import numpy as np
import glob
import cv2
import os

def auto_canny(image, sigma=0.3):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged

def main():
	curr = os.getcwd()
	print curr
	files = glob.glob(curr+"/Data/OriginalImage/*.jpg")
	for i in range(0,len(files)):
		# print files[i]
		filename = files[i].split("/")[-1]
		print "Processing ... " + filename
		image = cv2.imread(files[i])
		gt = cv2.imread(curr+"/Data/GroundTruthSegmentation/"+filename)

		blurred = cv2.GaussianBlur(image, (5, 5), 0)
		gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

		print image.shape
		print blurred.shape
		print gt.shape		

		wide = cv2.Canny(gray, 10, 200)
		wide = cv2.cvtColor(wide, cv2.COLOR_GRAY2BGR)
		tight = cv2.Canny(gray, 225, 250)
		tight = cv2.cvtColor(tight, cv2.COLOR_GRAY2BGR)
		auto = auto_canny(gray)
		auto = cv2.cvtColor(auto, cv2.COLOR_GRAY2BGR)

		print wide.shape
		print tight.shape
		print auto.shape

		# # cv2.imshow("Edges", np.hstack([wide, tight, auto]))
		# # cv2.waitKey(0)
		
		widefile = curr+"/Data/PredictedSegmentation/wide/"+filename
		tightfile = curr+"/Data/PredictedSegmentation/tight/"+filename
		autofile = curr+"/Data/PredictedSegmentation/auto/"+filename
		
		# print newfile
		cv2.imwrite(widefile,np.hstack([image, gt, wide]))
		cv2.imwrite(tightfile,np.hstack([image, gt, tight]))
		cv2.imwrite(autofile,np.hstack([image, gt, auto]))

		print "Segements generated for ... " + filename 
	print "DONE"

if __name__ == '__main__':
	main()