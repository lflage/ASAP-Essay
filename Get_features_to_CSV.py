# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 10:07:34 2018

@author: lucas
"""
import pandas as pd
from ASAP_essay import ASAP_essay
# import time

valid_set = pd.read_csv("./Dados ASAP/training_set_rel3.tsv", sep = '\t+', engine = 'python')

feature_df = pd.DataFrame()

for index, row in valid_set[:100].iterrows():
    X = ASAP_essay(valid_set['essay'][index],valid_set['essay_set'][index])
    feature_df.loc[index,'essay_id'] = valid_set['essay_id'][index]
    feature_df.loc[index,'nb_of_tokens'] = X.get_nb_of_tokens()
    feature_df.loc[index,'mean_char_p_words'] = X.get_mean_char_p_word()
    feature_df.loc[index,'diff_words'] = X.get_nb_of_diff_words()
    feature_df.loc[index,'optimal_sentences'] = X.get_nb_of_optimal_sentences()
    feature_df.loc[index,'nb_of_spell_errors'] = X.get_nb_of_speliing_errors()
    feature_df.loc[index,'flesch_score'] = X.get_flesch_score()
    feature_df.loc[index,'cos_dist'] = X.get_cos_dist()
    
    feature_df.loc[index,'style_errors'] = X.get_style_errors_LT()    
    feature_df.loc[index,'grammar_errors'] = X.get_nb_of_grammar_errors_LT()
    
    feature_df.loc[index,'nb_of_spell_errors'] = X.get_nb_of_speliing_errors()
    feature_df.loc[index,'discourse_markers'] = X.get_nb_of_discourse_markers()
    feature_df.loc[index,'grammar_errors_p_token'] = X.get_grammar_errors_p_token_n()
    feature_df.loc[index,'spell_errors_p_token'] = X.get_n_spell_errors_p_token_n()
    feature_df.loc[index,'discourse_markers_p_sentence'] = X.get_n_discourse_markers_p_sentence()
    
    
    print(index)
    
    
feature_df.to_csv('./test.csv', index = False)