from exif import Image  # Import the Image class from the exif module to work with EXIF data

def get_data(image):
    # Open the image file in binary read mode
    with open(image, 'rb') as image_file:
        # Create an Image object from the file to access its EXIF metadata
        img = Image(image_file)
        
        # Loop through all EXIF tags available in the image and print each tag
        for data in img.list_all():
            print(data)

# Call the get_data function with the specified image path
get_data('Path to image')
