

# import the necessary packages
from gi_detector import helpers
import numpy as np
import argparse
import glob
import cv2
import cPickle
import glob
import random
import h5py
from skimage.feature import hog
from skimage import data,color,exposure
from sklearn.svm import SVC
from scipy import io


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="Path to  test images")
ap.add_argument("-v", "--visualize",
	help="Flag indicating whether or not to visualize each iteration")
ap.add_argument("-p", "--path",
	help="path to gi_detector")
args = vars(ap.parse_args())

path_1 = '/Users/ankitrai/Dropbox/ppao_VM/gi_detector/'
def pyramid(image, scale=1.5, minSize=(55,55)):
    # yield the original image
    yield image

    # keep looping over the pyramid
    while True:
        # compute the new dimensions of the image and resize it
        w = int(image.shape[1] / scale)
        image = imutils.resize(image, width=w)

        # if the resized image does not meet the supplied minimum
        # size, then stop constructing the pyramid
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break

        # yield the next image in the pyramid
        yield image
def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in xrange(0, image.shape[0], stepSize):
        for x in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])
def detect(image, winDim, winStep=4, pyramidScale=1.5, minProb=0.7):
		# initialize the list of bounding boxes and associated probabilities


		# loop over the image pyramid
    pyramid_layers = pyramid(image,scale=1.5,minSize=(100,100))
    for layer in pyramid_layers:
        # determine the current scale of the pyramid
        scale = image.shape[0] / float(layer.shape[0])
        # loop over the sliding windows for the current pyramid layer
        for (x, y, window) in sliding_window(layer, winStep, winDim):
            (winH, winW) = window.shape[:2]
            if winH == winDim[1] and winW == winDim[0]:
            # extract HOG features from the current window and classifiy whether or
            # not this window contains an object we are interested in
                fd, hog_image = hog(window, orientations=8, pixels_per_cell=(16, 16),cells_per_block=(1, 1), visualise=True)
                features = fd.reshape(1, -1)
                prob = model.predict_proba(features)[0][1]
                    # check to see if the classifier has found an object with sufficient
                    # probability
                if prob > minProb:
                    (startX, startY) = (int(scale * x), int(scale * y))
                    endX = int(startX + (scale * winW))
                    endY = int(startY + (scale * winH))
                    boxes.append((startX, startY, endX, endY))
                    probs.append(prob)
# return a tuple of the bounding boxes and probabilities
    return (boxes, probs)

    class HOG:
	def __init__(self, orientations=9, pixelsPerCell=(4, 4), cellsPerBlock=(2, 2), normalize=True):
		# store the number of orientations, pixels per cell, cells per block, and
		# whether normalization should be applied to the image
		self.orientations = orientations
		self.pixelsPerCell = pixelsPerCell
		self.cellsPerBlock = cellsPerBlock
		self.normalize = normalize

	def describe(self, image):
		# compute Histogram of Oriented Gradients features
		hist = feature.hog(image, orientations=self.orientations, pixels_per_cell=self.pixelsPerCell,cells_per_block=self.cellsPerBlock, transform_sqrt=self.normalize)
		hist[hist < 0] = 0

		# return the histogram
		return hist
class RGBHistogram:
	def __init__(self, bins):
		# store the number of bins the histogram will use
		self.bins = bins

	def describe(self, image, mask = None):
		# compute a 3D histogram in the RGB colorspace,
		# then normalize the histogram so that images
		# with the same content, but either scaled larger
		# or smaller will have (roughly) the same histogram
		hist = cv2.calcHist([image], [0, 1, 2],
			None, self.bins, [0, 256, 0, 256, 0, 256])
		cv2.normalize(hist, hist)

		# return out 3D histogram as a flattened array
		return hist.flatten()
def hog(img):
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    mag, ang = cv2.cartToPolar(gx, gy)
    bins = np.int32(bin_n*ang/(2*np.pi))    # quantizing binvalues in (0...16)
    bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
    mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)     # hist is a 64 bit vector
    return hist

class LocalBinaryPatterns:
	def __init__(self, numPoints, radius):
		# store the number of points and radius
		self.numPoints = numPoints
		self.radius = radius
 
	def describe(self, image, eps=1e-7):
		# compute the Local Binary Pattern representation of the image, and then
		# use the LBP representation to build the histogram of patterns
		lbp = feature.local_binary_pattern(image, self.numPoints, self.radius, method="uniform")
		(hist, _) = np.histogram(lbp.ravel(), bins=range(0, self.numPoints + 3),
			range=(0, self.numPoints + 2))
 
		# normalize the histogram
		hist = hist.astype("float")
		hist /= (hist.sum() + eps)
 
		# return the histogram of Local Binary Patterns
		return hist
def dump_dataset(data, labels, path, datasetName, writeMethod="w"):
    # open the database, create the dataset, write the data and labels to dataset,
    # and then close the database
    db = h5py.File(path, writeMethod)
    dataset = db.create_dataset(datasetName, (len(data), len(data[0]) + 1), dtype="float")
    dataset[0:len(data)] = np.c_[labels, data]
    db.close()

def load_dataset(path, datasetName):
    # open the database, grab the labels and data, then close the dataset
    db = h5py.File(path, "r")
    (labels, data) = (db[datasetName][:, 0], db[datasetName][:, 1:])
    db.close()
 
    # return a tuple of the data and labels
    return (data, labels)


# load the image image, convert it to grayscale, and detect edges
template = cv2.imread(args["path"]+'bioswale_model'+'.png')
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]



for imagePath in glob.glob(args["images"] + "/*.jpg"):
	# load the image, convert it to grayscale, and initialize the
	# bookkeeping variable to keep track of the matched region
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	found = None

	# loop over the scales of the image
	for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		# resize the image according to the scale, and keep track
		# of the ratio of the resizing
		resized = helpers.resize(gray, width = int(gray.shape[1] * scale))
		r = gray.shape[1] / float(resized.shape[1])

		# if the resized image is smaller than the template, then break
		# from the loop
		if resized.shape[0] < tH or resized.shape[1] < tW:
			break


		edged = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

		# check to see if the iteration should be visualized
		if args.get("visualize", False):
			# draw a bounding box around the detected region
			clone = np.dstack([edged, edged, edged])
			cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
				(maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
			cv2.imshow("Visualize", clone)
			cv2.waitKey(0)

	
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)


	(_, maxLoc, r) = found
	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

	# draw a bounding box around the detected result and display the image
	cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
	cv2.imshow("Image", image)
	cv2.waitKey(0)
