# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 21:33:32 2018

@author: lucas
"""

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import scipy
import re
import nltk.data
from textblob import Word
import expandContractions as eC
import discourseMarkers
import Prompts


def pre_process(essay):
    
    """Função que expande contrações, põe em caixa baixa e retira whitespace a mais"""
        
    essay_proc = eC.expandContractions(essay.lower())
    essay_proc = re.sub(' +', ' ',essay_proc)
    return essay_proc

def token_features(essay):
    
    """ Utiliza o objeto Vectorizer para extrair features relacionados a tokens"""
    vector = CountVectorizer()
    tokenized_essay = vector.fit_transform([essay])
    
    """Feature 1: Número de Tokens"""
    nb_of_tokens = tokenized_essay.toarray().sum()
    
    """Feature 2: Media de caracteres por palavra"""
    nb_of_char = 0
    for position,item in enumerate(vector.get_feature_names()):
        nb_of_char += len(item)* tokenized_essay.toarray()[0][position]			# multiplica o tamanho da string(token) pela sua frequência
    mean_char_p_word = nb_of_char/nb_of_tokens
    
    """Feature 3: Número de palavras diferentes """
    nb_dif_words = len(vector.get_feature_names())
        
    return (nb_of_tokens,mean_char_p_word,nb_dif_words)	

def nb_of_speliing_errors(essay):
    
    """Feature 4: Utiliza a bilbioteca textblob para correção de erros de ortografia"""
    essay = re.sub('@\S+','',essay)                                                 # Retira nomes padrão do ASAP iniciados em @
    
    vector = CountVectorizer()
    vector.fit_transform([essay])
    
    list_tokens = vector.get_feature_names()
    
    spell_errors = 0    
    for i in list_tokens:
        __result = None
        __result = re.search('@\S+', i) 										# retira nomes padrão do ASAP como @Location
        if __result is None:
            w = Word(i)														    # da biblioteca textblob
            result_tuple = w.spellcheck()									    # o método spellcheck() returna uma tupla com a sugestão de correção e o nível de certeza em %
            if i != result_tuple[0][0] and result_tuple[0][1] == 1.0:			# só faz correções que o corretor tem certeza, 100%, evita sugestão de singular em formas plurais
                spell_errors += 1
    nb_of_spell_errors = spell_errors
    return nb_of_spell_errors

def get_cos_dist(essay,prompt_number):
    
    """Feature 5: Retorna a distância cosseno de dois textos usando Scikit"""
    __vectorizer = CountVectorizer()                                    		  
    red_promp = [essay,Prompts.get_prompt(prompt_number)]      		              # O CountVectorizer() cria duas arrays de frequências de palavras do
    y = __vectorizer.fit_transform(red_promp)                          		      # vocabulário do essay e do prompt
    x = y.toarray()
    transformer = TfidfTransformer(smooth_idf=False)
    tfidf = transformer.fit_transform(x)										  # Faz as operações do TF.IDF
    z = tfidf.toarray()
    cosine_distance = scipy.spatial.distance.cosine(z[0], z[1])
    return cosine_distance

def discourse_markers_features(essay):
    
    """Feature 6: Numero de marcadores de discurso na redação"""
    
    counter=0
    for discourse_marker in discourseMarkers.multi_word_expression():
        result = None
        result = discourse_marker.findall(essay)
        re.sub(discourse_marker,'',essay)
        counter += len(result)
        
    for discourse_marker in discourseMarkers.discourseMarkers():
        matches = None
        searchable_pattern = "\W" + discourse_marker + '\W'
        matches = re.findall(searchable_pattern,essay.lower())
        if matches != None:
            counter += len(matches)
    nb_of_discourse_markers = counter
    
    """Feature 7: Número de marcadores de discurso por frase"""
    
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')					
    n_of_sentences = len(sent_detector.tokenize(essay))
    discourse_markers_p_sentence = nb_of_discourse_markers/n_of_sentences
    
    return (nb_of_discourse_markers,discourse_markers_p_sentence)

def nb_optimal_sentence(essay):
    
    """Feature 8: Numero de frases com 15 a 20 palavras"""
    counter = 0
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')						# Sentence Tokenizer do NLKT
    essay_sentence_list = sent_detector.tokenize(essay)			
	  # essay_sentence_list é uma Lista de tokens(frases)
    for i in essay_sentence_list:
        n_words_sentence = len(i.split())
        if n_words_sentence >= 15 and n_words_sentence <= 20:
            counter +=1
        nb_of_optimal_sentences = counter
    return nb_of_optimal_sentences


