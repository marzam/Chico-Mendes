################################################################################
#
#
#  Universidade Federal Rural do Rio de Janeiro
#  Instituto Multidisciplinar - Departamento de Ciencia da Computacao
#  por: Marcelo Zamith - zamith.marcelo@gmail.com
#  para compilar com target release use o comando: make target=release + rápido
#
#  versão de on-ramp
#
################################################################################
EXEFILE      = occupCA
LIBFILE      = liboccupCA.so
APPLICATION  = -D_APPLICATION=\"$(EXEFILE)\"
#CPUCC       = /opt/intel/bin/icpc
CPUCC       = g++ #/opt/gnu-gcc/bin/g++
CPPFLAGS    = --std=c++11 -m64 -Wno-reorder #     -Wunused-variable #-Wno-conversion-null -Wdelete-non-virtual-dtor
DEFS        = $(APPLICATION)  $(VERSION) -DALIGN=64

INCLUDES  = -I.                           \
            -I/opt/glew/include \
            -I/usr/include/GL

LIBDIR   =  -L/usr/lib                          \
            -L/opt/glew/lib

#LIBDIR      = -L/opt/gnu-gcc/lib64
LIBS     =  -lm -lGLEW -lGLU -lglut -lGL

LINK     =  $(LIBDIR) $(LIBS)
CPU_COMPILE = $(CPUCC) $(DEFS) $(INCLUDES) $(CPPFLAGS)

ifeq ($(target), release)
  DEFS      +=
  CPPFLAGS  +=      -O3
else
  DEFS     += -D_DEBUG
  CPPFLAGS += -g -Wall -O0
endif

all: exec lib

exec:	CellularAutomata           \
		main

	$(CPU_COMPILE)  obj/CellularAutomata.o        \
			        obj/main.o             \
	$(LINK) -o $(EXEFILE)

main:
	$(CPU_COMPILE) -c main.cpp -o obj/main.o

CellularAutomata:
	$(CPU_COMPILE) -c CellularAutomata.cpp -o obj/CellularAutomata.o

#lIB
lib:	lCellularAutomata          \
			buildlib

buildlib:
	$(CPU_COMPILE) -shared  -Wl,-soname,$(LIBFILE)  -o $(LIBFILE) \
			      obj/lCellularAutomata.o


lCellularAutomata:
	$(CPU_COMPILE) -fPIC -c CellularAutomata.cpp -o obj/lCellularAutomata.o


clean:
	rm obj/*.o

files:
	rm *.txt; rm *.dat; rm obj/*.o
