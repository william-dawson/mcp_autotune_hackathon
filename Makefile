CC = gcc
CFLAGS ?= -O2 -Wall
LDFLAGS = -lm

all: lj_benchmark

lj_benchmark: lj_benchmark.c
	$(CC) $(CFLAGS) -o lj_benchmark lj_benchmark.c $(LDFLAGS)

test-correctness: lj_benchmark
	@echo "Running correctness test..."
	@./lj_benchmark 42 > /tmp/lj_output.txt
	@if grep -q "Total Lennard-Jones energy: 2453800171930224.000000" /tmp/lj_output.txt && \
	    grep -q "Number of particles: 30000" /tmp/lj_output.txt && \
	    grep -q "Number of interactions: 449985000" /tmp/lj_output.txt; then \
		echo "✓ Correctness test PASSED"; \
	else \
		echo "✗ Correctness test FAILED"; \
		cat /tmp/lj_output.txt; \
		exit 1; \
	fi

test-speed: lj_benchmark
	@echo "Running speed test..."
	time ./lj_benchmark

test: test-correctness test-speed

clean:
	rm -f lj_benchmark /tmp/lj_output.txt

.PHONY: all test test-correctness test-speed clean
