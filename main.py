"""
Solution for Task X of the "Mission Space Lab" project,
a project developed by the Raspberry Pi Foundation and ESA Education.
This task and solution were created by Mikkel Amstrup Brandt Neiiendam,
educator and certified ESA Education mentor.

Task Description:
The program must:
1. Extract the "datetime_original" EXIF tag from two images and compute the time difference in seconds.
2. Convert the images to grayscale OpenCV format.
3. Detect and compute ORB features (keypoints and descriptors) for both images.
4. Match the features between the two images using brute force matching with Hamming distance.
5. Calculate the average displacement (in pixels) between the matching keypoints.
6. Convert the average displacement into a speed (km/s) using a predefined conversion factor.
7. Write the calculated average speed (formatted with 5 significant figures) into a file named "result.txt",
   and print the speed to the console.

Usage:
Run the program to process the two specified images. The result (average speed in km/s) will be printed
to the console and saved in "result.txt".
"""

from exif import Image            # Import the Image class for EXIF data extraction
from datetime import datetime      # Import datetime for handling and parsing time information
import cv2                         # Import OpenCV for image processing and feature detection
import math                        # Import math for mathematical functions (e.g., square root)

def get_time(image_path):
    """
    Opens the specified image file in binary mode, extracts its EXIF "datetime_original" tag,
    converts the time string to a datetime object, and returns it.

    :param image_path: The file path to the image.
    :return: A datetime object representing the image's original timestamp.
    """
    with open(image_path, 'rb') as image_file:         # Open the image in binary mode
        img = Image(image_file)                         # Create an Image object to access its EXIF data
        timeStr = img.get("datetime_original")          # Retrieve the EXIF "datetime_original" as a string
        time_obj = datetime.strptime(timeStr, '%Y:%m:%d %H:%M:%S')  # Convert the string to a datetime object
    return time_obj

def get_time_difference(image1_path, image2_path):
    """
    Computes the time difference between two images using their EXIF "datetime_original" timestamps.

    :param image1_path: File path for the first image.
    :param image2_path: File path for the second image.
    :return: Time difference in seconds (integer).
    """
    time1 = get_time(image1_path)   # Get timestamp for the first image
    time2 = get_time(image2_path)   # Get timestamp for the second image
    time_difference = time2 - time1 # Compute the time difference
    return time_difference.seconds  # Return the difference in seconds

def convert_to_cv(image1_path, image2_path):
    """
    Converts the specified image files into OpenCV grayscale images.

    :param image1_path: File path for the first image.
    :param image2_path: File path for the second image.
    :return: A tuple containing the two grayscale images.
    """
    image1cv = cv2.imread(image1_path, 0)  # Load the first image in grayscale mode (flag = 0)
    image2cv = cv2.imread(image2_path, 0)  # Load the second image in grayscale mode
    return image1cv, image2cv

def calculate_features(image1, image2, featureNumber):
    """
    Detects and computes ORB features (keypoints and descriptors) for the two images.
    
    NOTE: This function uses the global variables 'image1cv' and 'image2cv' in place of its parameters.
          It is recommended to use the provided parameters for clarity.
    
    :param image1: First OpenCV grayscale image.
    :param image2: Second OpenCV grayscale image.
    :param featureNumber: Maximum number of features to detect.
    :return: A tuple containing keypoints and descriptors for both images.
    """
    orb = cv2.ORB_create(nfeatures=featureNumber)  # Initialize the ORB detector with the specified number of features
    # Detect and compute keypoints and descriptors for both images using ORB
    keypoints1, descriptors1 = orb.detectAndCompute(image1cv, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image2cv, None)
    return keypoints1, keypoints2, descriptors1, descriptors2

def calculate_matches(descriptors1, descriptors2):
    """
    Matches ORB descriptors between two images using a brute force matcher with Hamming distance.
    
    :param descriptors1: Descriptors from the first image.
    :param descriptors2: Descriptors from the second image.
    :return: A sorted list of matches (best matches first).
    """
    bruteForce = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # Create a BFMatcher with Hamming distance and cross-check enabled
    matches = bruteForce.match(descriptors1, descriptors2)          # Match descriptors between images
    matches = sorted(matches, key=lambda x: x.distance)               # Sort matches based on distance (lower distance is better)
    return matches

