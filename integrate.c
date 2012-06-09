#include <stdio.h>
#include <stdlib.h>
#include <math.h>


double integrate_trapezoidal(double (*f) (double),
                             double a,
                             double b,
                             int n)
{
    int i;
    double result = 0;
    double h = (b - a) / n;

    result += 0.5 * (f(a) + f(b));

    for (i = 0; i < n - 1; i++) {
        result += f(a + (i + 1) * h);
    }

    result *= h;

    return result;
}


double integrate_romberg(double (*f) (double),
                         double a,
                         double b,
                         int m,
                         int *num_calls,
                         int *num_operations)
{
    int i, j;
    double h = b - a;
    int n = 1;
    int tmp;
    double result;
    double *romberg_table = malloc(m * sizeof(double));
    if (!romberg_table) {
        printf("Hilfe, kein Speicher!\n");
        exit(1);
    }

    *num_calls = 0;
    *num_operations = 1;

    for (i = 0; i < m; i++) {
        romberg_table[i] = 0;
    }

    romberg_table[0] = (b - a) / 2 * (f(a) + f(b));
    *num_operations += 4;

    for (i = 1; i < m; i++) {

        // T_{n,0} -> T_{n+1,0}
        h /= 2;

        for (j = 0; j < n; j++) {
            romberg_table[i] += f(a + (2 * j + 1) * h);
        }

        romberg_table[i] *= h;

        romberg_table[i] += 0.5 * romberg_table[i - 1];

        *num_operations += 4 + n * 4;
        *num_calls += n;

        // T_{n, m}, T_{n-1, m} -> T_{n, m + 1}

        tmp = 1;

        for (j = i - 1; j >= 0; j--) {
            tmp *= 4;
            romberg_table[j] = romberg_table[j + 1]
                    + (romberg_table[j + 1] - romberg_table[j]) / (tmp - 1);
        }

        n *= 2;

        *num_operations += 7 * i + 1;
    }

    result = romberg_table[0];
    free(romberg_table);
    return result;
}
