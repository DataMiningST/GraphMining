CC = g++
CXXFLAGS += -std=c++11 -Wall
CXXFLAGS += -O3 -DNDEBUG -ftree-vectorizer-verbose=7 -msse2 -msse -msse4.1
# turn on for OpenMP
CXXFLAGS += -fopenmp
LDFLAGS +=
LIBS += -lrt

FM_STATISTICS_CPP = fmStatistics.cpp FMCounter.cpp
FM_STATISTICS_OBJS=$(subst .cpp,.o,$(FM_STATISTICS_CPP))

INCLUDE_PATHS := -ISnap-3.0/snap-core/ -ISnap-3.0/snap-adv/ -ISnap-3.0/glib-core/ -ISnap-3.0/snap-exp/

all: fms

fms: $(FM_STATISTICS_OBJS)
	$(CC) $(CXXFLAGS) -o fms $(FM_STATISTICS_OBJS) Snap-3.0/snap-core/Snap.o $(LDFLAGS) $(LIBS)

fmStatistics.o: fmStatistics.cpp
	$(CC) $(CXXFLAGS) $(INCLUDE_PATHS) -c $< 

%.o: %.cpp %.h
	$(CC) $(CXXFLAGS) $(INCLUDE_PATHS) -c $< 

clean:
	rm -f *.o fmStatistics
