# -*- make -*-
BASE=../..
SUBDIR=test/interactive-helper
APT_DOMAIN=none

# Bring in the default rules
include ../../buildlib/defaults.mak

# Program for testing methods
PROGRAM=mthdcat
SLIBS = 
SOURCE = mthdcat.cc
include $(PROGRAM_H)

# Program for testing the tar/deb extractor
PROGRAM=testdeb
SLIBS = -lapt-pkg -lapt-inst
LIB_MAKES = apt-pkg/makefile apt-inst/makefile
SOURCE = testdeb.cc
include $(PROGRAM_H)

# Program for testing tar extraction
PROGRAM=extract-control
SLIBS = -lapt-pkg -lapt-inst
LIB_MAKES = apt-pkg/makefile apt-inst/makefile
SOURCE = extract-control.cc
include $(PROGRAM_H)

# Program for testing udevcdrom
PROGRAM=test_udevcdrom
SLIBS = -lapt-pkg
LIB_MAKES = apt-pkg/makefile
SOURCE = test_udevcdrom.cc
include $(PROGRAM_H)

# Program for checking rpm versions
#PROGRAM=rpmver
#SLIBS = -lapt-pkg -lrpm
#SOURCE = rpmver.cc
#include $(PROGRAM_H)

# Program for testing udevcdrom
PROGRAM=aptwebserver
SLIBS = -lapt-pkg -lpthread
LIB_MAKES = apt-pkg/makefile
SOURCE = aptwebserver.cc
include $(PROGRAM_H)
