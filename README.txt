Shannon Paul

to execute:
	python3 final_project.py

libraries:
	OpenCV
	glob2
	numpy

to install libraries (using pip):
	pip install opencv-python
	pip install glob2
	pip install numpy

source files:
	final_project.py

/result_image:
	This is where the final images will save.

Line 21 in source code dataset = 'dataset/dataset_1/*.png' 
may be adjusted to select one of the following datasets. 

/dataset/dataset_1:
	satr1.png
	stars2.png

/dataset/dataset_2:
	balcony1.png
	balcony2.png
	balcony3.png

/dataset/dataset_3:
	sample1.1.png
	sample1.2.png
	sample1.3.png
	sample1.4.png
	sample1.5.png

/dataset_3_ex_out:
	compared.png
	manual_stack.png
	median_stack.png

	This folder contains the example output when running the code
	with dataset_3

Documentation:
	Astrophotography and Image Stacking.pdf

Resources:

The function AutoAlign references code from: 
https://stackoverflow.com/questions/45162021/python-opencv-aligning-and-overlaying-multiple-images-one-after-another

The function AutoAlign references code from: 
https://stackoverflow.com/questions/69050464/zoom-into-image-with-cv2
