#ifndef FINDTOPKMOSTSIMILARDOCS_HPP
#define FINDTOPKMOSTSIMILARDOCS_HPP

#include <map>
#include <string>
#include <vector>
#include "findTopKMostSimilarDocs.hpp"


std::vector<int> findTopKMostSimilarDocs(
    const std::map<std::string, double> &inputTFIDF,
    const std::vector<std::map<std::string, double>> &docTFIDFs, int k);

#endif
