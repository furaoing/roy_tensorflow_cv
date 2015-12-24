# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 17:01:29 2015

@author: Taikor
"""


import xlrd
import xlsxwriter


class converter:
    def __init__(self, json_object, xlsx_path):
        self.json_object = json_object
        self.xlsx_path = xlsx_path

    def json_obj_to_xls_converter(self):
        workbook = xlsxwriter.Workbook(self.xlsx_path)  # create a new xlsx file
        worksheet = workbook.add_worksheet()
          
        row = 0
        for dict_obj in self.json_object:
            col = 0
            for key, value in dict_obj.items():
                value = str(value)
                value = unicode(value, encoding="utf8")
                worksheet.write(row, col, value)
                col += 1
            row += 1
        workbook.close()
        
        return self.xlsx_path
                      
    def __call__(self):
        return self.json_obj_to_xls_converter()
