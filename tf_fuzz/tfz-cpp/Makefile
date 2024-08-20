# Copyright (c) 2019-2024, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

CXX = g++
INCLUDES = -I /usr/include -I . -I ./parser -I ./template -I ./assets -I ./calls -I ./boilerplate -I ./utility -I ./crypto_model
override CXXFLAGS += -std=gnu++17 -Werror=return-type -O0 -g $(INCLUDES)

sources = $(wildcard assets/*.cpp) \
          $(wildcard crypto_model/*.cpp) \
		  $(wildcard boilerplate/*.cpp) \
		  $(wildcard calls/*.cpp) \
		  $(wildcard template/*.cpp) \
		  $(wildcard utility/*.cpp) \
		  $(wildcard *.cpp)

headers = $(wildcard assets/*.hpp) \
          $(wildcard crypto_model/*.hpp) \
		  $(wildcard boilerplate/*.hpp) \
		  $(wildcard calls/*.hpp) \
		  $(wildcard template/*.hpp) \
		  $(wildcard utility/*.hpp) \
		  $(wildcard *.hpp)

objs    = $(sources:.cpp=.o)
depends = $(sources:.cpp=.d)

generated_sources  = parser/tf_fuzz_grammar.tab.cpp parser/tf_fuzz_grammar.lex.c
generated_objs	   = parser/tf_fuzz_grammar.tab.o parser/tf_fuzz_grammar.lex.o
generated_includes = parser/tf_fuzz_grammar.tab.hpp

.PHONY: default
default: $(generated_includes) tfz;

# Automatically gather prerequisites
# [GNU Make manual, section 4.14]

include $(depends)

%.d: %.cpp $(generated_includes) $(generated_sources)
	@set -e; rm -f $@; \
	$(CXX) -M -MM $(CXXFLAGS) $< > $@.$$$$; \
	sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' < $@.$$$$ > $@; \
	rm -f $@.$$$$

tfz: $(generated_includes) $(generated_objs) $(objs) $(headers) Makefile
	$(CXX) $(CXXFLAGS) -o tfz $(generated_objs) $(objs)

parser/tf_fuzz_grammar.tab.hpp:  parser/tf_fuzz_grammar.y class_forwards.hpp \
boilerplate/boilerplate.hpp utility/gibberish.hpp utility/string_ops.hpp \
tf_fuzz.hpp utility/data_blocks.hpp utility/variables.hpp \
utility/find_or_create_asset.hpp assets/psa_asset.hpp \
assets/sst_asset.hpp assets/crypto_asset.hpp calls/psa_call.hpp \
template/template_line.hpp Makefile
	rm -f parser/tf_fuzz_grammar.tab.hpp parser/tf_fuzz_grammar.tab.cpp \
	parser/tf_fuzz_grammar.tab.o
	bison --verbose -d parser/tf_fuzz_grammar.y -o \
	parser/tf_fuzz_grammar.tab.cpp

parser/tf_fuzz_grammar.tab.cpp:  parser/tf_fuzz_grammar.y class_forwards.hpp \
boilerplate/boilerplate.hpp utility/gibberish.hpp utility/string_ops.hpp \
tf_fuzz.hpp utility/data_blocks.hpp utility/variables.hpp \
utility/find_or_create_asset.hpp assets/psa_asset.hpp \
assets/sst_asset.hpp assets/crypto_asset.hpp calls/psa_call.hpp \
template/template_line.hpp Makefile
	rm -f parser/tf_fuzz_grammar.tab.hpp parser/tf_fuzz_grammar.tab.cpp \
	parser/tf_fuzz_grammar.tab.o
	bison --verbose -d parser/tf_fuzz_grammar.y -o \
	parser/tf_fuzz_grammar.tab.cpp

parser/tf_fuzz_grammar.lex.c:  parser/tf_fuzz_grammar.l \
parser/tf_fuzz_grammar.tab.hpp Makefile
	lex --outfile=parser/tf_fuzz_grammar.lex.c parser/tf_fuzz_grammar.l

parser/tf_fuzz_grammar.lex.o:  parser/tf_fuzz_grammar.lex.c Makefile
	$(CXX) $(CXXFLAGS) -c -o $@ \
	parser/tf_fuzz_grammar.lex.c

parser/tf_fuzz_grammar.tab.o:  parser/tf_fuzz_grammar.lex.o \
parser/tf_fuzz_grammar.tab.cpp parser/tf_fuzz_grammar.tab.hpp Makefile
	$(CXX) $(CXXFLAGS) -c -o $@ \
	parser/tf_fuzz_grammar.tab.cpp

.PHONY: clean
clean:
	rm -f tfz *.d **/*.d *.d* **/*.d* $(objs) $(generated_objs) $(generated_includes) $(generated_sources)
	rm -rf parser/tf_fuzz_grammar.lex.c parser/tf_fuzz_grammar.output
	rm -f `find regression -name "stdout_stderr"`
	rm -f `find regression -name "test.c"`
	rm -f demo/tossThis*
