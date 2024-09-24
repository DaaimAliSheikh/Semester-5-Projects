#include <fstream>
#include <iomanip> // for std::setprecision
#include <map>
#include <regex>
#include <sstream>
#include <vector>
#include <parseTfIdfVector.hpp>

std::map<std::string, double> parseTfIdfVector(const std::string &line) {
  std::map<std::string, double> tfIdfVector;
  std::regex regex(R"(\{([^}]+)\})"); // Regex to match the content within {}
  std::smatch match;

  if (std::regex_search(line, match, regex)) {
    std::string jsonStr = match[1]; // Get the matched content
    std::istringstream ss(jsonStr);
    std::string token;

    // Split by commas to get each "key: value" pair
    while (std::getline(ss, token, ',')) {
      std::string key;
      double value;
      std::istringstream keyValueStream(token);
      if (std::getline(keyValueStream, key, ':')) {
        key.erase(remove(key.begin(), key.end(), '\"'),
                  key.end()); // Remove quotes
        key.erase(remove(key.begin(), key.end(), ' '),
                  key.end());     // Remove spaces
        keyValueStream >> value;  // Get the value
        tfIdfVector[key] = value; // Store in the map
      }
    }
  }

  return tfIdfVector;
}