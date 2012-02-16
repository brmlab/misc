NAME=@EDITME@
CC=gcc
CXX=g++
CFLAGS=$(shell pkg-config --cflags @EDITME@) -Wall
CXXFLAGS=$(CFLAGS)
LDFLAGS=
LIBS=$(shell pkg-config --libs @EDITME@)
OBJ=$(NAME).o

$(NAME): $(OBJ)
	$(CC) $(LDFLAGS) $(LIBS) $(OBJ) -o $(NAME)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(NAME) $(OBJ)
