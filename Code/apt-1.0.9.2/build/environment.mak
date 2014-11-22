# This file contains everything that autoconf guessed for your system.
# if you want you can edit it, just don't re-run configure.

PACKAGE = apt
PACKAGE_VERSION = 1.0.9.2
PACKAGE_MAIL = APT Development Team <deity@lists.debian.org>

# C++ compiler options
CC = gcc
CPPFLAGS+=  -DHAVE_CONFIG_H -D_REENTRANT -D_FORTIFY_SOURCE=2
CXX = g++
CXXFLAGS+= -g -O2 -Wall -Wextra
CXXFLAGS+= -Wcast-align -Wlogical-op -Wredundant-decls -Wmissing-declarations -Wunsafe-loop-optimizations
CXXFLAGS+= -Wsuggest-attribute=pure -Wsuggest-attribute=const -Wsuggest-attribute=noreturn
# a bit too pedantic to be run by default
#CXXFLAGS+= -Wpedantic -Wno-long-long -Wno-vla -Wno-variadic-macros
NUM_PROCS = 16

# Linker stuff
PICFLAGS+= -fPIC -DPIC
LFLAGS+= 
LEFLAGS+= 
SOCKETLIBS:= 
AR:=ar
RANLIB:=ranlib

# Dep generation - this only works for gnu stuff
GCC3DEP = yes
INLINEDEPFLAG = -MD

DOXYGEN = /usr/bin/doxygen
W3M = 

# xsltproc for the man pages and documentation
XSLTPROC := /usr/bin/xsltproc

# DocBook XML
DOCBOOK = $(XSLTPROC) --nonet --novalid --xinclude
DOCBOOK2TEXT = $(W3M) -o display_charset=UTF-8 -no-graph -T text/html \
	-cols 78 -dump

# po4a for the man pages
PO4A := 

# Gettext settings
GMSGFMT = /usr/bin/msgfmt
XGETTEXT = /usr/bin/xgettext
MSGCOMM:=$(dir $(XGETTEXT))/msgcomm
MSGMERGE:=$(dir $(XGETTEXT))/msgmerge
BASH = /bin/bash

# Various library checks
PTHREADLIB = 
PYTHONLIB = @PYTHONLIB@
PYTHONVER = @PYTHONVER@
PYTHONPREFIX = @PYTHONPREFIX@
PYTHONEXECPREFIX = @PYTHONEXECPREFIX@
PYTHONINCLUDE = @PYTHONINCLUDE@
BDBLIB = 
INTLLIBS = 

# Shim Headerfile control
HAVE_STATVFS = yes
HAVE_ZLIB = yes
HAVE_BZ2 = no
HAVE_LZMA = no
NEED_SOCKLEN_T_DEFINE = 

# Shared library things
HOST_OS = linux-gnu
ifneq ($(words $(filter gnu% linux-gnu% kfreebsd-gnu% %-gnu,$(HOST_OS))),0)
   SONAME_MAGIC=-Wl,-soname -Wl,
   LFLAGS_SO=
else
   # Do not know how to create shared libraries here.
   ONLYSTATICLIBS = yes
endif
