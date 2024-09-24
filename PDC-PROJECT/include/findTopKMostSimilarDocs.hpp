#ifndef FINDTOPKMOSTSIMILARDOCS_HPP
#define FINDTOPKMOSTSIMILARDOCS_HPP

#include <map>
#include <string>
#include <vector>

std::vector<std::string> findTopKMostSimilarDocs(std::string sentence, int k,
                                                 int numThreads);

#endif
