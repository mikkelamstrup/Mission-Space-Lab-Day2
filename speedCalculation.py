"""
Solution for Task X of the "Mission Space Lab" project,
a project developed by the Raspberry Pi Foundation and ESA Education.
This task and solution were created by Mikkel Amstrup Brandt Neiiendam.

Task Description:
The program must:
1. Extract the "datetime_original" EXIF tag from two images and compute the time difference in seconds.
2. Convert the image files to grayscale images for OpenCV processing.
3. Detect and compute ORB features (keypoints and descriptors) for both images.
4. Match the ORB descriptors between the two images using a brute force matcher with Hamming distance.
5. Extract the (x, y) coordinates of matching keypoints from both images.
6. Print the coordinates of the first matching keypoint pair from each image.

Usage:
Run the program to process the two specified images. The coordinates of the first matching keypoint pair will be printed.
"""

from exif import Image          # Import the Image class to work with EXIF data
from datetime import datetime    # Import datetime to parse EXIF time strings and compute time differences
import cv2                       # Import OpenCV for image processing and feature detection

def get_time(image):
    """
    Opens the specified image file in binary mode, extracts its EXIF "datetime_original" tag,
    converts the time string to a datetime object, and returns it.

    :param image: The file path to the image.
    :return: A datetime object representing the image's original timestamp.
    """
    with open(image, 'rb') as image_file:          # Open the image file in binary read mode
        img = Image(image_file)                     # Create an Image object to access its EXIF data
        timeStr = img.get("datetime_original")      # Retrieve the EXIF "datetime_original" tag as a string
        time = datetime.strptime(timeStr, '%Y:%m:%d %H:%M:%S')  # Convert the time string to a datetime object
    return time

def get_time_difference(image1, image2):
    """
    Calculates the time difference between two images based on their EXIF "datetime_original" timestamps.

    :param image1: File path for the first image.
    :param image2: File path for the second image.
    :return: The time difference in seconds as an integer.
    """
    time1 = get_time(image1)  # Get the timestamp for the first image
    time2 = get_time(image2)  # Get the timestamp for the second image
    time_difference = time2 - time1  # Compute the time difference between the two timestamps
    return time_difference.seconds  # Return the difference in seconds

def convert_to_cv(image1, image2):
    """
    Converts two image files to OpenCV grayscale images.

    :param image1: File path for the first image.
    :param image2: File path for the second image.
    :return: A tuple containing the two grayscale images.
    """
    image1cv = cv2.imread(image1, 0)  # Load the first image in grayscale mode
    image2cv = cv2.imread(image2, 0)  # Load the second image in grayscale mode
    return image1cv, image2cv

def calculate_features(image1, image2, featureNumber):
    """
    Detects and computes ORB features (keypoints and descriptors) for both images.

    :param image1: First OpenCV grayscale image.
    :param image2: Second OpenCV grayscale image.
    :param featureNumber: Maximum number of features to detect.
    :return: A tuple containing keypoints and descriptors for both images.
    """
    orb = cv2.ORB_create(nfeatures=featureNumber)  # Create an ORB detector with the specified number of features
    # Note: The code below uses the global variables image1cv and image2cv.
    # It is recommended to use the function parameters (image1 and image2) for clarity.
    keypoints1, descriptors1 = orb.detectAndCompute(image1cv, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image2cv, None)
    return keypoints1, keypoints2, descriptors1, descriptors2

def calculate_matches(descriptors1, descriptors2):
    """
    Matches ORB descriptors between two images using a brute force matcher with Hamming distance.

    :param descriptors1: Descriptors from the first image.
    :param descriptors2: Descriptors from the second image.
    :return: A sorted list of matches based on descriptor distance.
    """
    bruteForce = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # Initialize BFMatcher with Hamming distance and cross-check
    matches = bruteForce.match(descriptors1, descriptors2)          # Match the descriptors between the two images
    matches = sorted(matches, key=lambda x: x.distance)               # Sort matches by distance (lower is better)
    return matches

# Define file paths for the two images
image1 = 'Path to image'
image2 = 'Path to image'

def display_matches(image1cv, keypoints1, image2cv, keypoints2, matches):
    """
    Draws and displays the matching keypoints between two images.

    :param image1cv: First OpenCV grayscale image.
    :param keypoints1: Keypoints from the first image.
    :param image2cv: Second OpenCV grayscale image.
    :param keypoints2: Keypoints from the second image.
    :param matches: List of matches between the keypoints.
    """
    matchimg = cv2.drawMatches(image1cv, keypoints1, image2cv, keypoints2, matches, None)  # Draw matches between images
    resize = cv2.resize(matchimg, (1600, 600), interpolation=cv2.INTER_AREA)               # Resize the match image for display
    cv2.imshow('matches', resize)   # Display the resulting image in a window titled 'matches'
    cv2.waitKey(0)                  # Wait indefinitely until a key is pressed
    cv2.destroyWindow('matches')    # Close the 'matches' window

def find_matching_coordinates(keypoints1, keypoints2, matches):
    """
    Extracts the (x, y) coordinates of matching keypoints from both images.

    :param keypoints1: Keypoints from the first image.
    :param keypoints2: Keypoints from the second image.
    :param matches: List of matches between the keypoints.
    :return: Two lists containing (x, y) coordinates for each matching keypoint in both images.
    """
    coordinates1 = []
    coordinates2 = []
    for match in matches:
        image1idx = match.queryIdx  # Index of the keypoint in the first image
        image2idx = match.trainIdx  # Index of the keypoint in the second image
        (x1, y1) = keypoints1[image1idx].pt  # Extract coordinates from the first image keypoint
        (x2, y2) = keypoints2[image2idx].pt  # Extract coordinates from the second image keypoint
        coordinates1.append((x1, y1))
        coordinates2.append((x2, y2))
    return coordinates1, coordinates2

# Calculate the time difference between the two images (in seconds)
time_difference = get_time_difference(image1, image2)

# Convert the image files to OpenCV grayscale images
image1cv, image2cv = convert_to_cv(image1, image2)

# Detect and compute ORB features for both images (up to 1000 features)
keypoints1, keypoints2, descriptors1, descriptors2 = calculate_features(image1cv, image2cv, 1000)

# Match the descriptors between the two images
matches = calculate_matches(descriptors1, descriptors2)

# Extract the coordinates of the matching keypoints from both images
coordinates1, coordinates2 = find_matching_coordinates(keypoints1, keypoints2, matches)

# Print the coordinates of the first matching keypoint pair from each image
print(coordinates1[0], coordinates2[0])
