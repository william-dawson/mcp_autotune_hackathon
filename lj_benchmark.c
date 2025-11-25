#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N_PARTICLES 17000
#define EPSILON 1.0
#define SIGMA 1.0

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

int main(int argc, char *argv[]) {
    Particle *particles = malloc(N_PARTICLES * sizeof(Particle));
    double total_energy = 0.0;
    unsigned int seed = 42;  // Default seed

    // Use seed from command line if provided
    if (argc > 1) {
        seed = atoi(argv[1]);
    }
    srand(seed);

    // Initialize particles with arbitrary positions
    for (int i = 0; i < N_PARTICLES; i++) {
        particles[i].x = (double)rand() / RAND_MAX * 10.0;
        particles[i].y = (double)rand() / RAND_MAX * 10.0;
        particles[i].z = (double)rand() / RAND_MAX * 10.0;
    }

    // Double loop to calculate all pairwise interactions
    for (int i = 0; i < N_PARTICLES; i++) {
        for (int j = i + 1; j < N_PARTICLES; j++) {
            double r = distance(&particles[i], &particles[j]);
            if (r > 0.1) {  // Avoid division by zero
                total_energy += lennard_jones(r);
            }
        }
    }

    printf("Total Lennard-Jones energy: %f\n", total_energy);
    printf("Number of particles: %d\n", N_PARTICLES);
    printf("Number of interactions: %d\n", (N_PARTICLES * (N_PARTICLES - 1)) / 2);

    free(particles);
    return 0;
}
