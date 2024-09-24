#include "saveIDFMap.hpp"
#include <fstream>
#include <iostream>
#include <map>
#include <string>

void saveIDFMap(const std::map<std::string, double> &idf,
                const std::string &filename) {
  // Create file or open and overwrite new data if file exists
  std::ofstream outFile(filename, std::ios::binary);
  if (!outFile) {
    std::cerr << "Error opening file for writing." << std::endl;
    return;
  }

  std::cout << "Writing IDF map to file idf.bin..." << std::endl;
  // Write the size of the map first

  size_t size = idf.size();
  outFile.write(reinterpret_cast<const char *>(&size), sizeof(size));

  // Write each pair of the map
  for (const auto &pair : idf) {
    // Write string size and content
    size_t strSize = pair.first.size();
    outFile.write(reinterpret_cast<const char *>(&strSize), sizeof(strSize));
    outFile.write(pair.first.data(), strSize);

    // Write the double value
    outFile.write(reinterpret_cast<const char *>(&pair.second),
                  sizeof(pair.second));
  }

  outFile.close();
}