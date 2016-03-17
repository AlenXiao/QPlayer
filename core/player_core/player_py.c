#include <Python.h>
#include "player.h"

static PyObject * cp_load_file_py(PyObject *self, PyObject *args) {
    const char *file_path;
    CPlayer *cp;
    if (!PyArg_ParseTuple(args, "s", &file_path)) {
        return Py_BuildValue("i", 0);
    }
    cp = cp_load_file(file_path);
    return Py_BuildValue("i", 1);
}

static PyObject * cp_free_player_py(PyObject *self, PyObject *args) {
    cp_free_player();
    return Py_BuildValue("i", 1);
}

static PyObject * cp_pause_audio_py(PyObject *self, PyObject *args) {
    cp_pause_audio();
    return Py_BuildValue("i", 1);
}

static PyObject * cp_stop_audio_py(PyObject *self, PyObject *args) {
    cp_stop_audio();
    return Py_BuildValue("i", 1);
}

static PyObject * cp_get_time_length_py(PyObject *self, PyObject *args) {
    int length;
    length = cp_get_time_length();
    printf("cp_get_length %d\n", length);
    return Py_BuildValue("i", length);
}

static PyObject * cp_get_current_time_pos_py(PyObject *self, PyObject *args) {
    double pos;
    pos = cp_get_current_time_pos();
    printf("cp_get_current_time_pos %f\n", pos);
    return Py_BuildValue("f", pos);
}

static PyObject * cp_is_stopping_py(PyObject *self, PyObject *args) {
    int st;
    st = cp_is_stopping();
    return Py_BuildValue("i", st);
}

static PyMethodDef CPlayerMethods[] = {
    {"cp_load_file_py",  cp_load_file_py, METH_VARARGS, "Open file_path and play."},
    {"cp_free_player_py",  cp_free_player_py, METH_VARARGS, "free player."},
    {"cp_pause_audio_py",  cp_pause_audio_py, METH_VARARGS, "free player."},
    {"cp_stop_audio_py",  cp_stop_audio_py, METH_VARARGS, "free player."},
    {"cp_get_time_length_py",  cp_get_time_length_py, METH_VARARGS, "free player."},
    {"cp_get_current_time_pos_py",  cp_get_current_time_pos_py, METH_VARARGS, "free player."},
    {"cp_is_stopping_py",  cp_is_stopping_py, METH_VARARGS, "free player."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initCPlayer(void) {
    (void) Py_InitModule("CPlayer", CPlayerMethods);
}

int main(int argc, char *argv[]) {
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initCPlayer();
    return 0;
}
