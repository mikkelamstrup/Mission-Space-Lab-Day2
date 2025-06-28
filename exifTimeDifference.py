"""
Solution for Task 3 of the "Mission Space Lab" project day 2,
a project developed by the Raspberry Pi Foundation and ESA Education.
This task and solution were created by Mikkel Amstrup Brandt Neiiendam.

Task Description:
1. Extract the "datetime_original" EXIF tag from two image files.
2. Convert the extracted EXIF datetime string to Python datetime objects.
3. Print the timestamps of both images.
4. Calculate and print the time difference between the two images.
"""

from exif import Image  # Import the Image class from the exif module for handling EXIF data
from datetime import datetime  # Import datetime to parse EXIF time strings and calculate differences

def get_time(image):
    """
    Opens the specified image file in binary mode, extracts its EXIF "datetime_original" data,
    converts the time string to a datetime object, and returns the datetime.

    :param image: The file path to the image
    :return: A datetime object representing the image's original timestamp
    """
    # Open the image file in binary read mode
    with open(image, 'rb') as image_file:
        # Create an Image object to access its EXIF metadata
        img = Image(image_file)
        # Retrieve the EXIF "datetime_original" tag as a string
        timeStr = img.get("datetime_original")
        # Convert the EXIF time string to a Python datetime object using the appropriate format
        time = datetime.strptime(timeStr, '%Y:%m:%d %H:%M:%S')
    return time

# Print the timestamp for the first image
print("Tidspunkt for billede 1:")
print(get_time('Path to image'))

# Print the timestamp for the second image
print("Tidspunkt for billede 2:")
print(get_time('Path to image'))

def get_time_difference(image1, image2):
    """
    Calculates the time difference between two images based on their EXIF "datetime_original" timestamps.
    It prints and returns the difference as a timedelta object.

    :param image1: The file path to the first image
    :param image2: The file path to the second image
    :return: A timedelta object representing the time difference between the two images
    """
    # Retrieve the timestamp for the first image
    time1 = get_time(image1)
    # Retrieve the timestamp for the second image
    time2 = get_time(image2)
    # Calculate the time difference between the two timestamps
    time_difference = time2 - time1 
    # Print the calculated time difference
    print(f"Tidsforskellen er: {time_difference}")
    return time_difference

# Calculate and print the time difference between the two specified images
get_time_difference(
    'Path to image',
    'Path to image'
)
