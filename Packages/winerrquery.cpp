#include <Windows.h>
extern "C" {
    #define PY_SSIZE_T_CLEAN
    #define Py_LIMITED_API 0x03050000
    #include <Python.h>
    PyDoc_STRVAR(winerrquery_query_doc, "query(code: int, language: Optional[int]=None) -> Optional[str]\nQuery Windows Errno Message.\nParameter `code` is from 0x0 to 0xFFFFFFFF.\nParameter `lang` is a LANG_* constant. Default None.\nNote: if `lang` is None, the message will use your System Language.\nReturns None if the message is not found.");
    PyObject* winerrquery_query(PyObject* self, PyObject* args, PyObject* kwargs) {
        PyObject* obj = NULL;
        unsigned long code = 0;
        PyObject* language = Py_None;
        static char* keywords[] = {"code", "language", NULL};
        if (!PyArg_ParseTupleAndKeywords(args, kwargs, "k|O", keywords, &code, &language)) {
            return NULL;
        }
        if (code < 0) {
            PyErr_SetString(PyExc_ValueError, "Invalid ierr. 0 <= ierr <= 0xFFFFFFFF");
            PyErr_Print();
            return NULL;
        }
        else {
            int len = 0;
            DWORD err = (DWORD)code;
            WCHAR* result = NULL;
            if (language == NULL) {
                language = Py_None;
            }
            if (language == Py_None) {
                language = PyLong_FromLong(LANG_NEUTRAL);
            }
            if (PyLong_Check(language)) {
                len = FormatMessageW(
                    FORMAT_MESSAGE_ALLOCATE_BUFFER |
                    FORMAT_MESSAGE_FROM_SYSTEM |
                    FORMAT_MESSAGE_IGNORE_INSERTS,
                    NULL,
                    err,
                    MAKELANGID((DWORD)PyLong_AsUnsignedLong(language), SUBLANG_DEFAULT),
                    (LPWSTR)&result,
                    0,
                    NULL
                );
            } else {
                PyErr_SetString(PyExc_TypeError, "`language` must be int or None.");
                PyErr_Print();
                return NULL;
            }
            if (len == 0) {
                return Py_None;
            }
            else {
                PyObject* message = PyUnicode_FromWideChar(result, len);
                if (message == NULL) {
                    return Py_None;
                }
                return message;
            }
        }
        Py_RETURN_NONE;
    }
    static PyMethodDef winerrquery_functions[] = {
        {"query", (PyCFunction)winerrquery_query, METH_VARARGS | METH_KEYWORDS, winerrquery_query_doc},
        {NULL, NULL, 0, NULL}
    };
    int exec_winerrquery(PyObject* module) {
        PyModule_AddFunctions(module, winerrquery_functions);
        PyModule_AddObject(module, "LANG_NEUTRAL", PyLong_FromUnsignedLong(LANG_NEUTRAL));
        PyModule_AddObject(module, "LANG_INVARIANT", PyLong_FromUnsignedLong(LANG_INVARIANT));
        PyModule_AddObject(module, "LANG_AFRIKAANS", PyLong_FromUnsignedLong(LANG_AFRIKAANS));
        PyModule_AddObject(module, "LANG_ALBANIAN", PyLong_FromUnsignedLong(LANG_ALBANIAN));
        PyModule_AddObject(module, "LANG_ALSATIAN", PyLong_FromUnsignedLong(LANG_ALSATIAN));
        PyModule_AddObject(module, "LANG_AMHARIC", PyLong_FromUnsignedLong(LANG_AMHARIC));
        PyModule_AddObject(module, "LANG_ARABIC", PyLong_FromUnsignedLong(LANG_ARABIC));
        PyModule_AddObject(module, "LANG_ARMENIAN", PyLong_FromUnsignedLong(LANG_ARMENIAN));
        PyModule_AddObject(module, "LANG_ASSAMESE", PyLong_FromUnsignedLong(LANG_ASSAMESE));
        PyModule_AddObject(module, "LANG_AZERI", PyLong_FromUnsignedLong(LANG_AZERI));
        PyModule_AddObject(module, "LANG_AZERBAIJANI", PyLong_FromUnsignedLong(LANG_AZERBAIJANI));
        PyModule_AddObject(module, "LANG_BANGLA", PyLong_FromUnsignedLong(LANG_BANGLA));
        PyModule_AddObject(module, "LANG_BASHKIR", PyLong_FromUnsignedLong(LANG_BASHKIR));
        PyModule_AddObject(module, "LANG_BASQUE", PyLong_FromUnsignedLong(LANG_BASQUE));
        PyModule_AddObject(module, "LANG_BELARUSIAN", PyLong_FromUnsignedLong(LANG_BELARUSIAN));
        PyModule_AddObject(module, "LANG_BENGALI", PyLong_FromUnsignedLong(LANG_BENGALI));
        PyModule_AddObject(module, "LANG_BRETON", PyLong_FromUnsignedLong(LANG_BRETON));
        PyModule_AddObject(module, "LANG_BOSNIAN", PyLong_FromUnsignedLong(LANG_BOSNIAN));
        PyModule_AddObject(module, "LANG_BOSNIAN_NEUTRAL", PyLong_FromUnsignedLong(LANG_BOSNIAN_NEUTRAL));
        PyModule_AddObject(module, "LANG_BULGARIAN", PyLong_FromUnsignedLong(LANG_BULGARIAN));
        PyModule_AddObject(module, "LANG_CATALAN", PyLong_FromUnsignedLong(LANG_CATALAN));
        PyModule_AddObject(module, "LANG_CENTRAL_KURDISH", PyLong_FromUnsignedLong(LANG_CENTRAL_KURDISH));
        PyModule_AddObject(module, "LANG_CHEROKEE", PyLong_FromUnsignedLong(LANG_CHEROKEE));
        PyModule_AddObject(module, "LANG_CHINESE", PyLong_FromUnsignedLong(LANG_CHINESE));
        PyModule_AddObject(module, "LANG_CHINESE_SIMPLIFIED", PyLong_FromUnsignedLong(LANG_CHINESE_SIMPLIFIED));
        PyModule_AddObject(module, "LANG_CHINESE_TRADITIONAL", PyLong_FromUnsignedLong(LANG_CHINESE_TRADITIONAL));
        PyModule_AddObject(module, "LANG_CORSICAN", PyLong_FromUnsignedLong(LANG_CORSICAN));
        PyModule_AddObject(module, "LANG_CROATIAN", PyLong_FromUnsignedLong(LANG_CROATIAN));
        PyModule_AddObject(module, "LANG_CZECH", PyLong_FromUnsignedLong(LANG_CZECH));
        PyModule_AddObject(module, "LANG_DANISH", PyLong_FromUnsignedLong(LANG_DANISH));
        PyModule_AddObject(module, "LANG_DARI", PyLong_FromUnsignedLong(LANG_DARI));
        PyModule_AddObject(module, "LANG_DIVEHI", PyLong_FromUnsignedLong(LANG_DIVEHI));
        PyModule_AddObject(module, "LANG_DUTCH", PyLong_FromUnsignedLong(LANG_DUTCH));
        PyModule_AddObject(module, "LANG_ENGLISH", PyLong_FromUnsignedLong(LANG_ENGLISH));
        PyModule_AddObject(module, "LANG_ESTONIAN", PyLong_FromUnsignedLong(LANG_ESTONIAN));
        PyModule_AddObject(module, "LANG_FAEROESE", PyLong_FromUnsignedLong(LANG_FAEROESE));
        PyModule_AddObject(module, "LANG_FARSI", PyLong_FromUnsignedLong(LANG_FARSI));
        PyModule_AddObject(module, "LANG_FILIPINO", PyLong_FromUnsignedLong(LANG_FILIPINO));
        PyModule_AddObject(module, "LANG_FINNISH", PyLong_FromUnsignedLong(LANG_FINNISH));
        PyModule_AddObject(module, "LANG_FRENCH", PyLong_FromUnsignedLong(LANG_FRENCH));
        PyModule_AddObject(module, "LANG_FRISIAN", PyLong_FromUnsignedLong(LANG_FRISIAN));
        PyModule_AddObject(module, "LANG_FULAH", PyLong_FromUnsignedLong(LANG_FULAH));
        PyModule_AddObject(module, "LANG_GALICIAN", PyLong_FromUnsignedLong(LANG_GALICIAN));
        PyModule_AddObject(module, "LANG_GEORGIAN", PyLong_FromUnsignedLong(LANG_GEORGIAN));
        PyModule_AddObject(module, "LANG_GERMAN", PyLong_FromUnsignedLong(LANG_GERMAN));
        PyModule_AddObject(module, "LANG_GREEK", PyLong_FromUnsignedLong(LANG_GREEK));
        PyModule_AddObject(module, "LANG_GREENLANDIC", PyLong_FromUnsignedLong(LANG_GREENLANDIC));
        PyModule_AddObject(module, "LANG_GUJARATI", PyLong_FromUnsignedLong(LANG_GUJARATI));
        PyModule_AddObject(module, "LANG_HAUSA", PyLong_FromUnsignedLong(LANG_HAUSA));
        PyModule_AddObject(module, "LANG_HAWAIIAN", PyLong_FromUnsignedLong(LANG_HAWAIIAN));
        PyModule_AddObject(module, "LANG_HEBREW", PyLong_FromUnsignedLong(LANG_HEBREW));
        PyModule_AddObject(module, "LANG_HINDI", PyLong_FromUnsignedLong(LANG_HINDI));
        PyModule_AddObject(module, "LANG_HUNGARIAN", PyLong_FromUnsignedLong(LANG_HUNGARIAN));
        PyModule_AddObject(module, "LANG_ICELANDIC", PyLong_FromUnsignedLong(LANG_ICELANDIC));
        PyModule_AddObject(module, "LANG_IGBO", PyLong_FromUnsignedLong(LANG_IGBO));
        PyModule_AddObject(module, "LANG_INDONESIAN", PyLong_FromUnsignedLong(LANG_INDONESIAN));
        PyModule_AddObject(module, "LANG_INUKTITUT", PyLong_FromUnsignedLong(LANG_INUKTITUT));
        PyModule_AddObject(module, "LANG_IRISH", PyLong_FromUnsignedLong(LANG_IRISH));
        PyModule_AddObject(module, "LANG_ITALIAN", PyLong_FromUnsignedLong(LANG_ITALIAN));
        PyModule_AddObject(module, "LANG_JAPANESE", PyLong_FromUnsignedLong(LANG_JAPANESE));
        PyModule_AddObject(module, "LANG_KANNADA", PyLong_FromUnsignedLong(LANG_KANNADA));
        PyModule_AddObject(module, "LANG_KASHMIRI", PyLong_FromUnsignedLong(LANG_KASHMIRI));
        PyModule_AddObject(module, "LANG_KAZAK", PyLong_FromUnsignedLong(LANG_KAZAK));
        PyModule_AddObject(module, "LANG_KHMER", PyLong_FromUnsignedLong(LANG_KHMER));
        PyModule_AddObject(module, "LANG_KICHE", PyLong_FromUnsignedLong(LANG_KICHE));
        PyModule_AddObject(module, "LANG_KINYARWANDA", PyLong_FromUnsignedLong(LANG_KINYARWANDA));
        PyModule_AddObject(module, "LANG_KONKANI", PyLong_FromUnsignedLong(LANG_KONKANI));
        PyModule_AddObject(module, "LANG_KOREAN", PyLong_FromUnsignedLong(LANG_KOREAN));
        PyModule_AddObject(module, "LANG_KYRGYZ", PyLong_FromUnsignedLong(LANG_KYRGYZ));
        PyModule_AddObject(module, "LANG_LAO", PyLong_FromUnsignedLong(LANG_LAO));
        PyModule_AddObject(module, "LANG_LATVIAN", PyLong_FromUnsignedLong(LANG_LATVIAN));
        PyModule_AddObject(module, "LANG_LITHUANIAN", PyLong_FromUnsignedLong(LANG_LITHUANIAN));
        PyModule_AddObject(module, "LANG_LOWER_SORBIAN", PyLong_FromUnsignedLong(LANG_LOWER_SORBIAN));
        PyModule_AddObject(module, "LANG_LUXEMBOURGISH", PyLong_FromUnsignedLong(LANG_LUXEMBOURGISH));
        PyModule_AddObject(module, "LANG_MACEDONIAN", PyLong_FromUnsignedLong(LANG_MACEDONIAN));
        PyModule_AddObject(module, "LANG_MALAY", PyLong_FromUnsignedLong(LANG_MALAY));
        PyModule_AddObject(module, "LANG_MALAYALAM", PyLong_FromUnsignedLong(LANG_MALAYALAM));
        PyModule_AddObject(module, "LANG_MALTESE", PyLong_FromUnsignedLong(LANG_MALTESE));
        PyModule_AddObject(module, "LANG_MANIPURI", PyLong_FromUnsignedLong(LANG_MANIPURI));
        PyModule_AddObject(module, "LANG_MAORI", PyLong_FromUnsignedLong(LANG_MAORI));
        PyModule_AddObject(module, "LANG_MAPUDUNGUN", PyLong_FromUnsignedLong(LANG_MAPUDUNGUN));
        PyModule_AddObject(module, "LANG_MARATHI", PyLong_FromUnsignedLong(LANG_MARATHI));
        PyModule_AddObject(module, "LANG_MOHAWK", PyLong_FromUnsignedLong(LANG_MOHAWK));
        PyModule_AddObject(module, "LANG_MONGOLIAN", PyLong_FromUnsignedLong(LANG_MONGOLIAN));
        PyModule_AddObject(module, "LANG_NEPALI", PyLong_FromUnsignedLong(LANG_NEPALI));
        PyModule_AddObject(module, "LANG_NORWEGIAN", PyLong_FromUnsignedLong(LANG_NORWEGIAN));
        PyModule_AddObject(module, "LANG_OCCITAN", PyLong_FromUnsignedLong(LANG_OCCITAN));
        PyModule_AddObject(module, "LANG_ODIA", PyLong_FromUnsignedLong(LANG_ODIA));
        PyModule_AddObject(module, "LANG_ORIYA", PyLong_FromUnsignedLong(LANG_ORIYA));
        PyModule_AddObject(module, "LANG_PASHTO", PyLong_FromUnsignedLong(LANG_PASHTO));
        PyModule_AddObject(module, "LANG_PERSIAN", PyLong_FromUnsignedLong(LANG_PERSIAN));
        PyModule_AddObject(module, "LANG_POLISH", PyLong_FromUnsignedLong(LANG_POLISH));
        PyModule_AddObject(module, "LANG_PORTUGUESE", PyLong_FromUnsignedLong(LANG_PORTUGUESE));
        PyModule_AddObject(module, "LANG_PULAR", PyLong_FromUnsignedLong(LANG_PULAR));
        PyModule_AddObject(module, "LANG_PUNJABI", PyLong_FromUnsignedLong(LANG_PUNJABI));
        PyModule_AddObject(module, "LANG_QUECHUA", PyLong_FromUnsignedLong(LANG_QUECHUA));
        PyModule_AddObject(module, "LANG_ROMANIAN", PyLong_FromUnsignedLong(LANG_ROMANIAN));
        PyModule_AddObject(module, "LANG_ROMANSH", PyLong_FromUnsignedLong(LANG_ROMANSH));
        PyModule_AddObject(module, "LANG_RUSSIAN", PyLong_FromUnsignedLong(LANG_RUSSIAN));
        PyModule_AddObject(module, "LANG_SAKHA", PyLong_FromUnsignedLong(LANG_SAKHA));
        PyModule_AddObject(module, "LANG_SAMI", PyLong_FromUnsignedLong(LANG_SAMI));
        PyModule_AddObject(module, "LANG_SANSKRIT", PyLong_FromUnsignedLong(LANG_SANSKRIT));
        PyModule_AddObject(module, "LANG_SCOTTISH_GAELIC", PyLong_FromUnsignedLong(LANG_SCOTTISH_GAELIC));
        PyModule_AddObject(module, "LANG_SERBIAN", PyLong_FromUnsignedLong(LANG_SERBIAN));
        PyModule_AddObject(module, "LANG_SERBIAN_NEUTRAL", PyLong_FromUnsignedLong(LANG_SERBIAN_NEUTRAL));
        PyModule_AddObject(module, "LANG_SINDHI", PyLong_FromUnsignedLong(LANG_SINDHI));
        PyModule_AddObject(module, "LANG_SINHALESE", PyLong_FromUnsignedLong(LANG_SINHALESE));
        PyModule_AddObject(module, "LANG_SLOVAK", PyLong_FromUnsignedLong(LANG_SLOVAK));
        PyModule_AddObject(module, "LANG_SLOVENIAN", PyLong_FromUnsignedLong(LANG_SLOVENIAN));
        PyModule_AddObject(module, "LANG_SOTHO", PyLong_FromUnsignedLong(LANG_SOTHO));
        PyModule_AddObject(module, "LANG_SPANISH", PyLong_FromUnsignedLong(LANG_SPANISH));
        PyModule_AddObject(module, "LANG_SWAHILI", PyLong_FromUnsignedLong(LANG_SWAHILI));
        PyModule_AddObject(module, "LANG_SWEDISH", PyLong_FromUnsignedLong(LANG_SWEDISH));
        PyModule_AddObject(module, "LANG_SYRIAC", PyLong_FromUnsignedLong(LANG_SYRIAC));
        PyModule_AddObject(module, "LANG_TAJIK", PyLong_FromUnsignedLong(LANG_TAJIK));
        PyModule_AddObject(module, "LANG_TAMAZIGHT", PyLong_FromUnsignedLong(LANG_TAMAZIGHT));
        PyModule_AddObject(module, "LANG_TAMIL", PyLong_FromUnsignedLong(LANG_TAMIL));
        PyModule_AddObject(module, "LANG_TATAR", PyLong_FromUnsignedLong(LANG_TATAR));
        PyModule_AddObject(module, "LANG_TELUGU", PyLong_FromUnsignedLong(LANG_TELUGU));
        PyModule_AddObject(module, "LANG_THAI", PyLong_FromUnsignedLong(LANG_THAI));
        PyModule_AddObject(module, "LANG_TIBETAN", PyLong_FromUnsignedLong(LANG_TIBETAN));
        PyModule_AddObject(module, "LANG_TIGRIGNA", PyLong_FromUnsignedLong(LANG_TIGRIGNA));
        PyModule_AddObject(module, "LANG_TIGRINYA", PyLong_FromUnsignedLong(LANG_TIGRINYA));
        PyModule_AddObject(module, "LANG_TSWANA", PyLong_FromUnsignedLong(LANG_TSWANA));
        PyModule_AddObject(module, "LANG_TURKISH", PyLong_FromUnsignedLong(LANG_TURKISH));
        PyModule_AddObject(module, "LANG_TURKMEN", PyLong_FromUnsignedLong(LANG_TURKMEN));
        PyModule_AddObject(module, "LANG_UIGHUR", PyLong_FromUnsignedLong(LANG_UIGHUR));
        PyModule_AddObject(module, "LANG_UKRAINIAN", PyLong_FromUnsignedLong(LANG_UKRAINIAN));
        PyModule_AddObject(module, "LANG_UPPER_SORBIAN", PyLong_FromUnsignedLong(LANG_UPPER_SORBIAN));
        PyModule_AddObject(module, "LANG_URDU", PyLong_FromUnsignedLong(LANG_URDU));
        PyModule_AddObject(module, "LANG_UZBEK", PyLong_FromUnsignedLong(LANG_UZBEK));
        PyModule_AddObject(module, "LANG_VALENCIAN", PyLong_FromUnsignedLong(LANG_VALENCIAN));
        PyModule_AddObject(module, "LANG_VIETNAMESE", PyLong_FromUnsignedLong(LANG_VIETNAMESE));
        PyModule_AddObject(module, "LANG_WELSH", PyLong_FromUnsignedLong(LANG_WELSH));
        PyModule_AddObject(module, "LANG_WOLOF", PyLong_FromUnsignedLong(LANG_WOLOF));
        PyModule_AddObject(module, "LANG_XHOSA", PyLong_FromUnsignedLong(LANG_XHOSA));
        PyModule_AddObject(module, "LANG_YAKUT", PyLong_FromUnsignedLong(LANG_YAKUT));
        PyModule_AddObject(module, "LANG_YI", PyLong_FromUnsignedLong(LANG_YI));
        PyModule_AddObject(module, "LANG_YORUBA", PyLong_FromUnsignedLong(LANG_YORUBA));
        PyModule_AddObject(module, "LANG_ZULU", PyLong_FromUnsignedLong(LANG_ZULU));
        return 0;
    }
    PyDoc_STRVAR(winerrquery_doc, "The winerrquery module provides a function to query Windows Errno Message.");
    static PyModuleDef_Slot winerrquery_slots[] = {
        { Py_mod_exec, exec_winerrquery },
        { 0, NULL }
    };
    static PyModuleDef winerrquery_def = {
        PyModuleDef_HEAD_INIT,
        "winerrquery",
        winerrquery_doc,
        0,
        NULL,
        winerrquery_slots,
        NULL,
        NULL,
        NULL,
    };
    PyMODINIT_FUNC PyInit_winerrquery() {
        return PyModuleDef_Init(&winerrquery_def);
    }
}
