import streamlit as st


def karatsuba(x, y):
    """Multiplies two integers x and y using the Karatsuba algorithm."""
    # Base case for recursion (when numbers are small enough)
    if x < 10 or y < 10:
        return x * y

    # Calculate the size of the numbers
    n = max(x.bit_length(), y.bit_length())
    half = n // 2

    # Split x and y into high and low parts
    high_x = x >> half
    low_x = x - (high_x << half)
    high_y = y >> half
    low_y = y - (high_y << half)

    # Recursive steps
    z0 = karatsuba(low_x, low_y)
    z1 = karatsuba((low_x + high_x), (low_y + high_y))
    z2 = karatsuba(high_x, high_y)

    # Combine results
    return (z2 << (2 * half)) + ((z1 - z2 - z0) << half) + z0


# GUI

# Title of the app
st.title("Karatsuba Multiplication Algorithm for 10 sample input files containing atleast 101 8-bit binary integers each")

# File uploader widget with a limit of 10 files
uploaded_files = st.file_uploader(
    "Upload exactly 10 files with 8-bit binary entries",
    type=["txt"],
    accept_multiple_files=True
)

# Initialize a 2D list to store the binary strings, where each subarray represents a file
binary_data = []

# Check if the user uploaded exactly 10 files
if uploaded_files:
    if len(uploaded_files) != 10:
        st.error("Please upload exactly 10 files.")
    else:
        # Process each file
        all_files_valid = True  # Track if all files meet the criteria
        for file in uploaded_files:
            content = file.read().decode("utf-8").splitlines()

            # Check if the file has at least 101 lines
            if len(content) < 101:
                st.error(
                    f"File '{file.name}' does not have at least 101 lines.")
                all_files_valid = False
                break

            # Parse each line to check if it's a valid 8-bit binary string
            file_binary_data = []
            for line in content:
                if len(line) == 8 and all(c in '01' for c in line):
                    file_binary_data.append(line)
                else:
                    st.error(
                        f"File '{file.name}' contains an invalid binary format.")
                    all_files_valid = False
                    break

            # Add the list for this file to the 2D array if valid
            if all_files_valid:
                binary_data.append(file_binary_data)
            else:
                break

        if all_files_valid:
            st.success("All files uploaded and processed successfully!")
            for i in range(len(binary_data)):
                st.write("Data in File ", i + 1)
                st.write(binary_data[i])
                st.write("Multiplication Result for data in File ", i + 1)
                integers = [int(b, 2) for b in binary_data[i]]  # Convert binary strings to base 10 integers
                # Multiply all integers with each other using Karatsuba algorithm
                result = integers[0]
                for i in range(1, len(integers)):
                    result = karatsuba(result, integers[i])
                # Convert the result back to binary string (without the '0b' prefix))
                st.write(bin(result)[2:])
else:
    st.write("Please upload 10 files.")
