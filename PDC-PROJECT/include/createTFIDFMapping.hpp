#ifndef CREATETFIDFMAPPING_HPP
#define CREATETFIDFMAPPING_HPP
#include <map>
#include <string>
#include <vector>

void createTFIDFMapping(const std::string &test_file_path,
                        std::map<std::string, double> &idf, long start,
                        long end);
#endif