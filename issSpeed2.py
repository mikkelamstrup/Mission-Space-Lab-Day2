from exif import Image
from datetime import datetime

def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        timeStr = img.get("datetime_original")
        time = datetime.strptime(timeStr, '%Y:%m:%d %H:%M:%S')
    return time

print("Tidspunkt for billede 1:")
print(get_time('/Users/mikkel/desktop/efterskole/astropi-iss-speed-en-resources/photo_0677.jpg'))
print("Tidspunkt for billede 2:")
print(get_time('/Users/mikkel/desktop/efterskole/astropi-iss-speed-en-resources/photo_0678.jpg'))
