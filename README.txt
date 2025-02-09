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

example output:

![Test](https://raw.githubusercontent.com/shannonpaul3/astrophotography-stacking/main/output_example/before_and_after_stacking.jpg)

/result_image:
	This is where the final images will save.

***Line 21 in source code dataset = 'dataset/dataset_1/*.png' 
must be adjusted to point to a dataset.***

Dataset file structure can look like the following: 

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

Resources:

The function AutoAlign references code from: 
https://stackoverflow.com/questions/45162021/python-opencv-aligning-and-overlaying-multiple-images-one-after-another

The function AutoAlign references code from: 
https://stackoverflow.com/questions/69050464/zoom-into-image-with-cv2
