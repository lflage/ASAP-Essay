# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 15:54:26 2018

@author: lucas
"""
from py4j.java_gateway import JavaGateway
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import scipy
import re
import nltk.data
from textblob import Word
import expandContractions as eC
from textstat.textstat import textstat
import discourseMarkers
import Prompts
# =============================================================================
# import requests
# =============================================================================



class ASAP_essay():
    """classe para extração de features em uma redação do database ASAP"""
    
    def __init__(self,essay,prompt_number):     # entra com o essay e o essay_set do DataFrame

        
        self.essay = essay
        self.prompt_number = prompt_number
        self.nb_of_tokens = 0
        self.cosine_distance = 0
        self.nb_of_grammar_errors = 0
        self.nb_of_spell_errors = 0
        self.nb_of_optimal_sentences = 0
        self.mean_char_p_word = 0
        self.flesch_score = 0
        self.nb_of_discourse_markers = 0
        self.nb_of_diff_words = 0
        self.grammar_errors_p_token = 0
        self.spell_errors_p_token = 0
        self.discourse_markers_p_sentence = 0
        self.style_errors = 0
        
        to_tokenize = eC.expandContractions(self.essay.lower())
        to_tokenize = re.sub(' +', ' ',to_tokenize)
        self.vector = CountVectorizer()
        self.tokenized_essay = self.vector.fit_transform([to_tokenize])
        
        """Inicializa o LanguageTool para recolher erros"""
        self.gg = JavaGateway.launch_gateway(classpath="./Java/errorslanguagetool.jar;./Java/LanguageTool-4.3;./Java/py4j0.10.8.1.jar;./Java/LanguageTool-4.3/languagetool.jar")
        self.extract = self.gg.jvm.languagetoolEnglish.ExtractErrors()
        self.errors = self.extract.getErrors()
        self.errors.process(self.essay)
        
        
    def get_nb_of_tokens(self):
        self.nb_of_tokens = self.tokenized_essay.toarray().sum()						# Soma todas as frequências de tokens dadas pelo CountVectorizer()
        return (self.tokenized_essay.toarray().sum())	
        
    def get_mean_char_p_word(self):
        if self.nb_of_tokens == 0:
            print('Você deve ter o numero de tokens primeiro')
        else:
            nb_of_char = 0
            for position,item in enumerate(self.vector.get_feature_names()):
                nb_of_char += len(item)* self.tokenized_essay.toarray()[0][position]			# multiplica o tamanho da string(token) pela sua frequência
            self.mean_char_p_word = nb_of_char/self.nb_of_tokens
        return self.mean_char_p_word
        
        
    def get_nb_of_diff_words(self):
        self.nb_of_diff_words = len(self.vector.get_feature_names())							# lista de palavras dieferentes fornecidas pelo CountVectorizer
        return (self.nb_of_diff_words)
        
    def get_nb_of_optimal_sentences(self):
        counter = 0
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')						# Sentence Tokenizer do NLKT
        essay_sentence_list = sent_detector.tokenize(self.essay)			
		  # essay_sentence_list é uma Lista de tokens(frases)
        for i in essay_sentence_list:
            n_words_sentence = len(i.split())
            if n_words_sentence >= 15 and n_words_sentence <= 20:
                counter +=1
        self.nb_of_optimal_sentences = counter
        return self.nb_of_optimal_sentences
        
    def get_nb_of_speliing_errors(self):
        spell_errors = 0
        new_vec = CountVectorizer()
        to_tokenize = eC.expandContractions(self.essay.lower())
        to_tokenize = re.sub(' +', ' ',to_tokenize)
        to_tokenize = re.sub('@\S+','',to_tokenize)
        
        new_vec.fit_transform([to_tokenize])
        
        list_tokens = new_vec.get_feature_names()
        
        for i in list_tokens:
            __result = None
            __result = re.search('@\S+', i) 										      # retira nomes padrão do ASAP como @Location
            if __result is None:
                w = Word(i)														           	# da biblioteca textblob
                result_tuple = w.spellcheck()									         	# returna uma tupla com a sugestão de correção e o nível de certeza em %
                if i != result_tuple[0][0] and result_tuple[0][1] == 1.0:			# só faz correções que o corretor tem certeza, evita sugestão de singular em formas plurais
                    spell_errors += 1
        self.nb_of_spell_errors = spell_errors
        return self.nb_of_spell_errors
    
    def get_flesch_score(self):
        self.flesch_score = textstat.flesch_reading_ease(self.essay)
        return self.flesch_score
        
    def get_cos_dist(self):
        # Retorna a distância cosseno de dois textos usando Scikit
        __vectorizer = CountVectorizer()                                    		  
        red_promp = [self.essay,Prompts.get_prompt(self.prompt_number)]      		      # O CountVectorizer() cria duas arrays de frequências de palavras do
        y = __vectorizer.fit_transform(red_promp)                          		      # vocabulário do essay e do prompt
        x = y.toarray()
        transformer = TfidfTransformer(smooth_idf=False)
        tfidf = transformer.fit_transform(x)										             # Faz as operações do TF.IDF
        z = tfidf.toarray()
        self.cosine_distance = scipy.spatial.distance.cosine(z[0], z[1])
        return self.cosine_distance
    
# =============================================================================
#     def get_nb_of_grammar_errors(self):
#         url = 'https://languagetool.org/api/v2/check'
#         r = requests.post(url, data = {'text':self.essay,
#                                        'language': 'en',
#                                        'disabledRules':'EN_QUOTES,WHITESPACE_RULE,COMMA_PARENTHESIS_WHITESPACE,SENTENCE_WHITESPACE' } )
#         print('Status code:',r.status_code)
#         response_dict = r.json()
#         self.nb_of_grammar_errors = (len(response_dict['matches']))
#         return self.nb_of_grammar_errors
# =============================================================================
    
        
    def get_nb_of_grammar_errors_LT(self):
        self.nb_of_grammar_errors = self.errors.getOthersErrors()
        return self.nb_of_grammar_errors
        
    def get_nb_of_discourse_markers(self):
        counter=0
        
        for discourse_marker in discourseMarkers.multi_word_exp():
            result = None
            essay = self.essay
            result = discourse_marker.findall(essay.lower())
            re.sub(discourse_marker,'',essay)
            counter += len(result)
        
        for discourse_marker in discourseMarkers.discourseMarkers():
            matches = None
            searchable_pattern = "\W" + discourse_marker + '\W'
            matches = re.findall(searchable_pattern,essay.lower())
            if matches != None:
                counter += len(matches)
        self.nb_of_discourse_markers = counter
        return self.nb_of_discourse_markers
    
    
    def get_grammar_errors_p_token_n(self):
        self.grammar_errors_p_token = self.nb_of_grammar_errors/self.nb_of_tokens
        return self.grammar_errors_p_token
    
    def get_n_spell_errors_p_token_n(self):
        self.spell_errors_p_token = self.nb_of_spell_errors/self.nb_of_tokens
        return self.spell_errors_p_token
    
    def get_n_discourse_markers_p_sentence(self):
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')					
        n_of_sentences = len(sent_detector.tokenize(self.essay))
        self.discourse_markers_p_sentence = self.nb_of_discourse_markers/n_of_sentences
        return self.discourse_markers_p_sentence
    
    def get_style_errors_LT(self):
        return self.errors.getStyleErrors()
    
# =============================================================================
#     def get_style_errors(self):
#          url = 'https://languagetool.org/api/v2/check'
#          r = requests.post(url, data = {'text':self.essay,
#                                    'language': 'en',
#                                    'enabledCategories':'STYLE',
#                                    'disabledRules':'EN_QUOTES,WHITESPACE_RULE,COMMA_PARENTHESIS_WHITESPACE,SENTENCE_WHITESPACE',
#                                    })
#          print('Status code:',r.status_code)
#          response_dict = r.json()
#          self.style_errors = len(response_dict['matches'])
#          return self.style_errors
# =============================================================================

        