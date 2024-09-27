#include "createTFIDFMapping.hpp"
#include "tokenize.hpp"
#include <algorithm> // for std::all_of
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <omp.h>
#include <set>
#include <string>
#include <vector>

// Function to calculate TF for a single document
// how many times a word appears in a single sentence
// eg: [{"hello":  0.1 },{"world":  0.2 }]
std::map<std::string, double> calculateTF(const std::vector<std::string> &doc) {
  std::map<std::string, int> wordCount;
  for (const auto &word : doc) {
    wordCount[word]++;
  }

  std::map<std::string, double> tf;
  for (const auto &word : wordCount) {
    tf[word.first] = (double)word.second / doc.size();
  }
  return tf;
}

// Helper function to trim whitespace
std::string trim(const std::string &str) {
  // Step 1: Trim leading and trailing whitespace
  size_t first = str.find_first_not_of(" \n\r\t\f\v");
  if (first == std::string::npos)
    return ""; // String is empty or consists only of whitespace

  size_t last = str.find_last_not_of(" \n\r\t\f\v");
  std::string trimmedStr = str.substr(first, last - first + 1);

  // Step 2: Remove newlines from the middle
  std::string result;
  for (char c : trimmedStr) {
    if (c == '\n') {
      // Replace newlines with a space
      if (!result.empty() && result.back() != ' ') {
        result +=
            ' '; // Add a space if the last character is not already a space
      }
    } else {
      result += c; // Append the character
    }
  }

  return result;
}

// Adjust start position of a chunk to the next delimiter
void adjustToSentenceBoundary(std::fstream &inFile, long &start) {
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
/// check if string is only whitespace before converting into a tf-idf vector
bool isOnlyWhitespace2(const std::string &str) {
  return std::all_of(str.begin(), str.end(),
                     [](unsigned char c) { return std::isspace(c); });
}

// Function for reading and processing a part of the file
void createTFIDFMapping(const std::string &test_file_path,
                        std::map<std::string, double> &idf, long start,
                        long end) {
  std::fstream inFile(test_file_path, std::ios::in);
  if (!inFile) {
    std::cout << "Error opening test file" << std::endl;
    return;
  }

  std::ofstream output("document_files/tf-idf-chunks/" +
                       std::to_string(omp_get_thread_num()) + ".txt");
  if (!output.is_open()) {
    std::cerr << "Error opening file" << std::endl;
    return;
  }

  // Adjust start position to the next full sentence
  adjustToSentenceBoundary(inFile, start);

  // Move file pointer to the adjusted starting point
  inFile.seekg(start);

  std::string sentence;
  char delimiter = '.';

  // Read until the chunk's end, then continue reading until the next delimiter

  while (std::getline(inFile, sentence, delimiter)) {
    std::streampos currentPos = inFile.tellg();

    sentence = trim(sentence);

    if (sentence != "" && !isOnlyWhitespace2(sentence)) {
      // Calculate TF-IDF Vector
      std::map<std::string, double> tf = calculateTF(tokenize(sentence));
      std::map<std::string, double> tfidf;
      for (const auto &word : tf) {
        auto it = idf.find(word.first);
        double idfValue = (it != idf.end())
                              ? it->second
                              : 0.0; // Default IDF value if word not found
        tfidf[word.first] = word.second * idfValue;
      }
      // Write the TF-IDF vector
      output << "{";
      for (auto it = tfidf.begin(); it != tfidf.end(); ++it) {
        output << "\"" << it->first << "\": " << std::fixed
               << std::setprecision(2) << it->second;
        if (std::next(it) != tfidf.end()) {
          output << ", ";
        }
      }
      output << "} " << sentence << std::endl; // Write the sentence
    }

    // If we've read past the thread's chunk and finished a sentence, break
    if (currentPos >= end) {
      break;
    }
    sentence.clear(); // Clear sentence for the next one
  }

  inFile.close();
}
