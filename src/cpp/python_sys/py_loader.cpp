#include <iostream>



// Compatability fix for Python.h and boost/python.hpp
#define HAVE_SNPRINTF 1
// #define BOOST_BIND_GLOBAL_PLACEHOLDERS 1


#include <boost/bind/bind.hpp>
using namespace boost::placeholders;

#include <Python.h>
#include <boost/python.hpp>
#include <boost/filesystem.hpp>
#include <boost/foreach.hpp>



#include "py_loader.h"

#define PY_OFFSETTER_PATH "offsetter"


#define CALC_FN "calculate_response"
#define FORMAT_FN "format_response"
#define CALC_FORMAT_FN "calculate_formatted_response"


#ifdef PY_BOOST_API_MODE

// Abbreviation, without confusion as to whether something is coming from this namespace.

// Main Module:
bpy::object offsetter_module;

// Functions:
bpy::object calc_fn;
bpy::object format_fn;
bpy::object calc_format_fn;

int load_python_module() {
    offsetter_module = bpy::import(PY_OFFSETTER_PATH);
    calc_fn = offsetter_module.attr(CALC_FN);
    format_fn = offsetter_module.attr(FORMAT_FN);
    calc_format_fn = offsetter_module.attr(CALC_FORMAT_FN);
    return 0;
}
void unload_python_module() {
    // ??
}
std::string py_eval_calc_simple(std::string eval_statement) {
    return bpy::call<std::string>(calc_format_fn.ptr(), eval_statement);
    // bpy::object result = bpy::call<bpy::object>(calc_fn.ptr(), eval_statement);
    // bpy::object result = bpy::call<void>(calc_fn.ptr(), eval_statement);
    // return bpy::call<std::string>(format_fn.ptr(), result); 
}

// bpy::object py_eval(std::string eval_statement) {
//     bpy::object result = bpy::call<bpy::object>(calc_fn.ptr(), eval_statement);
//     return bpy::call<std::string>(format_fn.ptr(), result); 
// }





#else
PyObject* py_module;
PyObject* py_calculate_formatted_response_fn;
PyObject* py_calculate_response_fn;
PyObject* py_format_response_fn;

int load_python_module() {
    PyObject* pName = PyUnicode_DecodeFSDefault(PY_MAIN_PATH);
    py_module = PyImport_Import(pName);
    Py_DECREF(pName);

    py_calculate_response_fn = PyObject_GetAttrString(py_module, "calculate_response");
    py_format_response_fn = PyObject_GetAttrString(py_module, "format_response");
    py_calculate_formatted_response_fn = PyObject_GetAttrString(py_module, "calculate_formatted_response");
    if (
        py_calculate_formatted_response_fn && PyCallable_Check(py_calculate_formatted_response_fn)
        && py_calculate_formatted_response_fn && PyCallable_Check(py_calculate_formatted_response_fn)
        && py_calculate_formatted_response_fn && PyCallable_Check(py_calculate_formatted_response_fn)
    ) {
        return 0;
    }
    std::cout << "ERROR: PYTHON MODULE NOT FOUND!";
    return 1;
}

void unload_python_module() {
    Py_DECREF(py_calculate_formatted_response_fn);
}

// PyObject* eval_calc(std::string eval_statement) {
std::string py_eval_calc_simple(std::string eval_statement) {
    // PyObject* py_args;
    PyObject* py_args = PyTuple_New(1);
    // std::string py_args_string = "(\'\'\'" + eval_statement + "\'\'\'";
    // PyArg_ParseTuple(py_args, py_args_string.c_str());
    // PyTuple_SetItem(py_args, 0, PyBytes_FromString(eval_statement.c_str()));
    PyTuple_SetItem(py_args, 0, PyUnicode_FromString(eval_statement.c_str()));

    PyObject* result = PyObject_CallObject(py_calculate_formatted_response_fn, py_args);
    // std::cout << result;
    std::string result_str = std::string(PyUnicode_AsUTF8(result));
    Py_DECREF(py_args);
    Py_DECREF(result);

    return result_str;
    // return "";
}
#endif