import streamlit as st
import math


def closest_pair(points):
    """
    calls the _closest_pair function which calls itself recursively to find the closest pair of points.
    """
    if not points:
        return None

    return _closest_pair(sorted(points, key=lambda x: x[0]))


def _closest_pair(points):
    """
    Parameters:
    points (list): A sorted list of 2D points, where each point is represented as a list [x, y].

    Returns:
    tuple: A tuple containing the two closest points.
    """
    if len(points) <= 3:
        return brute_force(points)

    mid = len(points) // 2
    left_points = points[:mid]
    right_points = points[mid:]

    # Recursively find the closest pair in the left and right halves
    left_closest = _closest_pair(left_points)
    right_closest = _closest_pair(right_points)

    # Find the closest pair across the middle line
    min_distance = min(dist(left_closest[0], left_closest[1]), dist(
        right_closest[0], right_closest[1]))
    strip = [point for point in points if abs(
        point[0] - points[mid][0]) < min_distance]
    strip.sort(key=lambda x: x[1])

    closest_pair = left_closest if dist(left_closest[0], left_closest[1]) < dist(
        right_closest[0], right_closest[1]) else right_closest

    for i in range(len(strip)):
        for j in range(i + 1, min(i + 7, len(strip))):
            if dist(strip[i], strip[j]) < min_distance:
                closest_pair = (strip[i], strip[j])
                min_distance = dist(strip[i], strip[j])

    return closest_pair


def brute_force(points):
    """
    Find the closest pair of points using a brute-force approach.

    Parameters:
    points (list): A list of 2D points, where each point is represented as a list [x, y].

    Returns:
    tuple: A tuple containing the two closest points.
    """
    min_distance = float('inf')
    closest_pair = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = dist(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = (points[i], points[j])

    return closest_pair


def dist(p1, p2):
    """
    Calculate the distance between two 2D points.
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# GUI

# Title of the app
st.title("Closest pair of Points algorithm on 10 different input files containing 101 Coordinates each")

# File uploader widget with a limit of 10 files
uploaded_files = st.file_uploader(
    "Upload exactly 10 files with coordinates",
    type=["txt"],
    accept_multiple_files=True
)

# Initialize a 3D list to store the data
coordinate_data = []

# Check if the user uploaded exactly 10 files
if uploaded_files:
    if len(uploaded_files) != 10:
        st.error("Please upload exactly 10 files.")
    else:
        # Process each file
        all_files_valid = True  # Track if all files meet the criteria
        for file in uploaded_files:
            content = file.read().decode("utf-8").splitlines()

            # Check if the file has exactly 101 lines
            if len(content) < 101:
                st.error(
                    f"File '{file.name}' should have atleast 101 coordinates.")
                all_files_valid = False
                break

            # Parse each line to extract x and y coordinates
            file_coordinates = []
            for line in content:
                try:
                    x_str, y_str = line.split(",")
                    x, y = int(x_str), int(y_str)
                    file_coordinates.append([x, y])
                except ValueError:
                    st.error(f"File '{file.name}' contains invalid format.")
                    all_files_valid = False
                    break

            # Add the 2D array for this file to the 3D array if valid
            if all_files_valid:
                coordinate_data.append(file_coordinates)
            else:
                break

        # If all files are valid, convert to numpy array and display
        if all_files_valid:
            st.success("All files uploaded and processed successfully!")
            for i in range(len(coordinate_data)): #iterate over each file 
                # sort the coordinates on basis of x-axis
                coordinate_data[i] = sorted(
                    coordinate_data[i], key=lambda x: x[0])
                st.write("Coordinates of file ", i + 1)
                st.write(coordinate_data[i])
                st.write("Closest pair of points in file ", i + 1)
                st.write(closest_pair(coordinate_data[i]))  #find closest pair among the data of the current file
else:
    st.write("Please upload 10 files.")
