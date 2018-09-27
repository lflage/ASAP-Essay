# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 18:41:26 2018

@author: Lucas Fonseca Lage
"""
import os

lista_prompts = []

for dirpath, dirnames, filenames in os.walk(os.getcwd() + "\Essay_prompts"):
    for filename in filenames:
            file = open(os.path.normpath(os.path.join(dirpath,filename)), 'r') 
            lista_prompts.append(file.read())

def get_prompt(essay_set):
    essay_set -= 1                      
    return lista_prompts[essay_set]
    
            
            
