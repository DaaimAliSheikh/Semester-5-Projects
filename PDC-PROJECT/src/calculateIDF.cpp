
#include "calculateIDF.hpp"
#include <cmath>
#include <map>
#include <set>
#include <string>
#include <vector>

// Function to calculate IDF for all documents
// how many sentences does a specific word appear in, irrespective of how
// many times it appears in a single specfic sentence
std::map<std::string, double>
calculateIDF(const std::vector<std::vector<std::string>> &docs) {
  std::map<std::string, int> docCount;
  int totalDocs = docs.size();

  for (const auto &doc : docs) {
    // converting single doc(array of words/strings) into a set of words/strings
    std::set<std::string> uniqueWords(doc.begin(), doc.end());
    for (const auto &word : uniqueWords) {
      docCount[word]++;
    }
  }

  std::map<std::string, double> idf;
  for (const auto &word : docCount) {
    idf[word.first] = log((double)totalDocs / (1 + word.second));
    // adding one to prevent overly large IDF values for
    // rare words(for which word.second is 1 or any other low value)
  }
  return idf;
}