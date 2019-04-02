# Image-Processing-Pipeline

## A pipeline to deliver imagery to an image processing model

#### 1.An image processing pipeline. This pipeline prepares raw jpegs for input into a machine learning model. The model takes in an input of dimension (224, 224, 3) by default
#### 2. The basic pipeline with image augmentation techniques.
#### 3. Map the locations of the images on a world map if the images contain exif information

### Setup
1) pip install virtualenv
2) virtualenv project_venv
3) cd project_venv\Scripts(For macbooks- cd project_env/bin)
4) activate
5) cd ..
6) cd ..
7) pip install -r requirements.txt
8) cd code
9) python .\GeoSpatialVisualizer.py(For macbooks- python GeoSpatialVisualizer.py)
10) python .\ImageProcessingPipeline.py(For macbooks- python ImageProcessingPipeline.py). Three
optional arguments width(int), height(int), and a threshold(float). E.g. python
.\ImageProcessingPipeline.py 228 228 0.3
11) python .\ImageAugmentationPipeline.py(For macbooks- python ImageAugmentationPipeline.py)

### Code Documentation

#### The following external python packages were used-
1)	virtualenv- To create a python virtual environment
2)	numpy- For matrix manipulations
3)	Pillow- This is a PIL fork. PIL is the Python Imaging Library by Fredrik Lundh and Contributors.
4)	Exifread- To read the Exif of an image
5)	Folium- To visualize geolocation data on a map
6)	Wand- Used for image augmentations from the python file

#### 4 Python files are made
1)	GeoSpatialVisualizer.py- Used to visualize geolocation data. This reads the Exifs of all the images. A marker with info icon (info icon used to indicate marker is clickable. On clicking on it we get the landscape type). All icons are mapped by a different color. Colors will be repeated if there are more than 10 unique image labels.  
2)	ImageExtractor.py- Has utility method to map a list of images to a crop type depending upon the folder name. The other utility method is to create the folder for transformed images if it doesn't exist and get the path to that folder.
3)	ImageProcessingPipeline.py- Creates the basic pipeline to transform the images. This takes 3 optional arguments- width, height, threshold. The default values are 224, 224, and 0.2. The width and height are the dimensions of the desired resized images. The file re-sizes the image, by getting it’s numpy matrix. It does the same to all the images. The dimension of each image is width X height. First, the smaller dimension is found, then image slices are made along the longer dimension with that size, so we get square images with each side being equal to the smaller dimension. Let the smaller dimension be dim. In case, the longer dimension is not an exact multiple of the smaller dimension, we will be left with a remainder matrix. Now if the ratio of the remaining matrix is greater than the threshold, we take an extra slice from the end of the larger dimension of the original image array having dimensions dim x dim. 
e.g. 1. Input array size – (220, 224). So, one image will be of size (220, 220). Now 4 / 220 = 0.018 < 0.2. Hence, the output will be only 1 image of size (224, 224). We get this by resizing the (220, 220) image we got from the previous step. 
e.g. 2. Input array size – (220, 330). So, one image will be of size (220, 220). Now 110 / 220 = 0.5 > 0.2. Hence, we will get one more image having the size (220, 220). The first image takes the slice [0:220, 0:220] while the second one takes the slice [0:220, 110:330]. These two slices are taken from the original image matrix. After re-sizing, the output will be 2 images, each having size (224, 224). 
Once all the images are resized, they are stored on the hard drive in the “imgs_converted” directory. This directory is at the same level as the original image directory. 
4)	ImageAugmentationPipeline.py- Extends the basic pipeline with image augmentation techniques. It picks all the images from the “imgs_converted” directory. For every image it performs the following 10 augmentations) 
a.	Vertical mirror image- If the image we get has been vertically inverted.
b.	Horizontal mirror image- The image might be clicked from the front or the back camera. The same information captured by the two cameras are horizontal mirror images of each other. 
c.	Translation by 20 pixels to right- Shifts the content of the image to right by 20 pixels. 
d.	Translation by 20 pixels to left- Shifts the content of the image to left by 20 pixels.
e.	Translation by 20 pixels to up- Up shifts the content of the image by 20 pixels.
f.	Translation by 20 pixels to down- Down shifts the content of the image by 20 pixels.
g.	Blurring each pixel with a radius of 2 pixel not including the center pixel with a standard deviation of 1 pixel- This will take care of the camera quality. If the camera quality is not too good, we might get blurred images. 
h.	900 rotation- The angle of 90 is chosen as all the images are square, so the concept of portrait/ landscape will be handled by this. 
i.	 Random noise is added to every pixel- To get images that might not be of high quality. 
j.	Image is center cropped to half the original dimensions. This cropped image is then resized to original dimensions. This will take care of the cases where an image would be zoomed in.


Once all the images are augmented/ transformed, they are stored on the hard drive, added to
the “imgs_converted” directory. This directory is at the same level as the original image
directory.
