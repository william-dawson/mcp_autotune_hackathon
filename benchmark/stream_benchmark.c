#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 80000000
#define NTIMES 100

double a[N], b[N], c[N];

int main(int argc, char *argv[]) {
    for (int i = 0; i < N; i++) {
        a[i] = 1.0;
        b[i] = 2.0;
        c[i] = 0.0;
    }

    struct timespec start, end;
    double time;
    double sum = 0.0;  // Accumulator to prevent optimization

    // Copy: a[i] = b[i]
    sum = 0.0;
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int k = 0; k < NTIMES; k++) {
        for (int i = 0; i < N; i++) a[i] = b[i];
        sum += a[N/2];  // Forces each iteration to execute
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    if (sum < 0.0) return 1;  // Use sum to prevent elimination
    time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    double copy_bw = (2 * N * sizeof(double) * NTIMES / time) / 1e9;

    // Scale: b[i] = 2.0 * a[i]
    sum = 0.0;
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int k = 0; k < NTIMES; k++) {
        for (int i = 0; i < N; i++) b[i] = 2.0 * a[i];
        sum += b[N/2];  // Forces each iteration to execute
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    if (sum < 0.0) return 1;  // Use sum to prevent elimination
    time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    double scale_bw = (2 * N * sizeof(double) * NTIMES / time) / 1e9;

    // Add: c[i] = a[i] + b[i]
    sum = 0.0;
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int k = 0; k < NTIMES; k++) {
        for (int i = 0; i < N; i++) c[i] = a[i] + b[i];
        sum += c[N/2];  // Forces each iteration to execute
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    if (sum < 0.0) return 1;  // Use sum to prevent elimination
    time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    double add_bw = (3 * N * sizeof(double) * NTIMES / time) / 1e9;

    // Triad: a[i] = b[i] + 3.0 * c[i]
    sum = 0.0;
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int k = 0; k < NTIMES; k++) {
        for (int i = 0; i < N; i++) a[i] = b[i] + 3.0 * c[i];
        sum += a[N/2];  // Forces each iteration to execute
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    if (sum < 0.0) return 1;  // Use sum to prevent elimination
    time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    double triad_bw = (3 * N * sizeof(double) * NTIMES / time) / 1e9;

    // Compute checksum
    double checksum = 0.0;
    for (int i = 0; i < N; i++) {
        checksum += a[i] + b[i] + c[i];
    }

    printf("{\"copy_GB_s\": %.2f, \"scale_GB_s\": %.2f, \"add_GB_s\": %.2f, \"triad_GB_s\": %.2f, \"checksum\": %.1f}\n",
           copy_bw, scale_bw, add_bw, triad_bw, checksum);

    return 0;
}
