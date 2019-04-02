"""
Assumes the image data is placed in the data directory.
This data directory is at the same level as the code directory.
|
|
|--- code
|--- data\imgs_de
"""

import os

class ImageExtractor:

  """
  Method to get images corresponding to the landscape
  Raises value error incase there are no images
  @:param folder_name from which all the images need to be extracted
  """
  def get_image_dict(self, folder_name):
    # Get the path of the code folder
    code_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(code_directory)

    # Get parent directory of code folder
    parent_dir = os.path.dirname(code_directory)

    image_dir = os.path.join(parent_dir, 'data', folder_name)

    landscape_folders = [x[0] for x in os.walk(image_dir) if x[0] != image_dir]


    # Specifying image extensions
    image_types = ['.jpg', '.jpeg']

    image_dict = dict()
    # Iterate over landscape folders
    for landscape in landscape_folders:

      for landscape_image in os.walk(landscape):
        # Getting the list of all the image files
        images = [x for x in landscape_image[2] if os.path.splitext(x)[1] in image_types]
        if len(images) > 0:
          # Add to dict only if there is more than zero images corresponding to a landscape
          # print(images[0])
          images = [os.path.join(landscape_image[0], x) for x in images]
          image_dict[os.path.basename(landscape)] = images

    if len(image_dict) < 1:
      raise ValueError('No images found')

    return image_dict

  def get_converted_image_path(self):
    # First creates the folder for converted images if it doesn't exist.
    # Then returns the path of this newly created folder. This folder will hold the transformed images.
    code_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(code_directory)

    # Get parent directory of code folder
    parent_dir = os.path.dirname(code_directory)

    image_dir = os.path.join(parent_dir, 'data', 'imgs_converted')

    try:
      os.makedirs(image_dir)
    except FileExistsError:
      # directory already exists
      pass

    return image_dir