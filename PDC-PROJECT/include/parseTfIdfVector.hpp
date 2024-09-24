#ifndef PARSETFIDFVECTOR_HPP
#define PARSETFIDFVECTOR_HPP
#include <map>
#include <string>

std::map<std::string, double> parseTfIdfVector(const std::string &line);
#endif