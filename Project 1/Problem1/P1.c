
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double exponential_rand(double lambda){
    double u = (double) rand() / RAND_MAX;
    return -log(u) / lambda;
}


int main(){
    int num_process = 1000;
    double arrival_lambda = 2.0;
    double service_lambda = 1.0;
    double current_time = 0.0;
    double tot_service_time = 0.0;

    printf("Process ID\tArrival Time\tRequested Service Time\n");
    printf("---------------------------------------------------\n");

    for(int i = 1; i <= num_process; i++){
        double int_arrival_time = exponential_rand(arrival_lambda);
        current_time += int_arrival_time;

        double service_time = exponential_rand(service_lambda);
        tot_service_time += service_time;

        printf("%d\t\t%.2f\t\t%.2f\n", i, current_time,  service_time);
    }
    printf("\nActual Average Arrival Rate: %.2f processes per second\n", num_process / current_time);
    printf("\nActual Average Service Time: %.2f seconds\n", tot_service_time / num_process);

    return 0;
}