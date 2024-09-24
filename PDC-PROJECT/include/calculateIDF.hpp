#ifndef CALCULATEIDF_HPP
#define CALCULATEIDF_HPP
#include <map>
#include <string>
#include <vector>

std::map<std::string, double> calculateIDF(const std::string &test_file_path,
                                           int numThreads = 4);
#endif