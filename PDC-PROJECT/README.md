COMMANDS TO RUN when in the same directory as the MakeFile:
-make //build the project
-make run //run the project, or build and run if the project has not been built yet
-make clean //delete build and bin folders

PARALLELIZATION TO DO:

- parallelize the tokenization of each sentence in sentences(main.cpp)
- parallelize TFIDF generation of each document(main.cpp)
- parallelize file reading(getSentences.cpp)
- parallelize cosine_similarity search of inputTFIDF with each of the otehr IDFs in the for loop(main.cpp)
- try to parallelize the calculateIDF logarithm loop, divide the docCount array into chunks(calculateIDF.cpp)

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
|── include/ #Directory for header files
├── build/ # Directory for object files
└── bin/ # Directory for the final executable
