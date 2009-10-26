#include <stdio.h>
#include <malloc.h>
#include "modules.h"

int* get_numbers(num_numbers) {
	int* array = NULL;
        int cur_index = 0;
	
	array = malloc(num_numbers * sizeof(int));
	if (array == NULL) {
		return NULL;
	}

        for(cur_index = 0; cur_index < num_numbers; cur_index++) {
            fprintf(stdout, "Next number: ");
            fscanf(stdin, "%d", &array[cur_index]);
        }
	
	return array;
}
