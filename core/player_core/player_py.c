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
    return Py_BuildValue("i", length);
}

static PyObject * cp_get_current_time_pos_py(PyObject *self, PyObject *args) {
    double pos;
    pos = cp_get_current_time_pos();
    return Py_BuildValue("f", pos);
}

static PyObject * cp_is_stopping_py(PyObject *self, PyObject *args) {
    int st;
    st = cp_is_stopping();
    return Py_BuildValue("i", st);
}

static PyObject * cp_seek_audio_by_sec_py(PyObject *self, PyObject *args) {
    int sec;
    if (!PyArg_ParseTuple(args, "i", &sec)) {
        return Py_BuildValue("i", 0);
    }
    cp_seek_audio_by_sec(sec);
    return Py_BuildValue("i", 1);
}

static PyObject * cp_is_alive_py(PyObject *self, PyObject *args) {
    int status = 0;
    if (global_cplayer_ctx != NULL) {
        status = 1;
    }
    return Py_BuildValue("i", status);
}

static PyObject * cp_get_metadata_py(PyObject *self, PyObject *args) {
    const char *file_path;
    PyObject *dict;
    PyObject *v;
    SongInfo *info = (SongInfo *)malloc(sizeof(SongInfo));
    dict = Py_BuildValue("{}");
    if (!PyArg_ParseTuple(args, "s", &file_path)) {
        goto rt;
    }
    int state = extract_meta_data((char *)file_path, info);
    v = Py_BuildValue("s", info->title);
    PyMapping_SetItemString(dict, "title", v);
    v = Py_BuildValue("s", info->album);
    PyMapping_SetItemString(dict, "album", v);
    v = Py_BuildValue("s", info->artist);
    PyMapping_SetItemString(dict, "artist", v);
    v = Py_BuildValue("s", info->genre);
    PyMapping_SetItemString(dict, "genre", v);
    v = Py_BuildValue("s", info->track);
    PyMapping_SetItemString(dict, "track", v);
    v = Py_BuildValue("s", info->date);
    PyMapping_SetItemString(dict, "date", v);
rt:
    return dict;
}

static PyObject * cp_set_volume_py(PyObject *self, PyObject *args) {
    int volume = 0;
    if (!PyArg_ParseTuple(args, "i", &volume)) {
        goto rt;
    }
    cp_set_volume(volume);
rt:
    return Py_BuildValue("i", 1);
}

static PyMethodDef CPlayerMethods[] = {
    {"cp_load_file_py",  cp_load_file_py, METH_VARARGS, "Open file_path and play."},
    {"cp_free_player_py",  cp_free_player_py, METH_VARARGS, "free player."},
    {"cp_pause_audio_py",  cp_pause_audio_py, METH_VARARGS, "free player."},
    {"cp_stop_audio_py",  cp_stop_audio_py, METH_VARARGS, "free player."},
    {"cp_get_time_length_py",  cp_get_time_length_py, METH_VARARGS, "free player."},
    {"cp_get_current_time_pos_py",  cp_get_current_time_pos_py, METH_VARARGS, "free player."},
    {"cp_is_stopping_py",  cp_is_stopping_py, METH_VARARGS, "free player."},
    {"cp_seek_audio_by_sec_py",  cp_seek_audio_by_sec_py, METH_VARARGS, "free player."},
    {"cp_is_alive_py",  cp_is_alive_py, METH_VARARGS, "is_alive."},
    {"cp_get_metadata_py",  cp_get_metadata_py, METH_VARARGS, "metadata."},
    {"cp_set_volume_py",  cp_set_volume_py, METH_VARARGS, "set volume."},
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
