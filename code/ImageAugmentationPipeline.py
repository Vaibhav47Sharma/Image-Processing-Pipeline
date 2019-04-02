# To get a dict of images
from ImageExtractor import ImageExtractor
# For matrix operations on images
import numpy as np

import os
# To carry out image augmentations
from wand.image import Image

# Pillow is the friendly PIL fork by Alex Clark and Contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors.
from PIL import Image as PILImage, ImageFile

# Making PIL to be tolerant of files that are truncated
ImageFile.LOAD_TRUNCATED_IMAGES = True
class ImageAugmentationPipeline:
  @classmethod
  def get_landscape_transform(cls, image):
    # Crops the image by half from center and then resize it to original dimensions
    img = image.clone()
    width, height = img.size
    img = img[int(width/4): int(3/4*width), int(height/4): int(3/4*height)]
    img.resize(width, height)
    return PILImage.fromarray(np.asarray(img))

  @classmethod
  def get_flip_transformation(cls, image):
    # Verical mirror of the image
    img = image.clone()
    img.flip()
    return PILImage.fromarray(np.asarray(img))

  @classmethod
  def get_blur_transformation(cls, image):
    # Blur with radius 2, standard deviation 1
    img = image.clone()
    img.gaussian_blur(2,1)
    return PILImage.fromarray(np.asarray(img))

  @classmethod
  def get_flop_transformation(cls, image):
    # Horizontal mirror of the image
    img = image.clone()
    img.flip()
    return PILImage.fromarray(np.asarray(img))

  @classmethod
  def get_rotation_transformation(cls, image):
    # Rotates image bu 90 degrees
    img = image.clone()
    img.rotate(90)
    return PILImage.fromarray(np.asarray(img))

  @classmethod
  def get_translations_transformations(cls, image):
    # Returns a list of 4 images translated by 20 pixels- up, left, right, and down
    img = np.asarray(image)
    width, height, depth = img.shape

    up = np.zeros(shape=(width, height, depth))
    down = np.zeros(shape=(width, height, depth))
    left = np.zeros(shape=(width, height, depth))
    right = np.zeros(shape=(width, height, depth))

    # Shifting Up
    for j in range(width):
      for i in range(height):
        if (j < width - 20 and j > 20):
          up[j][i] = img[j + 20][i]
        else:
          up[j][i] = 0

    # Shifting Down
    for j in range(width):
      for i in range(height):
        if (j > 20):
          down[j][i] = img[j - 20][i]

    # Shifting Right
    for j in range(width):
      for i in range(height):
        if (i < height - 20):
          right[j][i] = img[j][i + 20]

    # Shifting Left
    for i in range(height, 1, -1):
      for j in range(width):
        if (i < height - 20):
          left[j][i] = img[j][i - 20]
        elif (i < height - 1):
          left[j][i] = 0

    return list((PILImage.fromarray(np.uint8(up)), PILImage.fromarray(np.uint8(left)), PILImage.fromarray(np.uint8(right)), PILImage.fromarray(np.uint8(down))))

  @classmethod
  def get_noise_transformations(cls, img):
    # Adds random noise to image
    img = np.asarray(img)
    width, height, depth = img.shape[0], img.shape[1], img.shape[2]

    noise = np.random.randint(5, size=(width, height, depth), dtype='uint8')

    for i in range(width):
      for j in range(height):
        for k in range(depth):
          # Used 8 bit numpy. Hence, require the below check to avoid overflow!
          if (img[i][j][k] <= 250):
            img[i][j][k] += noise[i][j][k]

    return PILImage.fromarray(np.uint8(img))


  @classmethod
  def get_all_image_transformations(cls, img):
    # Returns a list of all ten transformations
    transformed_image = [ImageAugmentationPipeline.get_landscape_transform(img), ImageAugmentationPipeline.get_flip_transformation(img),
                         ImageAugmentationPipeline.get_flop_transformation(img), ImageAugmentationPipeline.get_blur_transformation((img))]
    transformed_image.extend([ImageAugmentationPipeline.get_rotation_transformation(img), ImageAugmentationPipeline.get_noise_transformations(img)])
    transformed_image.extend(ImageAugmentationPipeline.get_translations_transformations(img))
    return transformed_image


  @classmethod
  def save_transformed_images(cls, original_image_path, transformed_image):
    # Saves the file transformations of image_file as image_file_T(0,1,2...).jpg
    img_path = original_image_path
    original_file = os.path.splitext(img_path)

    for i in range(len(transformed_image)):
      transformed_image[i].save(original_file[0] + '_T' + str(i) + original_file[1] + '.jpg', 'jpeg')


  def start_img_transformations(self):
    images_dict = ImageExtractor().get_image_dict('imgs_converted')
    for original_image_path_list in images_dict.values():
      for i in range(len(original_image_path_list)):
        original_image_path = original_image_path_list[i]
        img = Image(filename=original_image_path)
        transformations = ImageAugmentationPipeline.get_all_image_transformations(img)
        ImageAugmentationPipeline.save_transformed_images(original_image_path, transformations)

    return ImageExtractor().get_converted_image_path()





if __name__ == "__main__":
  print('Starting image augmentation pipeline')
  output_folder = ImageAugmentationPipeline().start_img_transformations()
  print('Finished the basic image processing pipeline. It is saved at-')
  print(output_folder)