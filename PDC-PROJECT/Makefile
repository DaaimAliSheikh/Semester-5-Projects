
# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -fopenmp 

# Root directory for source files
SRCDIR = src

# Root directory for object files
BUILDDIR = build

# Directory for header files
INCLUDEDIR = include

# Directory for the final executable
BINDIR = bin

# List of source files(.cpp) in src, full paths of the files attained
SRCS = $(shell find $(SRCDIR) -name '*.cpp')  


# List of object files (replace source directory with build directory using path substitution)
OBJS = $(patsubst $(SRCDIR)/%.cpp, $(BUILDDIR)/%.o, $(SRCS))

# Output binary file
TARGET = $(BINDIR)/main

# Rule to build the binary
$(TARGET): $(OBJS)
	@mkdir -p $(BINDIR)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Rule to compile .cpp files to .o files in the build directory
#$<: Refers to the dependency (in this case, the .cpp file).
#$@: Refers to the target (in this case, the .o file).
$(BUILDDIR)/%.o: $(SRCDIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -I$(INCLUDEDIR) -c $< -o $@

# Clean up the build files
clean:
	rm -rf $(BUILDDIR) $(BINDIR)

# Run the compiled binary
run: $(TARGET)
	./$(TARGET)