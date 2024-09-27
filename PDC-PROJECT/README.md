### COMMANDS TO RUN when in the same directory as the MakeFile:

    -make //build the project
    -make run //run the project, or build and run if the project has not been built yet
    -make clean //delete build and bin folders

- Add document_files folder in the root folder with a file named text.txt with the target data:

- document_files folder will contain:

  - test.txt
  - tf-idf-chunks folder (auto-generated)
  - idf.bin (auto-generated)

FOLDER STRUCTURE

    project/
    ├── src/
    │ ├── main.cpp
    │ ├── module1/
    │ │ ├── file1.cpp
    │ └── module2/
    │ ├── file2.cpp
    |── document_files/
    |── include/ #Directory for header files
    ├── build/ # Directory for object files
    └── bin/ # Directory for the final executable
