#ifndef SAVEIDFMAP_HPP
#define SAVEIDFMAP_HPP

#include <map>
#include <string>
void saveIDFMap(const std::map<std::string, double> &idf,
                const std::string &filename);
#endif
