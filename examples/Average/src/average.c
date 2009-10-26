#include "modules.h"

float average(int num_numbers, int array[]) {
    int sum = 0;
    int cur_index = 0;
    
    for(cur_index = 0; cur_index < num_numbers; cur_index++) {
        sum += array[cur_index];
    }

    return (float)sum / (float)num_numbers;
}
