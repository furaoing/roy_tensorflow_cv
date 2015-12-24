# -*- coding: utf-8 -*-
__author__ = 'Taikor'

from .file_converter_baseClass import converter


def json_obj_to_excel(json_object, xlsx_path):
    con = converter(json_object, xlsx_path)
    new_path = con()
    return new_path
