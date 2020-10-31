#include <iostream>

#include <Python.h>
// #include <boost/python.hpp>
#include <boost/filesystem.hpp>
#include <boost/foreach.hpp>

#include "py_loader.h"

// #ifdef DEBUG
#define PY_MAIN_PATH "main"
// #endif


PyObject* py_module;
PyObject* py_calculate_formatted_response_fn;
PyObject* py_calculate_response_fn;
PyObject* py_formatt_response_fn;

int load_python_module() {
    PyObject* pName = PyUnicode_DecodeFSDefault(PY_MAIN_PATH);
    py_module = PyImport_Import(pName);
    Py_DECREF(pName);

    py_calculate_formatted_response_fn = PyObject_GetAttrString(py_module, "calculate_formatted_response");
    if (py_calculate_formatted_response_fn && PyCallable_Check(py_calculate_formatted_response_fn)) {
        return 0;
    }
    std::cout << "ERROR: PYTHON MODULE NOT FOUND!";
    return 0;
}

void unload_python_module() {
    Py_DECREF(py_calculate_formatted_response_fn);
}

// PyObject* eval_calc(std::string eval_statement) {
std::string py_eval_calc(std::string eval_statement) {
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