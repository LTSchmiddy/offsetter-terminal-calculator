#include <Python.h>
#include <boost/python.hpp>

#define PY_BOOST_API_MODE 1

#ifdef PY_BOOST_API_MODE
#define bpy boost::python
#endif

int load_python_module();
void unload_python_module();

// PyObject* eval_calc(std::string eval_statement);
std::string py_eval_calc_simple(std::string eval_statement);