#include <iostream>
#include <boost/filesystem.hpp>
#include <Python.h>

using namespace boost::filesystem;
using namespace std;

int main(int argc, char* argv[]) {
    Py_SetProgramName(Py_DecodeLocale(argv[0], NULL));

    Py_Initialize();

    // path main_script_path();
    PyObject* pName = PyUnicode_DecodeFSDefault("../src/py/main.py");
}