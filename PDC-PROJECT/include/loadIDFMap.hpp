#ifndef LOADIDFMAP_HPP
#define LOADIDFMAP_HPP

#include <map>
#include <string>

// Function to load map from a binary file
std::map<std::string, double> loadIDFMap(const std::string &filename);
#endif