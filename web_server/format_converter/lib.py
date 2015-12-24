# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:17:09 2015

@author: Taikor
"""

import re
import json
import os

def kw_spam_detect(line, kwargs_rules, kwargs_field_position):  
    str_list = line.split('\t')
    
    spam = False    
    for key in kwargs_rules.keys():
        position = kwargs_field_position[key]
        for rule in kwargs_rules[key]:
            if re.search(rule, str_list[position]):
                spam = True
                break
                # if find spam language component in any field of the line, jump out and return True
            else:
                pass
        if spam == True:
            break
        else:
            pass
    
    return spam

def len_spam_detect(line, field_position, min_len):
    str_list = line.split('\t')
    
    field = str_list[field_position]
    if len(field) < min_len:
        return True
    else:
        return False
    
def read_from_json(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        string = f.read()
    
    return json.loads(string)
    
def retrive_basename(file_path):
    return os.path.basename(file_path)
    
def retrive_dirname(file_path):
    return os.path.dirname(file_path)
    
def generate_newpath(prefix, file_path):
    filted_basename = prefix + retrive_basename(file_path)
    filted_dirname = retrive_dirname(file_path)
    if len(filted_dirname) > 0:
        f_path = filted_dirname + '\\' + filted_basename
    else:
        f_path = filted_basename
    return f_path