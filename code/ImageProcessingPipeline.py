# To get a dict of images
from ImageExtractor import ImageExtractor

# For matrix operations
import numpy as np

# For ceil operation
import math

import os, sys

# Pillow is the friendly PIL fork by Alex Clark and Contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors.
from PIL import Image, ImageFile

# Making PIL to be tolerant of files that are truncated
ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageProcessingPipeline:
  """
  Re-sizes the image numpy matrix into a list of images. The dimension of each image is width X height.
  First finds the smaller dimension, then makes the image slices along the longer dimension with that size, so we get square images
  with each side being equal to the smaller dimension. Let the smaller dimension be dim.
  In case, the longer dimension is not an exact multiple of the smaller dimension, we will be left with a remainder matrix.
  Now if the ratio of the remaining matrix is greater than the threshold, we take an extra slice from the end of the
  larger dimension of the original image array having dimensions dim x dim.
  @:param imag_array The numpy matrix of input image
  @:param width of the output
  @:param height of the output
  @:param threshold(has to be less than 1)- if the the dimensions of last cut greater than the threshold, then only we take the "extra slice"
  """
  @classmethod
  def get_prepared_images(cls, img_array, width = 224, height = 224, threshold = 0.2):
    if threshold >= 1:
      raise ValueError('Threshold should be less than 1')
    in_width = img_array.shape[0]
    in_height = img_array.shape[1]

    # List of the images having dimensions width, height
    final_images = []

    # Image has a longer breadth
    if in_height < in_width:
      ratio = in_width / in_height
      for i in range(1, math.ceil(ratio)):
        final_images.append(img_array[(i - 1) * in_height: i * in_height, 0:in_height])

      # Take the extra slice
      if (ratio - int(ratio)) > threshold or in_width % in_height == 0:
        final_images.append(img_array[in_width - in_height: in_width, 0:in_height])

    else:
    # Image has a longer height or both the height and width are equal
      ratio = in_height / in_width
      for i in range(1, math.ceil(ratio)):
        final_images.append(img_array[0:in_width, (i - 1) * in_width: i * in_width])
      # Take the extra slice
      if (ratio - int(ratio)) > threshold or in_height % in_width == 0:
        final_images.append(img_array[0:in_width, in_height - in_width: in_height])

    final_images = [Image.fromarray(np.uint8(x)).resize((width, height)) for x in final_images]

    return final_images

  """
    This function saves the transfromed images after converting them into the desired
    height, and width
    @:param width of the output
    @:param height of the output
    @:param threshold(has to be less than 1)- if the the dimensions of last cut greater than the threshold, then only we take the extra slice
  """
  def store_prepared_images(self, width = 224, height = 224, threshold = 0.2):
    if threshold >= 1:
      raise ValueError('Threshold must lie between 0 and 1. Currently you have given it greater than or equal to 1')

    if threshold <= 0:
      raise ValueError('Threshold must lie between 0 and 1. Currently you have given it less than or equal to 0')

    # Dict of list of images
    img_dict = ImageExtractor().get_image_dict('imgs_de')

    # Dictionary of converted images into 3 channels(RGB)
    converted_images = dict()
    for landscape, landscape_list in img_dict.items():
      converted_images[landscape] = [Image.open(img).convert('RGB') for img in landscape_list]

    # Dictionary of finally reduced dimensions
    resized_images = dict()
    for landscape in list(converted_images.keys()):
      resized_images[landscape] = [ImageProcessingPipeline.get_prepared_images(np.asarray(x), width, height, threshold) for x in converted_images[landscape]]

    # Folder to store all the transformed images
    resized_images_folder = ImageExtractor().get_converted_image_path()

    for landscape_name in list(resized_images.keys()):
      image_dir = os.path.join(resized_images_folder, landscape_name)

      try:
        os.makedirs(image_dir)
      except FileExistsError:
        # directory already exists
        pass

      for i in range(0, len(resized_images[landscape_name])):

        for j in range(0, len(resized_images[landscape_name][i])):
          # Iterating over the converted images
          original_file = os.path.splitext(img_dict[landscape_name][i])
          file_name = os.path.basename(original_file[0]) + '_' + str(j) + original_file[1]
          file_full_path = os.path.join(image_dir, file_name)
          img = resized_images[landscape_name][i][j]
          img.save(file_full_path, 'jpeg')

    return resized_images_folder


if __name__ == "__main__":
  print('Beginning basic image processing pipeline')
  output_folder = ''
  if len(sys.argv) >= 4:
    output_folder = ImageProcessingPipeline().store_prepared_images(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
  elif len(sys.argv) == 3:
    output_folder = ImageProcessingPipeline().store_prepared_images(int(sys.argv[1]), int(sys.argv[2]))
  elif len(sys.argv) == 2:
    output_folder = ImageProcessingPipeline().store_prepared_images(int(sys.argv[1]))
  else:
    output_folder = ImageProcessingPipeline().store_prepared_images()

  print('Finished the basic image processing pipeline. It is saved at-')
  print(output_folder)