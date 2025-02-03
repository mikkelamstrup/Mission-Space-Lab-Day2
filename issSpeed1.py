from exif import Image

def get_data(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        for data in img.list_all():
            print(data)

get_data('/Users/mikkel/desktop/efterskole/astropi-iss-speed-en-resources/photo_0677.jpg')