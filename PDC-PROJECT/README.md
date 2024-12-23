### COMMANDS TO RUN when in the same directory as the MakeFile:

  - run `make` to build the project
  - run `make run` to run the project, or build and run if the project has not been built yet
  - run `make clean` to delete build and bin folders

- Add document_files folder in the root folder with a file named test.txt with the target data:

* document_files folder will contain:
  - test.txt
  - tf-idf-chunks folder 
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
    


  * COMPILE AND RUN mpi-idf-calculation.cpp
   `mpicxx MPI-findTopKMostSimilarDocs.cpp -o MPI-findTopKMostSimilarDocs.exe && mpirun -np 4 --oversubscribe MPI-findTopKMostSimilarDocs.exe && rm MPI-findTopKMostSimilarDocs.exe`

    /// * If you generate embeddings for x threads then the cosine similarity
  /// search should also be with x threads