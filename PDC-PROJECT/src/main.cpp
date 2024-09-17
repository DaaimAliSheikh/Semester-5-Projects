#include "calculateIDF.hpp"
#include "calculateTFIDF.hpp"
#include "findTopKMostSimilarDocs.hpp"
#include "getSentences.hpp"
#include "tokenize.hpp"
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <vector>

int main() {

  // Path should be relative to Makefile location
  std::cout << "Processing file: test.txt........" << std::endl;

  std::string filepath = "document_files/test.txt";

  std::vector<std::string> sentences = getSentences(filepath);

  std::vector<std::vector<std::string>> documents;
  for (const auto &sentence : sentences)
    documents.push_back(tokenize(sentence));

  // Calculate IDF from all documents
  std::map<std::string, double> idf = calculateIDF(documents);

  // Calculate TF-IDF for all documents
  std::vector<std::map<std::string, double>> docTFIDFs;
  for (const auto &doc : documents) {
    docTFIDFs.push_back(calculateTFIDF(doc, idf));
  }
  // for (const auto &pairing : idf){
  //   std::cout << pairing.first   << std::endl;
  // }
  // for (const auto &sentence : sentences){
  //   std::cout << sentence  <<"END"<< std::endl;
  // }

  std::string question;
  std::cout << "Ask a question regarding the dataset you provided:"
            << std::endl;
  std::getline(std::cin, question);

  int k;
  std::cout << "how many top matching sentences would you like to see?"
            << std::endl;
  std::cin >> k;

  std::map<std::string, double> inputTFIDF =
      calculateTFIDF(tokenize(question), idf);

  std::vector<int> topIndices =
      findTopKMostSimilarDocs(inputTFIDF, docTFIDFs, k);

  
 std::cout<<"size"<<topIndices.size()<<std::endl;
  std::cout << "The top " << k << " most similar sentences are:" <<
  std::endl;

  for (int i = 0; i < topIndices.size(); ++i) {
    std::cout << i + 1 << ". " << sentences[topIndices[i]] << std::endl;
  }

  return 0;
}
