#include "calculateIDF.hpp"
#include "createIDFMapping.hpp"
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <omp.h>
#include <string>
#include <vector>

std::map<std::string, double>
mergeMaps(const std::vector<std::map<std::string, double>> &local_idfs) {
  std::map<std::string, double> mergedMap;

  for (const auto &currentMap : local_idfs) {
    for (const auto &pair : currentMap) {
      mergedMap[pair.first] +=
          pair.second; // Add value to existing key or insert new key
    }
  }

  return mergedMap;
}

std::map<std::string, double> calculateIDF(const std::string &test_file_path,
                                           int numThreads) {
  std::cout << "Calculating IDF........" << std::endl;
  std::map<std::string, double> idf;

  // Open the file to get its size
  std::fstream inFile(test_file_path, std::ios::in | std::ios::ate);
  if (!inFile) {
    std::cout << "Error opening file" << std::endl;
    return idf;
  }
  long fileSize = inFile.tellg();
  inFile.close();

  // Calculate the size of the chunks each thread will handle
  long chunkSize = fileSize / numThreads;

  // Set the number of threads for OpenMP
  omp_set_num_threads(numThreads);

  int total_sentence_count = 0;
  std::vector<std::map<std::string, double>> local_idfs(numThreads);

// Parallelize the file reading using OpenMP
#pragma omp parallel reduction(+ : total_sentence_count)
  {
    int threadID = omp_get_thread_num();
    long start = threadID * chunkSize;
    long end =
        (threadID == numThreads - 1) ? fileSize : (threadID + 1) * chunkSize;

    total_sentence_count +=
        createIDFMapping(test_file_path, local_idfs[threadID], start, end);
  }
  idf = mergeMaps(local_idfs);
  /// IDF calculation
  for (const auto &word : idf) {
    idf[word.first] = log((double)total_sentence_count / (1 + word.second));
    // adding one to prevent overly large IDF values for
    // rare words(for which word.second is 1 or any other low value)
  }
  return idf;
}