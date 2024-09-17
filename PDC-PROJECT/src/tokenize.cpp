#include "tokenize.hpp"
#include <algorithm>
#include <cctype> // For std::ispunct
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>

// Function to split a string by spaces into a vector of words
std::vector<std::string> tokenize(const std::string sentence) {

  std::string cleaned_text;

  // Remove punctuation
  for (char c : sentence) {
    if (!std::ispunct(c)) {
      cleaned_text += c;
    }
  }

  std::stringstream ss(cleaned_text);
  std::string word;
  std::vector<std::string> tokens;
  std::unordered_set<std::string> stop_words = {
      "a",         "about",   "above",     "after",   "again",    "against",
      "all",       "am",      "an",        "and",     "any",      "are",
      "aren't",    "as",      "at",        "be",      "because",  "been",
      "before",    "being",   "below",     "between", "both",     "but",
      "by",        "can",     "cannot",    "could",   "did",      "didn't",
      "do",        "does",    "doesn't",   "doing",   "don't",    "down",
      "during",    "each",    "few",       "for",     "from",     "further",
      "had",       "hadn't",  "has",       "hasn't",  "have",     "haven't",
      "having",    "he",      "her",       "here",    "hers",     "herself",
      "him",       "himself", "his",       "how",     "i",        "if",
      "in",        "into",    "is",        "isn't",   "it",       "its",
      "itself",    "just",    "ll",        "m",       "me",       "might",
      "more",      "most",    "must",      "my",      "myself",   "need",
      "no",        "nor",     "not",       "now",     "o",        "of",
      "off",       "on",      "once",      "only",    "or",       "other",
      "our",       "ours",    "ourselves", "out",     "over",     "own",
      "re",        "s",       "same",      "shan't",  "she",      "should",
      "shouldn't", "so",      "some",      "such",    "t",        "than",
      "that",      "the",     "their",     "theirs",  "them",     "themselves",
      "then",      "there",   "these",     "they",    "this",     "those",
      "through",   "to",      "too",       "under",   "until",    "up",
      "very",      "was",     "wasn't",    "we",      "were",     "weren't",
      "what",      "when",    "where",     "which",   "while",    "who",
      "whom",      "why",     "will",      "with",    "won't",    "would",
      "y",         "you",     "your",      "yours",   "yourself", "yourselves"};

  while (ss >> word) {
    // convert word to lowercase
    std::transform(word.begin(), word.end(), word.begin(), ::tolower);
    if (stop_words.find(word) == stop_words.end()) {
      // filter out stop words
      tokens.push_back(word);
    }
  }

  return tokens;
}
