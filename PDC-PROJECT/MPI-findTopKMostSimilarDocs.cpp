
#include <algorithm>
#include <cmath>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <mpi.h>
#include <regex>
#include <string>
#include <unordered_set>
#include <vector>
namespace fs = std::filesystem;

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

// Function to split a string by spaces into a vector of words
std::vector<std::string> tokenize(const std::string sentence) {

  std::string cleaned_text;

  // Remove punctuation
  for (char c : sentence) {
    if (!std::ispunct(c)) {
      cleaned_text += c;
    }
  }

  std::stringstream ss(cleaned_text);
  std::string word;
  std::vector<std::string> tokens;
  std::unordered_set<std::string> stop_words = {
      "a",         "about",   "above",     "after",   "again",    "against",
      "all",       "am",      "an",        "and",     "any",      "are",
      "aren't",    "as",      "at",        "be",      "because",  "been",
      "before",    "being",   "below",     "between", "both",     "but",
      "by",        "can",     "cannot",    "could",   "did",      "didn't",
      "do",        "does",    "doesn't",   "doing",   "don't",    "down",
      "during",    "each",    "few",       "for",     "from",     "further",
      "had",       "hadn't",  "has",       "hasn't",  "have",     "haven't",
      "having",    "he",      "her",       "here",    "hers",     "herself",
      "him",       "himself", "his",       "how",     "i",        "if",
      "in",        "into",    "is",        "isn't",   "it",       "its",
      "itself",    "just",    "ll",        "m",       "me",       "might",
      "more",      "most",    "must",      "my",      "myself",   "need",
      "no",        "nor",     "not",       "now",     "o",        "of",
      "off",       "on",      "once",      "only",    "or",       "other",
      "our",       "ours",    "ourselves", "out",     "over",     "own",
      "re",        "s",       "same",      "shan't",  "she",      "should",
      "shouldn't", "so",      "some",      "such",    "t",        "than",
      "that",      "the",     "their",     "theirs",  "them",     "themselves",
      "then",      "there",   "these",     "they",    "this",     "those",
      "through",   "to",      "too",       "under",   "until",    "up",
      "very",      "was",     "wasn't",    "we",      "were",     "weren't",
      "what",      "when",    "where",     "which",   "while",    "who",
      "whom",      "why",     "will",      "with",    "won't",    "would",
      "y",         "you",     "your",      "yours",   "yourself", "yourselves"};

  while (ss >> word) {
    // convert word to lowercase
    std::transform(word.begin(), word.end(), word.begin(), ::tolower);
    if (stop_words.find(word) == stop_words.end()) {
      // filter out stop words
      tokens.push_back(word);
    }
  }

  return tokens;
}

/// parses a TF-IDF vector from a string read from a file
std::map<std::string, double> parseTfIdfVector(const std::string &line) {
  std::map<std::string, double> tfIdfVector;
  std::regex regex(R"(\{([^}]+)\})"); // Regex to match the content within {}
  std::smatch match;

  if (std::regex_search(line, match, regex)) {
    std::string jsonStr = match[1]; // Get the matched content
    std::istringstream ss(jsonStr);
    std::string token;

    // Split by commas to get each "key: value" pair
    while (std::getline(ss, token, ',')) {
      std::string key;
      double value;
      std::istringstream keyValueStream(token);
      if (std::getline(keyValueStream, key, ':')) {
        key.erase(remove(key.begin(), key.end(), '\"'),
                  key.end()); // Remove quotes
        key.erase(remove(key.begin(), key.end(), ' '),
                  key.end());     // Remove spaces
        keyValueStream >> value;  // Get the value
        tfIdfVector[key] = value; // Store in the map
      }
    }
  }

  return tfIdfVector;
}

// Function to calculate TF for a single document
// how many times a word appears in a single sentence
// eg: [{"hello":  1},{"world":  1 }]
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

/// check if string is only whitespace before parsing it into a tf-idf vector
/// and sentence
bool isOnlyWhitespace(const std::string &str) {
  return std::all_of(str.begin(), str.end(),
                     [](unsigned char c) { return std::isspace(c); });
}

/// -np must be equal to the number of chunks you created
int main(int argc, char *argv[]) {

  MPI_Init(&argc, &argv); // Initialize the MPI environment

  int world_size; // Total number of processes
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);

  int world_rank; // Rank of the current process
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

  std::map<std::string, double> idf;
  std::map<std::string, double> inputTF;
  std::map<std::string, double> inputTFIDF;
  // array of local score maps
  std::vector<std::multimap<double, std::string>> local_scoreMaps(world_size);
  std::string question;
  int k;
