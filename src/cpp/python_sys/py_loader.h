#include <Python.h>
// #include <boost/python.hpp>

int load_python_module();
void unload_python_module();

// PyObject* eval_calc(std::string eval_statement);
std::string py_eval_calc(std::string eval_statement);