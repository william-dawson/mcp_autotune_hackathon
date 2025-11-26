CC = gcc
CFLAGS ?= -O2 -Wall
LDFLAGS = -lm

all: stream_benchmark

stream_benchmark: stream_benchmark.c
	$(CC) $(CFLAGS) -o stream_benchmark stream_benchmark.c $(LDFLAGS)

custom: stream_benchmark_custom.c
	$(CC) $(CFLAGS) -o stream_benchmark stream_benchmark_custom.c $(LDFLAGS)

test-correctness: stream_benchmark
	./stream_benchmark

test-speed: stream_benchmark
	./stream_benchmark

test: test-correctness test-speed

clean:
	rm -f stream_benchmark stream_benchmark_custom.c

.PHONY: all test test-correctness test-speed clean custom
