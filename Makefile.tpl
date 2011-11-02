NAME=@EDITME@
CC=gcc
CXX=g++
CFLAGS=$(shell pkg-config --cflags @EDITME@) -Wall
CXXFLAGS=$(CFLAGS)
LDFLAGS=$(shell pkg-config --libs @EDITME@)
OBJ=$(NAME).o

$(NAME): $(OBJ)
	$(CC) $(OBJ) -o $(NAME) $(LDFLAGS)

%.o: %.c
	$(CC) -c $< -o $@ $(CFLAGS)

%.o: %.cpp
	$(CXX) -c $< -o $@ $(CXXFLAGS)

clean:
	rm -f $(NAME) $(OBJ)
