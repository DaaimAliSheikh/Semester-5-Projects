#include "calculateIDF.hpp"
#include "calculateTFIDF.hpp"
#include "findTopKMostSimilarDocs.hpp"
#include "loadIDFMap.hpp"
#include "saveIDFMap.hpp"
#include <chrono>
#include <filesystem>
#include <iostream>
#include <map>
#include <omp.h>
#include <vector>

namespace fs = std::filesystem;

int main() {
  // Path should be relative to Makefile location

  std::string test_file_path = "document_files/test.txt";
  std::string idf_file_path = "document_files/idf.bin";
  std::string tfidf_dir = "document_files/tf-idf-chunks";
  const int numThreads = 5;
  /// * If you generate embeddings for x threads then the cosine similarity
  /// search should also be with x threads
  /// * make sure each chunk of the dataset that is divided into numThreads
  /// contains atleast 1 complete sentence else there will be repeated sentences

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
      double start = omp_get_wtime();
      std::map<std::string, double> idf = calculateIDF(
          test_file_path,
          numThreads); // test_file_path and number of threads to process it

      /// save idf into a binary file
      saveIDFMap(idf, idf_file_path);

      /// calculate tf-idf chunks
      calculateTFIDF(test_file_path, idf, numThreads);

      double end = omp_get_wtime();

      // Calculate the duration in milliseconds
      double duration = end - start;
      std::cout << "Embeddings generated successfully in " << duration
                << " seconds\n"
                << std::endl;
      break;
    } else if (choice == "2") {
      /// check if tf-idf-chunks directory is empty
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

        std::cin >> k;
        if (k <= 0) {
          std::cout << "Please provide a valid value for k." << std::endl;
          continue;
        }
        break;
      }
      std::cout << "Searching........" << std::endl;
      double start = omp_get_wtime(); // start clock

      std::vector<std::string> topSentences =
          findTopKMostSimilarDocs(question, k, numThreads);
      double end = omp_get_wtime(); // end clock

      std::cout << "The top " << k
                << " most similar sentences are:" << std::endl;
      for (int i = 0; i < topSentences.size(); ++i)
        std::cout << i + 1 << ". " << topSentences[i] << std::endl;

      // Calculate the duration in milliseconds
      double duration = end - start;
      std::cout << std::endl;
      std::cout << "Time taken: " << duration << " seconds" << std::endl;

      break;
    } else {
      std::cout << "Invalid choice" << std::endl;
      continue;
    }
  }

  return 0;
}
