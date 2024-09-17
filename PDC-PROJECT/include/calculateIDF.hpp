#ifndef CALCULATETF_HPP
#define CALCULATETF_HPP
#include <map>
#include <string>
#include <vector>


std::map<std::string, double>
calculateIDF(const std::vector<std::vector<std::string>> &docs);


#endif