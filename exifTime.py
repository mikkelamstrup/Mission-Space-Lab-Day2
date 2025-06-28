"""
Solution for Task 2 of the "Mission Space Lab" project day 2,
a project developed by the Raspberry Pi Foundation and ESA Education.
This task and solution were created by Mikkel Amstrup Brandt Neiiendam.

Task Description:
The program must:
1. Open two specified image files in binary mode.
2. Extract the EXIF metadata "datetime_original" from each image.
3. Convert the EXIF time string to a Python datetime object.
4. Print the timestamp for each image to the console.

Usage:
Run the program to display the datetime of each image as stored in the EXIF metadata.
"""

from exif import Image  # Import the Image class from the exif module to handle EXIF data
from datetime import datetime  # Import datetime to convert the EXIF time string into a datetime object

def get_time(image):
    """
    Opens the specified image file in binary mode, extracts its EXIF "datetime_original" data,
    converts the time string to a datetime object, and returns the datetime.

    :param image: The file path to the image
    :return: A datetime object representing the "datetime_original" EXIF tag
    """
    # Open the image file in binary read mode
    with open(image, 'rb') as image_file:
        # Create an Image object from the file to access its EXIF metadata
        img = Image(image_file)
        # Retrieve the EXIF "datetime_original" tag as a string
        timeStr = img.get("datetime_original")
        # Convert the time string to a datetime object using the specified format
        time = datetime.strptime(timeStr, '%Y:%m:%d %H:%M:%S')
    return time

# Print the timestamp for the first image
print("Tidspunkt for billede 1:")
print(get_time('Path to image'))

# Print the timestamp for the second image
print("Tidspunkt for billede 2:")
print(get_time('Path to image'))
