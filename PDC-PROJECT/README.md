COMMANDS TO RUN when in the same directory as the MakeFile:
-make //build the project
-make run //run the project, or build and run if the project has not been built yet
-make clean //delete build and bin folders

FOLDER STRUCTURE
project/
├── src/
│ ├── main.cpp
│ ├── module1/
│ │ ├── file1.cpp
│ │ ├── file1.h
│ └── module2/
│ ├── file2.cpp
│ ├── file2.h
├── build/ # Directory for object files
└── bin/ # Directory for the final executable
