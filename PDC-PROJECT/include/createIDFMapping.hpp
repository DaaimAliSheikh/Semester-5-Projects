#ifndef CREATEIDFMAPPING_HPP
#define CREATEIDFMAPPING_HPP
#include <map>
#include <string>
#include <vector>

int createIDFMapping(const std::string &filepath,
                      std::map<std::string, double> &idf, long start,
                     long end);

#endif