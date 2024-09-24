#include "loadIDFMap.hpp"
#include <fstream>
#include <iostream>
#include <map>
#include <string>

// Function to load map from a binary file
std::map<std::string, double> loadIDFMap(const std::string &filename) {
  std::ifstream inFile(filename, std::ios::binary);
  if (!inFile) {
    std::cerr << "Error opening file for reading." << std::endl;
    return {};
  }

  std::map<std::string, double> idf;
  size_t size;

  // Read the size of the map
  inFile.read(reinterpret_cast<char *>(&size), sizeof(size));

  // Read each pair from the file
  for (size_t i = 0; i < size; ++i) {
    // Read string size and content
    size_t strSize;
    inFile.read(reinterpret_cast<char *>(&strSize), sizeof(strSize));

    std::string key(strSize, '\0');
    inFile.read(&key[0], strSize);

    // Read the double value
    double value;
    inFile.read(reinterpret_cast<char *>(&value), sizeof(value));

    // Insert into map
    idf[key] = value;
  }

  inFile.close();
  return idf;
}
