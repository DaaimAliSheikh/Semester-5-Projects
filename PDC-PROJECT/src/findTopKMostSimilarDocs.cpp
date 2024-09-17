

#include <cmath>
#include <map>
#include <string>
#include <vector>

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
std::vector<int> findTopKMostSimilarDocs(
    const std::map<std::string, double> &inputTFIDF,
    const std::vector<std::map<std::string, double>> &docTFIDFs, int k) {
  // Map to store similarity scores and corresponding document indices
  std::map<double, int, std::greater<>>
      scoreMap; /// greater<> sorts the key(similarity score here) in descending
                /// order when inserting a pair

  // Compute similarity scores for all documents
  for (int i = 0; i < docTFIDFs.size(); ++i) {
    double similarity = cosineSimilarity(inputTFIDF, docTFIDFs[i]);
    scoreMap[similarity] = i;
  }

  // Extract the top k indices
  std::vector<int> topKIndices;
  int count = 0;
  for (const auto &entry : scoreMap) {
    if (count >= k)
      break;
    topKIndices.push_back(entry.second);
    ++count;
  }
  return topKIndices; // Return indices of the top k most similar documents
}