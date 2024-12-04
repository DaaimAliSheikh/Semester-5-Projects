import os
import random

# Set the number of files to create
num_files = 10

# Set the number of lines per file
lines_per_file = 101
dir_name = "karatsuba_sample_input_files"

# Create the directory to store the files
os.makedirs(dir_name, exist_ok=True)

for file_num in range(1, num_files + 1):
    filename = f"sample_input_{file_num}.txt"
    file_path = os.path.join(dir_name, filename)

    with open(file_path, "w") as file:
        for _ in range(lines_per_file):
            binary_int = "{0:08b}".format(random.randint(0, 255))
            file.write(f"{binary_int}\n")

print(f"Successfully created {num_files} text files with random 8-bit binary integers in the 'binary_files' directory.")