# Mission Space Lab - EXIF and Image Processing Tasks

## Overview
This repository contains solutions to tasks for the "Mission Space Lab" project, developed by the Raspberry Pi Foundation 
and ESA Education. These tasks focus on working with image metadata (EXIF), time data, feature detection and matching using 
OpenCV, and performing calculations such as time differences and average speed based on image data.

The tasks and solutions were created by Mikkel Amstrup Brandt Neiiendam, educator and certified ESA Education mentor.

---

## Files and Descriptions

### **install requirements.txt**
**Description:**
- run this command in terminal
- pip install -r requirements.txt

### **1. exifData.py**
**Description:**
- This program opens a specified image file in binary mode, extracts its EXIF metadata, and prints all available EXIF tags.
- It is useful for inspecting the metadata stored within an image.

**Usage:**
1. Run the script.
2. The program will output all EXIF tags found in the image to the console.

---

### **2. exifTime.py**
**Description:**
- This program extracts the "datetime_original" EXIF tag from an image file.
- It converts the timestamp into a Python datetime object and prints the timestamp.

**Usage:**
1. Run the script.
2. The program will display the original timestamp of the image as recorded in its EXIF data.

---

### **3. exifTimeDifference.py**
**Description:**
- This program extracts the "datetime_original" timestamps from two image files.
- It calculates and prints the time difference between the two images in seconds.

**Usage:**
1. Run the script.
2. The program will display the time difference between the two images based on their EXIF timestamps.

---

### **4. orbMatches.py**
**Description:**
- This program converts two image files into grayscale and uses the ORB algorithm to detect features.
- It matches the detected features between the two images using a brute force matcher with Hamming distance.
- The matching keypoints are then displayed in a window.

**Usage:**
1. Run the script.
2. A window will open showing the matching keypoints between the two images.
3. Press any key to close the window.

---

### **5. orbCoordinates.py**
**Description:**
- This program detects and computes ORB features for two images and matches them.
- It then extracts the (x, y) coordinates of matching keypoints and prints the coordinates of the first matching pair from each image.

**Usage:**
1. Run the script.
2. The program will print the coordinates of the first matching keypoint pair from each image to the console.

---

### **6. speedCalculation.py**
**Description:**
- This program calculates the average displacement (in pixels) between matching keypoints of two images.
- It computes the speed in km/s by dividing the average displacement by the time difference (extracted from EXIF data) and applying a conversion factor.
- The average speed is saved in a file named `result.txt` and also printed to the console.

**Usage:**
1. Run the script.
2. The program will calculate the average speed and display it in the console.
3. The result is saved to `result.txt`, formatted to 5 significant figures.

---

### **7. main.py**
**Description:**
- This integrated program combines functionalities from the previous modules.
- It extracts EXIF timestamps, calculates time differences, performs ORB feature detection and matching, extracts matching coordinates, and computes the average speed.
- The program displays the matching keypoints, prints relevant data to the console, and saves the average speed to `result.txt`.

**Usage:**
1. Run the script.
2. Follow the on-screen prompts and instructions.
3. The program will perform the complete analysis, display the matching keypoints, and output the calculated average speed.
4. The final average speed is saved in `result.txt`.

---

## How to Run the Programs
1. Ensure Python 3.x is installed on your system.
2. Install the required libraries (`exif` and `opencv-python`).
3. Open a terminal or command prompt.
4. Navigate to the directory containing the scripts.
5. Run the desired script by typing `python <script_name>.py`.

---

## Notes
- Ensure the image files are available at the paths specified in the scripts.
- The programs are designed for educational purposes and demonstrate concepts such as EXIF data extraction, time manipulation, feature detection, and image processing using Python.
