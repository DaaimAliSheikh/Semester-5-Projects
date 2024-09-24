#include "calculateIDF.hpp"
#include "calculateTFIDF.hpp"
#include "findTopKMostSimilarDocs.hpp"
#include "loadIDFMap.hpp"
#include "saveIDFMap.hpp"
#include "tokenize.hpp"
#include <filesystem>
#include <fstream>
#include <iomanip> // for std::setprecision
#include <iostream>
#include <map>
#include <omp.h>
#include <regex>
#include <sstream>
#include <vector>

namespace fs = std::filesystem;

int main() {
  // Path should be relative to Makefile location

  std::string test_file_path = "document_files/test.txt";
  std::string idf_file_path = "document_files/idf.bin";
  std::string tfidf_dir = "document_files/tf-idf-chunks";
  int numThreads = 10;

  std::cout << "1. Generate TF-IDF Embeddings for the the dataset provided in "
               "document_files/test.txt"
            << std::endl;
  std::cout << "2. Perform a relevancy search on the dataset using the "
               "generated TF-IDF Embeddings. "
            << std::endl;

  while (true) {

    std::string choice;
    std::cout << "Enter your choice: ";
    std::getline(std::cin, choice);

    if (choice == "1") {
      std::map<std::string, double> idf = calculateIDF(
          test_file_path,
          numThreads); // test_file_path and number of threads to process it

      /// save idf into a binary file
      saveIDFMap(idf, idf_file_path);

      /// calculate tf-idf chunks
      calculateTFIDF(test_file_path, idf, numThreads);

      std::cout << "Embeddings generated successfully." << std::endl;
      break;
    } else if (choice == "2") {
      if (fs::directory_iterator(tfidf_dir) == fs::directory_iterator{}) {
        std::cout << "Please generate the embeddings first." << std::endl;
        continue;
      }
      std::string question;
      int k;

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
        fflush(stdin);

        std::cin >> k;
        if (k <= 0) {
          std::cout << "Please provide a valid value for k." << std::endl;
          continue;
        }
        break;
      }
      std::cout << "Searching........" << std::endl;
      std::vector<std::string> topSentences =
          findTopKMostSimilarDocs(question, k, numThreads);

      std::cout << "The top " << k
                << " most similar sentences are:" << std::endl;
      for (int i = 0; i < topSentences.size(); ++i)
        std::cout << i + 1 << ". " << topSentences[i] << std::endl;

      break;
    } else {
      std::cout << "Invalid choice" << std::endl;
      continue;
    }
  }

  /// searching part

  // Calculate TF-IDF for all documents
  // std::vector<std::map<std::string, double>> docTFIDFs;
  // for (const auto &doc : documents) {
  //   docTFIDFs.push_back(calculateTFIDF(doc, idf));
  // }

  // std::map<std::string, double> inputTFIDF =
  //     calculateTFIDF(tokenize(question), idf);

  // std::vector<int> topIndices =
  //     findTopKMostSimilarDocs(inputTFIDF, docTFIDFs, k);

  // std::cout << "size" << topIndices.size() << std::endl;
  // std::cout << "The top " << k << " most similar sentences are:" <<
  // std::endl;

  // for (int i = 0; i < topIndices.size(); ++i) {
  //   std::cout << i + 1 << ". " << sentences[topIndices[i]] << std::endl;
  // }

  return 0;
}