//time
  /// ONE PROCESSOR
  if (world_rank == 0) {
    /// check if tf-idf-chunks directory is empty
    std::string tfidf_dir = "document_files/tf-idf-chunks";
    if (fs::directory_iterator(tfidf_dir) == fs::directory_iterator{}) {
      std::cout << "Please generate the embeddings first." << std::endl;
      return 1;
    }

    while (true) {

      std::cout << "Ask something regarding the dataset you provided:"
                << std::endl;

      std::getline(std::cin, question);

      if (question == "") {
        std::cout << "Please ask a valid question." << std::endl;
        continue;
      }
      break;
    }
    while (true) {

      std::cout << "How many top matching sentences would you like to see?"
                << std::endl;

      std::cin >> k;
      if (k <= 0) {
        std::cout << "Please provide a valid value for k." << std::endl;
        continue;
      }
      break;
    }
    std::string idf_path = "document_files/idf.bin";
    std::map<std::string, double> idf = loadIDFMap(idf_path);
    std::map<std::string, double> inputTF = calculateTF2(tokenize(question));

    // calculate inputTFIDF
    for (const auto &word : inputTF) {
      auto it = idf.find(word.first);
      double idfValue = (it != idf.end())
                            ? it->second
                            : 0.0; // Default IDF value if word not found
      inputTFIDF[word.first] = word.second * idfValue;
    }
    std::cout << "Searching........" << std::endl;
  }

  /// All initializations done, START TIMER
  MPI_Barrier(MPI_COMM_WORLD);
  double start_time = MPI_Wtime();
  /// ALL PROCESSORS
  std::ifstream inputFile("document_files/tf-idf-chunks/" +
                          std::to_string(world_rank) + ".txt");
  if (!inputFile.is_open()) {
    std::cout << "File chunk not found" << std::endl;
  }
  // calculate similarity score for each sentence
  std::string line;
  while (std::getline(inputFile, line)) {

    if (isOnlyWhitespace(line)) /// skip parsing if line is only whitespace
      continue;

    // Parse the TF-IDF vector from the line
    auto tfIdfVector = parseTfIdfVector(line);

    // Get the sentence (everything after the TF-IDF vector)
    size_t sentenceStart =
        line.find('}') +
        2; // Find the end of the TF-IDF vector and skip the space
    std::string sentence = line.substr(sentenceStart);

    if (isOnlyWhitespace(
            sentence)) /// skip adding entry if sentence is only whitespace
      continue;

    double similarity = cosineSimilarity(inputTFIDF, tfIdfVector);
    local_scoreMaps[world_rank].insert({similarity, sentence});
  }
  inputFile.close();

  // ONE PROCESSOR
  MPI_Barrier(MPI_COMM_WORLD);

  if (world_rank == 0) {
    // Map to store similarity scores and corresponding document sentences
    // multi map to prevent overwrite if the cosine score of multiple entries is
    // same
    std::multimap<double, std::string, std::greater<>>
        scoreMap; /// greater<> sorts the key(similarity score here) in
                  /// descending order when inserting a pair
    for (const auto &m : local_scoreMaps) {
      scoreMap.insert(m.begin(),
                      m.end()); // Insert each map's elements into the result
    }
    std::vector<std::string> topKSentences;
    int count = 0;
    for (const auto &entry : scoreMap) {
      if (count >= k)
        break;
      topKSentences.push_back(entry.second);
      ++count;
    }
    std::cout << "The top " << k << " most similar sentences are:" << std::endl;
    for (int i = 0; i < topKSentences.size(); ++i)
      std::cout << i + 1 << ". " << topKSentences[i] << std::endl;
  }

  // Synchronize processes again after computation
  MPI_Barrier(MPI_COMM_WORLD);
  // END TIMER
  double end_time = MPI_Wtime();

  // Calculate elapsed time for each process
  double elapsed_time = end_time - start_time;

  // Use MPI_Reduce to calculate the maximum elapsed time
  double max_time;
  MPI_Reduce(&elapsed_time, &max_time, 1, MPI_DOUBLE, MPI_MAX, 0,
             MPI_COMM_WORLD);

  // Rank 0 displays the total time taken
  if (world_rank == 0) {
    std::cout << std::endl;
    std::cout << "Total execution time (maximum time across all processes) "
                 "taken to find the top "
              << k << " most similar sentences: " << max_time << " seconds."
              << std::endl;
  }

  MPI_Finalize(); // Finalize the MPI environment
  return 0;
}