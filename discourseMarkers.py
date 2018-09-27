# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 18:28:20 2018

@author: lucas
"""
import pandas as pd
import re
import os

d_m = pd.read_csv(os.getcwd() + "\discoursemarkers.txt", sep = '\n', engine = "python", header = None)

discourse_markers = pd.Series(d_m[0])
discourse_markers = discourse_markers.apply(lambda x: x.strip())
discourse_markers = discourse_markers.apply(lambda x: x.lower())
    
def discourseMarkers():
    return discourse_markers

def multi_word_exp():
    x = (re.compile("(either)[^\.\!\?]+(or)"),re.compile("(if)[^\.\!\?]+(then)"),
           re.compile("(neither)[^\.\!\?]+(nor)"),re.compile("(on one hand)[^\.\!\?]+(on the other hand)"))
    return x