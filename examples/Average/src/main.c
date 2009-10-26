// project created on 10/26/2009 at 9:25 PM
#include <stdio.h>
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
	
	return 0;
}
