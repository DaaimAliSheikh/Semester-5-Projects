#include "calculateTFIDF.hpp"
#include "createTFIDFMapping.hpp"

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <omp.h>
#include <string>
#include <vector>

using namespace std;

// Function to calculate TF-IDF for a document
void calculateTFIDF(const std::string &test_file_path,
                    std::map<std::string, double> &idf, int numThreads) {

  // Open the file to get its size
  std::fstream inFile(test_file_path, std::ios::in | std::ios::ate);
  if (!inFile) {
    std::cout << "Error opening tf-idf file" << std::endl;
    return;
  }
  long fileSize = inFile.tellg();
  inFile.close();

  // Calculate the size of the chunks each thread will handle
  long chunkSize = fileSize / numThreads;

  // Remove the old files
  std::cout << "Removing any old tf-idf chunks........" << std::endl;
  std::string directoryPath = "document_files/tf-idf-chunks/*.txt";
  std::string command = "rm -f " + directoryPath;
  system(command.c_str());

  // Parallelize the file reading using OpenMP
  std::cout << "Calculating TF-IDF vectors........" << std::endl;

#pragma omp parallel num_threads(numThreads)
  {
    int threadID = omp_get_thread_num();
    long start = threadID * chunkSize;
    long end =
        (threadID == numThreads - 1) ? fileSize : (threadID + 1) * chunkSize;

    createTFIDFMapping(test_file_path, idf, start, end);
  }
}