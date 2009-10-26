#include <stdio.h>
#include <malloc.h>
#include "modules.h"

int* get_numbers(num_numbers) {
	int* array = NULL;
	
	array = malloc(num_numbers * sizeof(int));
	if (array == NULL) {
		return NULL;
	}
	
	return array;
}