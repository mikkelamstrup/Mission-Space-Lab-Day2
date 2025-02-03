from exif import Image
from datetime import datetime
import cv2


def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        timeStr = img.get("datetime_original")
        time = datetime.strptime(timeStr, '%Y:%m:%d %H:%M:%S')
    return time

def get_time_difference(image1,image2):
    time1 = get_time(image1)
    time2 = get_time(image2)
    time_difference = time2 - time1 
    return time_difference.seconds

def convert_to_cv(image1, image2):
    image1cv = cv2.imread(image1, 0)
    image2cv = cv2.imread(image2, 0)
    return image1cv, image2cv

def calculate_features(image1, image2, featureNumber):
    orb = cv2.ORB_create(nfeatures=featureNumber) 
    keypoints1, descriptors1 = orb.detectAndCompute(image1cv, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image2cv, None)
    return keypoints1,keypoints2, descriptors1, descriptors2

def calculate_matches(descriptors1, descriptors2):
    bruteForce = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bruteForce.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

image1 = '/Users/mikkel/desktop/efterskole/astropi-iss-speed-en-resources/photo_0677.jpg'
image2 = '/Users/mikkel/desktop/efterskole/astropi-iss-speed-en-resources/photo_0678.jpg'

def display_matches(image1cv, keypoints1, image2cv, keypoints2, matches):
    matchimg = cv2.drawMatches(image1cv, keypoints1, image2cv, keypoints2, matches, None)
    resize = cv2.resize(matchimg, (1600, 600), interpolation = cv2.INTER_AREA)
    cv2.imshow('matches', resize)
    cv2.waitKey(0)
    cv2.destroyWindow('matches')

time_difference = get_time_difference(image1, image2) 
image1cv, image2cv = convert_to_cv(image1, image2) 
keypoints1, keypoints2, descriptors1, descriptors2 = calculate_features(image1cv, image2cv, 1000) 
matches = calculate_matches(descriptors1, descriptors2) 
display_matches(image1cv, keypoints1, image2cv, keypoints2, matches)