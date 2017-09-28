#!/bin/sh
echo "Compiling $1"
g++ ./$1
echo "Running $1"
./a.out
