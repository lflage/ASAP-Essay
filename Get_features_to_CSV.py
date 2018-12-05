# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 10:07:34 2018

@author: lucas
"""


import pandas as pd
#from ASAP_essay import ASAP_essay
import ASAP_essay as asap
from textstat.textstat import textstat
from py4j.java_gateway import JavaGateway

# Primeiramente iniciamos a conexão com java para extração de erros gramaticais com o Language Tool
gg = JavaGateway.launch_gateway(classpath="./Java/errorslanguagetool.jar;./Java/LanguageTool-4.3;./Java/py4j0.10.8.1.jar;./Java/LanguageTool-4.3/languagetool.jar")



# Leitura do dataset ASAP 
valid_set = pd.read_csv("./Dados ASAP/training_set_rel3.tsv", sep = '\t+', engine = 'python')

feature_df = pd.DataFrame()

for index, row in valid_set.iterrows():
    """Colocando o id de cada essay no dataframe"""
    feature_df.loc[index,'essay_id'] = valid_set['essay_id'][index]
    
    """pre processando o essay"""
    Y = asap.pre_process(valid_set['essay'][index])
    
    """extração de features sobre tokens"""
    token_feature_tp = asap.token_features(Y)
    feature_df.loc[index,'nb_of_tokens'] = token_feature_tp[0]                  #F1
    feature_df.loc[index,'mean_char_p_words'] = token_feature_tp[1]             #F2
    feature_df.loc[index,'diff_words'] = token_feature_tp[2]                    #F3
    
    """Features de sentença"""
    feature_df.loc[index,'optimal_sentences'] = asap.nb_optimal_sentence(Y)     #F4
    
    """Erros de ortografia"""
    feature_df.loc[index,'nb_of_spell_errors'] = asap.nb_of_speliing_errors(Y)  #F5
    feature_df.loc[index,'spell_errors_p_token'] = feature_df['nb_of_spell_errors'][index]/token_feature_tp[0]      #F6
    
    """Flesch Score"""
    feature_df.loc[index,'flesch_score'] = textstat.flesch_reading_ease(Y)      #F7
    
    """Distância cosseno entre o essay e o prompt"""
    feature_df.loc[index,'cos_dist'] = asap.get_cos_dist(Y,valid_set['essay_set'][index])       #F8
    
    """Erros gramaticais e de estilo com o LanguageTool"""
    extract = gg.jvm.languagetoolEnglish.ExtractErrors()
    errors = extract.getErrors()
    errors.process(Y)
    
    feature_df.loc[index,'style_errors'] = errors.getStyleErrors()              #F9
    feature_df.loc[index,'grammar_errors'] = errors.getOthersErrors()           #F10
    feature_df.loc[index,'grammar_errors_p_token'] = feature_df['grammar_errors'][index]/token_feature_tp[0]    #F11

    """Features de marcadores de discurso"""
    discourse_marker_tp = asap.discourse_markers_features(Y)
    feature_df.loc[index,'discourse_markers'] = discourse_marker_tp[0]              #F12
    feature_df.loc[index,'discourse_markers_p_sentence'] = discourse_marker_tp[1]   #F13
    
    print(index)
feature_df.to_csv('./ASAP_feature_table.csv', index = False)
