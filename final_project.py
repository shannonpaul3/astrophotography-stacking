# Final Project - COMP 4102
# Shannon Paul
# 101178140

# ----------------------------------------------------------------
# This application takes a dataset of astrophotography photos. 
# Two steps are followed to produce a final image: 
# 	Step 1: Align Images 
# 	Step 2: Stack Images
# It exports a final image with an improved signal-to-noise ratio. 
#
# Note: this application takes between 6-7 mins to run
# -----------------------------------------------------------------

# import libraries
import numpy as np
import cv2
import glob

# read-in list of images
dataset = 'dataset/dataset_3/*.png'
images = [cv2.imread(file) for file in glob.glob(dataset)]

# define variables
align_img = []			# list of aligned images
base_img = images[0]	# image to use as base
images.pop(0)			# remove base image from list

# --------------------------------------------------------------------------------------------------------------------- #
# This function takes two photos and aligns them. 																		#
#																														#
# AutoAlign references the following ressource:																			#
# https://stackoverflow.com/questions/45162021/python-opencv-aligning-and-overlaying-multiple-images-one-after-another	#
# --------------------------------------------------------------------------------------------------------------------- #
def AutoAlign(base, curr):
	# convert to grayscale
	base_gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)

	# find the coordinates of good features to track  in base
	base_features = cv2.goodFeaturesToTrack(base_gray, 5000, .01, 10)

	# find corresponding features in current photo
	curr_features = np.array([])
	curr_features, pyr_stati, _ = cv2.calcOpticalFlowPyrLK(base, curr, base_features, curr_features, flags=1)

	# only add features for which a match was found to the pruned arrays
	base_features_pruned = []
	curr_features_pruned = []
	for index, status in enumerate(pyr_stati):
	    if status == 1:
	        base_features_pruned.append(base_features[index])
	        curr_features_pruned.append(curr_features[index])

	# convert lists to numpy arrays so they can be passed to opencv function
	bf_final = np.asarray(base_features_pruned)
	cf_final = np.asarray(curr_features_pruned)

	# find perspective transformation using the arrays of corresponding points
	transformation, hom_stati = cv2.findHomography(cf_final, bf_final, method=cv2.RANSAC, ransacReprojThreshold=1)

	height, width = curr.shape[:2]
	mod_photo = cv2.warpPerspective(curr, transformation, (width, height))
	return mod_photo

# ----------------------------------------------------------------- #
# This function takes two photos and applies a manual stack filter. #
# ----------------------------------------------------------------- #
def ManualStack(bg, mod, opacity):
	# blend modified photo at part opacity with bg photo at full opacity
	return cv2.addWeighted(bg, 1, mod, opacity, 0)

# ----------------------------------------------------------------------- #
# This function takes a list of photos and applies a median stack filter. #
# ----------------------------------------------------------------------- #
def MedianStack(photos):
	st_img = np.zeros_like(photos[0])
	# loop through each pxl
	for i in range(0, photos[0].shape[0]):
		for j in range(0, photos[0].shape[1]):

			colours = []	# list of rgb values of current pixel
			
			# rgb values for each picture
			for pic in photos:
				colours.append(pic[i, j])
			
			# calculate median rgb values
			med_pxl = np.median(colours, axis = 0)

			# convert to np.uint8
			st_img[i, j, 2] = np.uint8(med_pxl[2])	#R
			st_img[i, j, 1] = np.uint8(med_pxl[1])	#G
			st_img[i, j, 0] = np.uint8(med_pxl[0])	#B

	return st_img

# --------------------------------------------------------------------- #
# This function takes an image and returns a zoomed in version. 		#
# The amount zoomed in is determined by the zoom_factor.				#
# 																		#
# zoom_center references the following ressource:						#
# https://stackoverflow.com/questions/69050464/zoom-into-image-with-cv2	#
# --------------------------------------------------------------------- #
def zoom_center(img, zoom_factor=4):

    y_size = img.shape[0]
    x_size = img.shape[1]
    
    # define new boundaries
    x1 = int(0.5*x_size*(1-1/zoom_factor))
    x2 = int(x_size-0.5*x_size*(1-1/zoom_factor))
    y1 = int(0.5*y_size*(1-1/zoom_factor))
    y2 = int(y_size-0.5*y_size*(1-1/zoom_factor))

    # first crop image then scale
    img_cropped = img[y1:y2,x1:x2]
    return cv2.resize(img_cropped, None, fx=zoom_factor, fy=zoom_factor)


# Step 1: Align Images #

for curr_img in images:
	mod_img = AutoAlign(base_img, curr_img)
	align_img.append(mod_img)

# Step 2: Stack Images #

# Option 1: Manual Stack
stack = base_img
diff = 1/(len(images) + 1)	 # difference of opacity
opacity = round(1 - diff, 2)

# lower opacity of each layer
for curr_img in align_img:
	stack = ManualStack(stack, curr_img, opacity)
	opacity = round(opacity - diff, 2)

# Option 2: Median Stack
align_img.append(base_img)
med_stack = MedianStack(align_img)

# Step 3: Display Images #

# call zoom function
base_zoomed_and_cropped = zoom_center(base_img)		# zoom into base image
stack_zoomed_and_cropped = zoom_center(med_stack)	# zoom into median stack image

# concatenate images for noise comparison
multi1 = np.concatenate((base_img, base_zoomed_and_cropped), axis=1)
multi2 = np.concatenate((med_stack, stack_zoomed_and_cropped), axis=1)	
multi3 = np.concatenate((multi1, multi2), axis=0)

# display images
cv2.imshow('Noise Comparison - Before Stack vs After Stack', multi3)
cv2.imshow('Final Image - Median Stack', med_stack)

cv2.imwrite('result_image/compared.png', multi3)
cv2.imwrite('result_image/median_stack.png', med_stack)
cv2.imwrite('result_image/manual_stack.png', stack)

cv2.waitKey(0)
cv2.destroyAllWindows()
