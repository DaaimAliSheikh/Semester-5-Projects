#ifndef CALCULATETFIDF_HPP
#define CALCULATETFIDF_HPP
#include <map>
#include <string>
#include <vector>


std::map<std::string, double>
calculateTFIDF(const std::vector<std::string> &doc,
               const std::map<std::string, double> &idf);
#endif