#include "createIDFMapping.hpp"
#include "tokenize.hpp"
#include <fstream>
#include <iostream>
#include <map>
#include <omp.h>
#include <set>
#include <string>
#include <vector>

// Helper function to trim whitespace
std::string trim2(const std::string &str) {
  size_t first = str.find_first_not_of(" \n\r\t\f\v");
  if (first == std::string::npos)
    return "";
  size_t last = str.find_last_not_of(" \n\r\t\f\v");
  return str.substr(first, last - first + 1);
}

// Adjust start position of a chunk to the next delimiter
void adjustToSentenceBoundary2(std::fstream &inFile, long &start) {
  if (start == 0) {
    // If start is the beginning of the file, don't adjust; start reading from
    // the beginning
    return;
  }

  inFile.seekg(start);

  char ch;
  while (inFile.get(ch)) {
    if (ch == '.') {
      // Move to the position just after the delimiter
      start = inFile.tellg();
      break;
    }
  }
}

// Function for reading and processing a part of the file
int createIDFMapping(const std::string &filepath,
                     std::map<std::string, double> &idf, long start, long end) {
  std::fstream inFile(filepath, std::ios::in);
  if (!inFile) {
    std::cout << "Error opening file" << std::endl;
    return -1;
  }

  // Adjust start position to the next full sentence
  adjustToSentenceBoundary2(inFile, start);

  // Move file pointer to the adjusted starting point
  inFile.seekg(start);

  std::string sentence;
  char delimiter = '.';

  // Read until the chunk's end, then continue reading until the next delimiter
  int sentence_count = 0;

  while (std::getline(inFile, sentence, delimiter)) {
    std::streampos currentPos = inFile.tellg();

    sentence = trim2(sentence);

    // Use OpenMP critical section for accessing the global variable safely
    if (sentence != "") {
      /// increment sentence_count
      sentence_count++;
      const std::vector<std::string> doc = tokenize(sentence);
      std::set<std::string> uniqueWords(doc.begin(), doc.end());
      for (const auto &word : uniqueWords) {
#pragma omp critical
        {
          // IDF mapping here
          idf[word]++;
        }
      }
    }

    // If we've read past the thread's chunk and finished a sentence, break
    if (currentPos >= end) {
      break;
    }
    sentence.clear(); // Clear sentence for the next one
  }

  inFile.close();
  return sentence_count;
}
