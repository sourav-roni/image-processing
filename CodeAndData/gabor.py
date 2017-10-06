import numpy as np
import cv2

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged
 
def build_filters():
	filters = []
	ksize = 11
 	for theta in np.arange(0, np.pi, np.pi / 16):
 		kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
 		kern /= 1.5*kern.sum()
 		filters.append(kern)
 	return filters
 
def process(img, filters):
 	accum = np.zeros_like(img)
 	for kern in filters:
 		fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
 		np.maximum(accum, fimg, accum)
 		return accum
 
if __name__ == '__main__':
	# import sys
	 
	# print __doc__
	# try:
	# 	img_fn = sys.argv[1]
	# except:
	# 	img_fn = 'test.png'
	 
	img_fn = "78004.jpg" 
	img = cv2.imread(img_fn)
	if img is None:
		print 'Failed to load image file:', img_fn
		sys.exit(1)
	 
	filters = build_filters()
	 
	res1 = process(img, filters)
	cv2.imshow('result', res1)
	cv2.waitKey(0)

	gray = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (3, 3), 0)

	wide = cv2.Canny(blurred, 10, 200)
	wide = cv2.cvtColor(wide, cv2.COLOR_GRAY2BGR)
	tight = cv2.Canny(blurred, 225, 250)
	tight = cv2.cvtColor(tight, cv2.COLOR_GRAY2BGR)
	auto = auto_canny(blurred)
	auto = cv2.cvtColor(auto, cv2.COLOR_GRAY2BGR)

	cv2.imshow("Edges", np.hstack([wide, tight, auto]))
	cv2.waitKey(0)

	cv2.destroyAllWindows()