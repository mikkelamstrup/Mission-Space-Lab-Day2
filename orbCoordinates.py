"""
Solution for Task 3 of the "Mission Space Lab" project day 2,
a project developed by the Raspberry Pi Foundation and ESA Education.
This task and solution were created by Mikkel Amstrup Brandt Neiiendam.

Task Description:
The program must:
1. Extract the "datetime_original" EXIF tag from two image files and compute the time difference (in seconds).
2. Convert the two image files into grayscale images for OpenCV processing.
3. Detect and compute ORB features (keypoints and descriptors) for both images.
4. Match the ORB descriptors using a brute force matcher with Hamming distance.
5. Display the matching keypoints between the two images in a window.

Usage:
Run the program to process the two specified images. A window will open displaying the matching keypoints.
"""

from exif import Image            # Import the Image class from the exif module for EXIF data extraction
from datetime import datetime      # Import datetime for parsing EXIF time strings and computing time differences
import cv2                         # Import OpenCV for image processing, feature detection, and matching

def get_time(image):
    """
    Opens the specified image file in binary mode, extracts its EXIF "datetime_original" data,
    converts the time string to a datetime object, and returns it.

    :param image: The file path to the image.
    :return: A datetime object representing the image's original timestamp.
    """
    with open(image, 'rb') as image_file:           # Open the image file in binary read mode
        img = Image(image_file)                      # Create an Image object to access EXIF metadata
        timeStr = img.get("datetime_original")       # Retrieve the "datetime_original" EXIF tag as a string
        time = datetime.strptime(timeStr, '%Y:%m:%d %H:%M:%S')  # Convert the string to a datetime object
    return time

def get_time_difference(image1, image2):
    """
    Calculates the time difference between two images based on their EXIF "datetime_original" timestamps.

    :param image1: The file path for the first image.
    :param image2: The file path for the second image.
    :return: The time difference in seconds as an integer.
    """
    time1 = get_time(image1)   # Get the timestamp for the first image
    time2 = get_time(image2)   # Get the timestamp for the second image
    time_difference = time2 - time1   # Calculate the time difference
    return time_difference.seconds   # Return the difference in seconds

def convert_to_cv(image1, image2):
    """
    Converts the specified image files to OpenCV grayscale images.

    :param image1: The file path for the first image.
    :param image2: The file path for the second image.
    :return: A tuple containing the two grayscale images.
    """
    image1cv = cv2.imread(image1, 0)   # Load the first image in grayscale mode
    image2cv = cv2.imread(image2, 0)   # Load the second image in grayscale mode
    return image1cv, image2cv

def calculate_features(image1, image2, featureNumber):
    """
    Detects and computes ORB features for both images.

    :param image1: The first OpenCV grayscale image.
    :param image2: The second OpenCV grayscale image.
    :param featureNumber: Maximum number of features to detect.
    :return: A tuple containing keypoints and descriptors for both images.
    """
    orb = cv2.ORB_create(nfeatures=featureNumber)   # Create an ORB detector with the specified number of features
    # Use the provided images (image1 and image2) for feature detection
    keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image2, None)
    return keypoints1, keypoints2, descriptors1, descriptors2

def calculate_matches(descriptors1, descriptors2):
    """
    Matches ORB descriptors between two images using a brute force matcher with Hamming distance.

    :param descriptors1: Descriptors from the first image.
    :param descriptors2: Descriptors from the second image.
    :return: A sorted list of matches based on the descriptor distance.
    """
    bruteForce = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # Initialize BFMatcher with Hamming distance and cross-check enabled
    matches = bruteForce.match(descriptors1, descriptors2)         # Match descriptors between the two images
    matches = sorted(matches, key=lambda x: x.distance)              # Sort matches by distance (lower distance indicates better match)
    return matches

# Define file paths for the two images
image1 = 'Path to image'
image2 = 'Path to image'

def display_matches(image1cv, keypoints1, image2cv, keypoints2, matches):
    """
    Draws and displays the matching keypoints between two images.

    :param image1cv: The first OpenCV grayscale image.
    :param keypoints1: Keypoints from the first image.
    :param image2cv: The second OpenCV grayscale image.
    :param keypoints2: Keypoints from the second image.
    :param matches: A list of matches between the keypoints.
    """
    # Draw the matches between the two images
    matchimg = cv2.drawMatches(image1cv, keypoints1, image2cv, keypoints2, matches, None)
    # Resize the resulting image for better display (e.g., 1600x600 pixels)
    resize = cv2.resize(matchimg, (1600, 600), interpolation=cv2.INTER_AREA)
    cv2.imshow('matches', resize)   # Display the image in a window titled 'matches'
    cv2.waitKey(0)                  # Wait indefinitely for a key press
    cv2.destroyWindow('matches')    # Close the 'matches' window

# Calculate the time difference between the two images (in seconds)
time_difference = get_time_difference(image1, image2)

# Convert the image files to OpenCV grayscale images
image1cv, image2cv = convert_to_cv(image1, image2)

# Detect and compute ORB features for both images (up to 1000 features)
keypoints1, keypoints2, descriptors1, descriptors2 = calculate_features(image1cv, image2cv, 1000)

# Match the descriptors between the two images
matches = calculate_matches(descriptors1, descriptors2)

# Display the matching keypoints between the two images
display_matches(image1cv, keypoints1, image2cv, keypoints2, matches)
