// project created on 10/26/2009 at 9:25 PM
#include <stdio.h>
#include <malloc.h>
#include "modules.h"

int main(int argc, char *argv[])
{
	int num_numbers = -1;
	int *array = NULL;
	
	do {
		fprintf(stdout, "Please enter the amount of numbers: ");
		fscanf(stdin, " %d", &num_numbers);
	} while(num_numbers <= 0);
	
	array = get_numbers(num_numbers);
	if (array == NULL) {
		fprintf(stderr, "Unable to allocate memory for number array\n");
		return 1;
	}

        fprintf(stdout, "The average of the numbers is %f\n",
                    average(num_numbers, array));

        free(array);
	
	return 0;
}
