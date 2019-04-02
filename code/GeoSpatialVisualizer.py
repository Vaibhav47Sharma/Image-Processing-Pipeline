# To get a dict of images
from ImageExtractor import ImageExtractor

# To get the Exif of image
import exifread as ef

# To create map
import folium

# To open HTML of map after creating it
import webbrowser, os


class GeoSpatialVisualizer:

  # based on https://gist.github.com/erans/983821
  @classmethod
  def convert_to_degress(cls, value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

  @classmethod
  def get_gps(cls, filepath):
    '''
    returns gps data if present other wise returns empty dictionary
    '''
    with open(filepath, 'rb') as f:
      tags = ef.process_file(f)
      latitude = tags.get('GPS GPSLatitude')
      latitude_ref = tags.get('GPS GPSLatitudeRef')
      longitude = tags.get('GPS GPSLongitude')
      longitude_ref = tags.get('GPS GPSLongitudeRef')
      if latitude:
        lat_value = GeoSpatialVisualizer.convert_to_degress(latitude)
        if latitude_ref.values != 'N':
          lat_value = -lat_value
      else:
        return {}
      if longitude:
        lon_value = GeoSpatialVisualizer.convert_to_degress(longitude)
        if longitude_ref.values != 'E':
          lon_value = -lon_value
      else:
        return {}
      return {'latitude': lat_value, 'longitude': lon_value}
    return {}

  def make_geospatial_visualization(self):
    # Dict of list of images
    img_dict = ImageExtractor().get_image_dict('imgs_de')

    # Will store data in the format((latitude, longitude), landscape_name)
    landscape_loc_tuple_list = []

    # To find the initial center of map
    center_latitude = 0
    center_longitude = 0

    for landscape, landscape_list in img_dict.items():
      for landscape_img in landscape_list:
        gps_info = GeoSpatialVisualizer.get_gps(landscape_img)
        if 'latitude' in gps_info.keys() and 'longitude' in gps_info.keys():
          latitude = gps_info['latitude']
          longitude = gps_info['longitude']

          center_longitude += longitude
          center_latitude += latitude

          landscape_loc_tuple_list.append(((latitude, longitude), landscape))

    if len(landscape_loc_tuple_list) == 0:
      return 'No exif data available in the images'
    # Creating landscape map with center as the average of latitude and  longitude
    center_latitude = center_latitude / len(landscape_loc_tuple_list)
    center_longitude = center_longitude / len(landscape_loc_tuple_list)
    landscape_map = folium.Map(location=[center_latitude, center_longitude], zoom_start=4)

    """
    Making color list
    I chose 10 different colors
    """
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen']

    # Placing markers
    for i in range(0, len(landscape_loc_tuple_list)):
      coordinates, landscape_name = landscape_loc_tuple_list[i]
      folium.Marker(
        location=[coordinates[0], coordinates[1]],
        popup=landscape_name,
        icon=folium.Icon(color=colors[list(img_dict.keys()).index(landscape_name)], icon='info-sign') #index of landscape name in the landscape lists, giving info-sign as icon to indicate its clickable
      ).add_to(landscape_map)

    landscape_map_html_name = 'landscape_map.html'
    landscape_map.save(landscape_map_html_name)

    webbrowser.open(os.path.join('file:', os.path.realpath(landscape_map_html_name)))
    return os.path.realpath(landscape_map_html_name)


if __name__ == "__main__":
  print('Making visualization on HTML')
  visualization_path = GeoSpatialVisualizer().make_geospatial_visualization()
  print('HTML saved at')
  print(visualization_path)