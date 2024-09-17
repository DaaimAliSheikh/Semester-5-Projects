#include "calculateTFIDF.hpp"

#include <iostream>
#include <map>
#include <string>
#include <vector>

using namespace std;

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

// Function to calculate TF-IDF for a document
std::map<std::string, double>
calculateTFIDF(const std::vector<std::string> &doc,
               const std::map<std::string, double> &idf) {
  std::map<std::string, double> tf = calculateTF(doc);
  std::map<std::string, double> tfidf;

  for (const auto &word : tf) {
    auto it = idf.find(word.first);
    double idfValue = (it != idf.end())
                          ? it->second
                          : 0.0; // Default IDF value if word not found
    tfidf[word.first] = word.second * idfValue;
  }
  return tfidf;
}