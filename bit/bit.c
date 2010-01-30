/* For people who don't want to install all of python */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Python.h>


int main(int argc, char* argv[])
{
    putenv("PYTHONPATH=./.buildit");
    Py_Initialize();
    
    FILE* build_file;
    char* buildit_code;
    char* file_name = "buildit";
    
    if(argc > 1) { file_name = argv[1]; }
    if((build_file = fopen(file_name, "r")) == NULL)
    {
        printf("ERROR: could not open %s", file_name);
    }
    /* Get the file length */
    fseek(build_file, 0, SEEK_END);
    size_t length = ftell(build_file);
    fseek(build_file, 0, SEEK_SET);
    /* Create the code string */
    buildit_code = (char*)malloc(length + 1);
    fread(buildit_code, 1, length, build_file);
    buildit_code[length] = '\0';
    
    /* Actual execution of builit script */
    PyRun_SimpleString(buildit_code);
 
    fclose(build_file);
    free(build_file);
    free(file_name);
    Py_Finalize();
    return 0;
}