def display_matches(image1cv, keypoints1, image2cv, keypoints2, matches):
    """
    Draws and displays the matching keypoints between two images.
    
    :param image1cv: First OpenCV grayscale image.
    :param keypoints1: Keypoints detected in the first image.
    :param image2cv: Second OpenCV grayscale image.
    :param keypoints2: Keypoints detected in the second image.
    :param matches: List of matches between keypoints.
    """
    matchimg = cv2.drawMatches(image1cv, keypoints1, image2cv, keypoints2, matches, None)  # Draw matches between the images
    resize = cv2.resize(matchimg, (1600, 600), interpolation=cv2.INTER_AREA)              # Resize the output image for better display
    cv2.imshow('matches', resize)    # Display the image in a window titled 'matches'
    cv2.waitKey(0)                   # Wait indefinitely for a key press
    cv2.destroyAllWindows()          # Close all OpenCV windows

def find_matching_coordinates(keypoints1, keypoints2, matches):
    """
    Extracts the (x, y) coordinates of matching keypoints from both images.
    
    :param keypoints1: Keypoints from the first image.
    :param keypoints2: Keypoints from the second image.
    :param matches: List of matches between the keypoints.
    :return: Two lists containing the (x, y) coordinates for each matching keypoint in both images.
    """
    coordinates1 = []
    coordinates2 = []
    for match in matches:
        image1idx = match.queryIdx         # Index of the keypoint in the first image
        image2idx = match.trainIdx         # Index of the corresponding keypoint in the second image
        (x1, y1) = keypoints1[image1idx].pt  # Extract (x, y) coordinates from the first image's keypoint
        (x2, y2) = keypoints2[image2idx].pt  # Extract (x, y) coordinates from the second image's keypoint
        coordinates1.append((x1, y1))
        coordinates2.append((x2, y2))
    return coordinates1, coordinates2

# Define file paths for the images
image1_path = '/Users/mikkl/Desktop/Efterskole/i1gb2y/astropi-iss-speed-en-resources/photo_0677.jpg'
image2_path = '/Users/mikkl/Desktop/Efterskole/i1gb2y/astropi-iss-speed-en-resources/photo_0678.jpg'

# Calculate the time difference (in seconds) between the two images using their EXIF data
time_difference = get_time_difference(image1_path, image2_path)

# Convert the image files to OpenCV grayscale format
image1cv, image2cv = convert_to_cv(image1_path, image2_path)

# Detect and compute ORB features for both images, allowing up to 1000 features
keypoints1, keypoints2, descriptors1, descriptors2 = calculate_features(image1cv, image2cv, 1000)

# Match the descriptors between the two images
matches = calculate_matches(descriptors1, descriptors2)

# Optionally display the matching keypoints (uncomment the next line to view the matches)
# display_matches(image1cv, keypoints1, image2cv, keypoints2, matches)

# Extract the (x, y) coordinates from the matching keypoints in both images
coordinates1, coordinates2 = find_matching_coordinates(keypoints1, keypoints2, matches)

# Calculate the average displacement (in pixels) between the matching keypoints
displacements = []
for (x1, y1), (x2, y2) in zip(coordinates1, coordinates2):
    dx = x2 - x1                   # Difference in x-coordinate
    dy = y2 - y1                   # Difference in y-coordinate
    displacement = math.sqrt(dx**2 + dy**2)  # Euclidean distance between the keypoints
    displacements.append(displacement)

avg_disp_pixels = sum(displacements) / len(displacements)  # Average displacement in pixels

# Calculate the speed in pixels per second (ensure that time_difference is not zero)
speed_pixels_per_sec = avg_disp_pixels / time_difference if time_difference != 0 else 0

# Conversion factor from pixels to kilometers (adjust this factor based on calibration)
conversion_factor = 0.001  # Example: 0.001 km per pixel

# Calculate the average speed in km/s
avg_speed_km_s = speed_pixels_per_sec * conversion_factor

# Format the average speed to 5 significant figures
formatted_speed = format(avg_speed_km_s, '.5g')

# Write the result to "result.txt" with the formatted speed
with open("result.txt", "w") as f:
    f.write(f"Gennemsnitlig hastighed: {formatted_speed} km/s\n")

# Print the average speed to the console
print(f"{formatted_speed} km/s")
