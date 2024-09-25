#include "findTopKMostSimilarDocs.hpp"
#include "loadIDFMap.hpp"
#include "tokenize.hpp"
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <omp.h>
#include <parseTfIdfVector.hpp>
#include <string>
#include <vector>

// Function to calculate TF for a single document
// how many times a word appears in a single sentence
// eg: [{"hello":  0.1 },{"world":  0.2 }]
std::map<std::string, double>
calculateTF2(const std::vector<std::string> &doc) {
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

// Function to calculate the dot product of two TF-IDF vectors
double dotProduct(const std::map<std::string, double> &vecA,
                  const std::map<std::string, double> &vecB) {
  double dot = 0.0;
  for (const auto &pair : vecA) {
    if (vecB.find(pair.first) != vecB.end()) {
      dot += pair.second * vecB.at(pair.first);
    }
  }
  return dot;
}

// Function to calculate the magnitude of a TF-IDF vector
double magnitude(const std::map<std::string, double> &vec) {
  double sum = 0.0;
  for (const auto &pair : vec) {
    sum += pair.second * pair.second;
  }
  return sqrt(sum);
}

// Function to calculate cosine similarity between two TF-IDF vectors
double cosineSimilarity(const std::map<std::string, double> &vecA,
                        const std::map<std::string, double> &vecB) {
  double dot = dotProduct(vecA, vecB);
  double magA = magnitude(vecA);
  double magB = magnitude(vecB);

  // Handle division by zero
  if (magA == 0.0 || magB == 0.0)
    return 0.0;

  return dot / (magA * magB);
}

// Function to find the most similar k documents
std::vector<std::string> findTopKMostSimilarDocs(std::string sentence, int k,
                                                 int numThreads) {
  std::string idf_path = "document_files/idf.bin";
  std::map<std::string, double> idf = loadIDFMap(idf_path);
  std::map<std::string, double> inputTF = calculateTF2(tokenize(sentence));
  std::map<std::string, double> inputTFIDF;

  for (const auto &word : inputTF) {
    auto it = idf.find(word.first);
    double idfValue = (it != idf.end())
                          ? it->second
                          : 0.0; // Default IDF value if word not found
    inputTFIDF[word.first] = word.second * idfValue;
  }

  //  for (const auto &word : inputTFIDF) {
  //     std::cout << word.first << " " << word.second << std::endl;
  //   }
  // Map to store similarity scores and corresponding document sentences

  std::map<double, std::string, std::greater<>>
      scoreMap; /// greater<> sorts the key(similarity score here) in descending
                /// order when inserting a pair

  // array of local score maps
  std::vector<std::map<double, std::string>> local_scoreMaps(numThreads);

  // Set the number of threads for OpenMP
  omp_set_num_threads(numThreads);

// Parallelize the file reading using OpenMP
#pragma omp parallel
  {
    int threadID = omp_get_thread_num();
    std::ifstream inputFile("document_files/tf-idf-chunks/" +
                            std::to_string(threadID) + ".txt");
    if (!inputFile.is_open()) {
      std::cout << "File chunk not found" << std::endl;
    }
    // calculate similarity score for each sentence
    std::string line;
    while (std::getline(inputFile, line)) {
      // Parse the TF-IDF vector from the line
      auto tfIdfVector = parseTfIdfVector(line);

      // Get the sentence (everything after the TF-IDF vector)
      size_t sentenceStart =
          line.find('}') +
          2; // Find the end of the TF-IDF vector and skip the space
      std::string sentence = line.substr(sentenceStart);

      double similarity = cosineSimilarity(inputTFIDF, tfIdfVector);
      local_scoreMaps[threadID][similarity] = sentence;
    }
    inputFile.close();
  }
  /// merge the local score maps in to global
  for (int i = 0; i < numThreads; ++i) {
    for (const auto &entry : local_scoreMaps[i]) {
      scoreMap[entry.first] = entry.second;
    }
  }

  // Extract the top k sentences
  std::vector<std::string> topKSentences;
  int count = 0;
  for (const auto &entry : scoreMap) {
    if (count >= k)
      break;
    topKSentences.push_back(entry.second);
    ++count;
  }
  return topKSentences; // Return indices of the top k most similar documents
}