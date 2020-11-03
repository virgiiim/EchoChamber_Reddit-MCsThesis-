import pandas as pd
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tag import StanfordNERTagger
import sys
import demjson

"""
cerca nella cartella i file con mese specificato come argomento; genera due file: uno col testo con stemming, uno con named entities + sentiment
argomento: mese in due cifre
"""

# tagger disponibile con 3,4 o 7 classi; per info -> https://nlp.stanford.edu/software/CRF-NER.shtml
st = StanfordNERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar',encoding='utf-8')

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
p_stemmer = nltk.stem.porter.PorterStemmer()
sid = SentimentIntensityAnalyzer()

df = pd.read_csv("utenti_features.csv")
selected_users = list(df["name"])


class Entities_list(object):
    # lista delle entità in una frase, comprensiva di sentiment
    
    def __init__(self, entities, sentiment):
        
        self.entities = entities
        self.sentiment = sentiment
        
    def get_info(self):
        
        return self.entities, self.sentiment


def analisi_linguistica(post_id, subr, testo):
    # sentiment analysis: per commento
    # NE extraction: classificazione eseguita sulle frasi tokenizzate
    # stemming: prima si fa la sostituzione delle NE (da "separate" a unite) in modo che risultino un unico token,
    #           poi si rimuovono le stopwords, infine si esegue lo stemming
    
    tokenTOT = []

    testo = testo.replace('\n', ' ').replace('\r', ' ').replace('\t', '')
    
    ss_tot = sid.polarity_scores(testo)
    sent_score = ss_tot['compound']

    sents = nltk.sent_tokenize(testo)
    tok_sents = [nltk.word_tokenize(sent) for sent in sents]
    
    classified_text = st.tag_sents(tok_sents)

    def unisci_NE(text):
        # per le NE composte da più di una parola

        text = [item for sentence in text for item in sentence]
        
        ne_list = []
        ne = []
        tag_prev = "O"
        for i  in range(len(text)):

            if text[i][1] != 'O':
                if tag_prev == "O" or tag_prev == text[i][1]:
                    ne.append(text[i][0])
                else:
                    ne_list.append(ne)
                    ne = [text[i][0]]
            
            if text[i][1] == 'O' or i == len(text)-1:
                if ne:
                    ne_list.append(ne)
                ne = []
            
            tag_prev = text[i][1]

        return ne_list

    NE = unisci_NE(classified_text)

    if NE:
        old_nes = [" ".join(ne) for ne in NE]
        new_nes = ["_".join(ne) for ne in NE]
        NE_list = [new_nes, sent_score]

        # se ci sono named entities, le sostituisce nel testo con la versione concatenata con _
        for i in range(len(new_nes)):
            testo = testo.replace(old_nes[i], new_nes[i])
            
    else:
        NE_list = []

    tokens = nltk.word_tokenize(testo)
    tokenTOT.append(tokens)

    all_tokens = [item for sublist in tokenTOT for item in sublist]
    stop_words = nltk.corpus.stopwords.words('english')
    stemmed_text = [p_stemmer.stem(tok) for tok in all_tokens if tok not in stop_words]
    
    return (post_id, subr), stemmed_text, NE_list


def run_analisi(filename):  
    
    print("workin' on {}".format(filename))
    
    data = demjson.decode_file(filename) 
        
    for comm in data:
        if comm['author'] in selected_users:

            text = comm['body']
            subreddit = comm['subreddit']
            post_id = comm['id']
            results = analisi_linguistica(post_id, subreddit, text)
    
            has_entities = results[2] != []

            id_stemmTxt = str(results[0]) + "," + str(results[1]) + "\n"
            id_entities = str(results[0]) + "," + str(results[2]) + "\n"
    
            if has_entities:
            
                print(id_entities, file=open('results_tp/entities_sentiment_' + sys.argv[1] , 'a'))
        
            print(id_stemmTxt, file=open('results_tp/stemmed_text_' + sys.argv[1], 'a'))

    print("done!")
 

path = "filtered_subrs/"  

for filename in os.listdir(path):
    if filename.endswith(sys.argv[1]):
        run_analisi(filename)
