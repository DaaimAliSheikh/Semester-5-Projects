#ifndef CALCULATETFIDF_HPP
#define CALCULATETFIDF_HPP
#include <map>
#include <string>
#include <vector>

void calculateTFIDF(const std::string &test_file_path,
                    std::map<std::string, double> &idf, int numThreads);
#endif