"""
Solution for Task 1 of the "Mission Space Lab" project day 2,
a project developed by the Raspberry Pi Foundation and ESA Education.
This task and solution were created by Mikkel Amstrup Brandt Neiiendam,
educator and certified ESA Education mentor.

Task Description:
The program must:
1. Open a specified image file in binary mode.
2. Extract the image's EXIF metadata.
3. Print all available EXIF tags to the console.

Usage:
Simply run the program to display all EXIF tags contained in the provided image.
"""

from exif import Image  # Import the Image class from the exif module to work with EXIF data

def get_data(image):
    """
    Opens the specified image file in binary mode, extracts its EXIF data,
    and prints out all available EXIF tags.
    
    :param image: The file path to the image
    """
    # Open the image file in binary read mode
    with open(image, 'rb') as image_file:
        # Create an Image object from the file to access its EXIF metadata
        img = Image(image_file)
        
        # Loop through all EXIF tags available in the image and print each tag
        for data in img.list_all():
            print(data)

# Call the get_data function with the specified image path
get_data('/Users/mikkel/desktop/efterskole/astropi-iss-speed-en-resources/photo_0677.jpg')
