import glob
import streamlit as st
import os
import pandas as pd
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from collections import defaultdict
import nltk
nltk.download('punkt')

#wide layout in streamlit
st.set_page_config(layout="wide")

#title of page
st.title('Tekst analyse v1.1')

#show / hide raw texts and tables
option1 = st.checkbox('Laat tabel zien')
option2 = st.checkbox('Laat alle teksten zien')

####################################

#change main textfile here if needed
maintextfile = 'text.csv'

####################################

#initialise some vars
data = ''
keeper = defaultdict(dict)

#load main text file
data = pd.read_csv(maintextfile, sep=';', parse_dates=True)

#load all training CSV files
def load_classifiers():
	for filename in glob.glob('*.csv'):
		if filename != maintextfile:
			noext = os.path.splitext(filename)
			with open(filename, 'r') as fp:
				keeper[noext[0]]['Classifier'] = NaiveBayesClassifier(fp, format="csv")	
			keeper[noext[0]]['CSV'] = filename	 
			data[noext[0]+' pos'] = ""
			data[noext[0]+' neg'] = ""

#loop through all texts
def analyse_texts():
	for ind in data.index: 
		for key in keeper:
			blob = TextBlob(data['Tekst'].values[ind],classifier=keeper[key]["Classifier"])
			prob_dist = keeper[key]["Classifier"].prob_classify(str(data['Tekst'].values[ind]))
			data[key+' pos'].values[ind] = round(prob_dist.prob("pos"),2)
			data[key+' neg'].values[ind] = 0-round(prob_dist.prob("neg"),2)
			if option2: st.write('Classify tekst: ',data['Tekst'].values[ind],': ',blob.classify(),round(prob_dist.prob("pos"),2),round(prob_dist.prob("neg"),2),key)
	if option1: st.table(data)


#remove Tekst from table and use date as index for graph
def write_graph():
	cleartable = data[data.columns.difference(['Tekst'])].rename(columns={'Datum':'index'}).set_index('index')		
	st.area_chart(cleartable,height=500)			

#load all functions
load_classifiers()
analyse_texts()
write_graph()

#####################################################
#end of script
