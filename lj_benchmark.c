#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define N_PARTICLES 30000
#define EPSILON 1.0
#define SIGMA 1.0
#define MIN_DISTANCE 0.5  // Minimum allowed distance between particles

typedef struct {
    double x, y, z;
} Particle;

double lennard_jones(double r) {
    double sr6 = pow(SIGMA / r, 6);
    double sr12 = sr6 * sr6;
    return 4.0 * EPSILON * (sr12 - sr6);
}

double distance(Particle *p1, Particle *p2) {
    double dx = p1->x - p2->x;
    double dy = p1->y - p2->y;
    double dz = p1->z - p2->z;
    return sqrt(dx*dx + dy*dy + dz*dz);
}

int check_overlap(Particle *particles, int n_current, Particle *new_particle) {
    for (int i = 0; i < n_current; i++) {
        double r = distance(&particles[i], new_particle);
        if (r < MIN_DISTANCE) {
            return 1;  // Overlap detected
        }
    }
    return 0;  // No overlap
}

int main(int argc, char *argv[]) {
    Particle *particles = malloc(N_PARTICLES * sizeof(Particle));
    double total_energy = 0.0;
    unsigned int seed = 42;  // Default seed
    struct timespec start, end;
    double elapsed;

    // Use seed from command line if provided
    if (argc > 1) {
        seed = atoi(argv[1]);
    }
    srand(seed);

    // Initialize particles with arbitrary positions, checking for overlaps
    printf("Generating %d non-overlapping particles...\n", N_PARTICLES);
    int n_generated = 0;
    int attempts = 0;
    double box_size = 100.0;  // Larger box to reduce overlap probability

    while (n_generated < N_PARTICLES && attempts < N_PARTICLES * 1000) {
        Particle candidate;
        candidate.x = (double)rand() / RAND_MAX * box_size;
        candidate.y = (double)rand() / RAND_MAX * box_size;
        candidate.z = (double)rand() / RAND_MAX * box_size;

        if (!check_overlap(particles, n_generated, &candidate)) {
            particles[n_generated] = candidate;
            n_generated++;
        }
        attempts++;
    }

    if (n_generated < N_PARTICLES) {
        printf("Warning: Could only generate %d particles without overlap\n", n_generated);
        free(particles);
        return 1;
    }

    printf("Generated %d particles (attempts: %d)\n", n_generated, attempts);
    printf("Starting benchmark...\n");

    // Time only the double loop calculation
    clock_gettime(CLOCK_MONOTONIC, &start);

    // Double loop to calculate all pairwise interactions
    for (int i = 0; i < N_PARTICLES; i++) {
        for (int j = i + 1; j < N_PARTICLES; j++) {
            double r = distance(&particles[i], &particles[j]);
            total_energy += lennard_jones(r);
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    printf("Total Lennard-Jones energy: %f\n", total_energy);
    printf("Number of particles: %d\n", N_PARTICLES);
    printf("Number of interactions: %d\n", (N_PARTICLES * (N_PARTICLES - 1)) / 2);
    printf("Computation time: %.3f seconds\n", elapsed);

    free(particles);
    return 0;
}
