#include "getSentences.hpp"
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

std::string trim(const std::string &str) {
  const std::string whitespace = " \t\n\r\f\v";
  size_t start = str.find_first_not_of(whitespace);
  size_t end = str.find_last_not_of(whitespace);

  if (start == std::string::npos || end == std::string::npos) {
    return "";
  }

  return str.substr(start, end - start + 1);
}

// Function to return array of strings from a file
std::vector<std::string> getSentences(const std::string filepath) {
  std::vector<std::string> sentences;

  std::fstream inFile(filepath,
                      std::ios::in); // Open the file for reading

  if (!inFile) {
    std::cout << "Error opening file" << std::endl;
  }

  std::string sentence;
  char delimiter = '.';
  while (std::getline(inFile, sentence,
                      delimiter)) { // Read file up to delimiter '.'
    sentences.push_back(trim(sentence));
    sentence.clear(); // Clear the sentence for the next one
  }
  inFile.close(); // Close the file
  return sentences;
}