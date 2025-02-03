"""
Solution for Task 4 of the "Mission Space Lab" project day 2,
a project developed by the Raspberry Pi Foundation and ESA Education.
This task and solution were created by Mikkel Amstrup Brandt Neiiendam,
educator and certified ESA Education mentor.

Task Description:
The program must:
1. Extract the "datetime_original" EXIF tag from two images and calculate the time difference (in seconds).
2. Convert the two image files to grayscale OpenCV images.
3. Detect and compute ORB features (keypoints and descriptors) for both images.
4. Match the features between the two images using Brute Force matching with Hamming distance.
5. Print the list of feature matches.

Usage:
Run the program to process the two specified images and print the resulting matches.
"""

from exif import Image  # Import the Image class from the exif module for handling EXIF metadata
from datetime import datetime  # Import datetime for parsing EXIF time strings and calculating time differences
import cv2  # Import OpenCV for image processing and feature detection

def get_time(image):
    """
    Opens the specified image file in binary mode, extracts its EXIF "datetime_original" data,
    converts the time string to a datetime object, and returns the datetime.

    :param image: The file path to the image
    :return: A datetime object representing the image's original timestamp
    """
    with open(image, 'rb') as image_file:  # Open the image file in binary read mode
        img = Image(image_file)  # Create an Image object to access its EXIF data
        timeStr = img.get("datetime_original")  # Retrieve the "datetime_original" EXIF tag as a string
        time = datetime.strptime(timeStr, '%Y:%m:%d %H:%M:%S')  # Convert the string to a datetime object
    return time

def get_time_difference(image1, image2):
    """
    Calculates the time difference between two images based on their EXIF "datetime_original" timestamps.

    :param image1: File path for the first image
    :param image2: File path for the second image
    :return: The time difference in seconds as an integer
    """
    time1 = get_time(image1)  # Get timestamp for the first image
    time2 = get_time(image2)  # Get timestamp for the second image
    time_difference = time2 - time1  # Calculate the time difference
    return time_difference.seconds  # Return the difference in seconds

def convert_to_cv(image1, image2):
    """
    Converts two image files to OpenCV grayscale images.

    :param image1: File path for the first image
    :param image2: File path for the second image
    :return: A tuple containing the two grayscale images
    """
    image1cv = cv2.imread(image1, 0)  # Read the first image in grayscale mode
    image2cv = cv2.imread(image2, 0)  # Read the second image in grayscale mode
    return image1cv, image2cv

def calculate_features(image1, image2, featureNumber):
    """
    Detects and computes ORB features for two images.

    :param image1: First OpenCV image (grayscale)
    :param image2: Second OpenCV image (grayscale)
    :param featureNumber: Maximum number of features to detect
    :return: A tuple containing keypoints and descriptors for both images
    """
    orb = cv2.ORB_create(nfeatures=featureNumber)  # Create an ORB detector with the specified number of features
    keypoints1, descriptors1 = orb.detectAndCompute(image1, None)  # Detect and compute features for the first image
    keypoints2, descriptors2 = orb.detectAndCompute(image2, None)  # Detect and compute features for the second image
    return keypoints1, keypoints2, descriptors1, descriptors2

def calculate_matches(descriptors1, descriptors2):
    """
    Matches ORB descriptors between two images using Brute Force matching with Hamming distance.

    :param descriptors1: Descriptors from the first image
    :param descriptors2: Descriptors from the second image
    :return: A sorted list of matches based on descriptor distance
    """
    bruteForce = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # Create BFMatcher with Hamming distance and cross-check enabled
    matches = bruteForce.match(descriptors1, descriptors2)  # Match the descriptors between the two images
    matches = sorted(matches, key=lambda x: x.distance)  # Sort the matches based on distance (lower is better)
    return matches

# Define file paths for the two images
image1 = '/Users/mikkel/desktop/efterskole/astropi-iss-speed-en-resources/photo_0677.jpg'
image2 = '/Users/mikkel/desktop/efterskole/astropi-iss-speed-en-resources/photo_0678.jpg'

# Calculate the time difference between the two images (in seconds)
time_difference = get_time_difference(image1, image2)

# Convert the image files to grayscale OpenCV images
image1cv, image2cv = convert_to_cv(image1, image2)

# Calculate ORB features for both images using a maximum of 1000 features
keypoints1, keypoints2, descriptors1, descriptors2 = calculate_features(image1cv, image2cv, 1000)

# Calculate the matches between the two sets of descriptors
matches = calculate_matches(descriptors1, descriptors2)

# Print the list of matches
print(matches)
