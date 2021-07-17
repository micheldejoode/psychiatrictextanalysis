import glob
import streamlit as st
import os
import pandas as pd
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from collections import defaultdict

#wide layout in streamlit
st.set_page_config(layout="wide")

#title of page
st.title('Tekst analyse van psychiatrische rapportages')
st.write('Dit is een app voor analyse van EPD rapportages in de psychiatrie / GGZ.')
st.write('De app herkent symptoomcategorieen in de tekst, en geeft het voorkomen hiervan weer in de grafiek.')

st.write('v1.1.6')

#show table with scores
option1 = False
#show scores per sentence
option2 = False
#checkbox show trainingfiles
option6 = False 

#show checkbox Advanced
option5 = st.checkbox('Geavanceerd',False)

#if checkbox Advanced
if option5:
	option6 = st.checkbox('Laat trainingsteksten zien.')

#if checkbox show trainingfiles
if option6 == False:
	option4 = st.checkbox('Laat positieve waarden zien',value=True,help='Positief betekent dat het symptoom herkent wordt in de tekst')
	option3 = st.checkbox('Laat negatieve waarden zien',value=False,help='Negatief betekent dat het tegenovergestelde van het symptoom wordt herkent in de tekst')

####################################

#change main textfile here if needed
maintextfile = 'text.csv'

####################################

#initialise some vars
data = ''
keeper = defaultdict(dict)
check = ''

	
#load all training CSV files
def load_classifiers():
	#load all csv files and filenames
	for filename in glob.glob('*.csv'):
		#check if there are trainingfiles available
		if len(glob.glob('*.csv')) != 1:
			#exclude text.csv
			if filename != maintextfile:
				#remove extension from filename
				noext = os.path.splitext(filename)
				try:
					#open trainingfiles
					with open(filename, 'r') as fp:
						#if checkbox show trainingfiles: show trainingfiles
						if option6:
							st.write(noext[0])
							st.write(fp.readlines())
						#load trainingfile in Textblob classifier
						keeper[noext[0]]['Classifier'] = NaiveBayesClassifier(fp, format="csv")	
						
						
				except:
					#if error in loading trainingfile
					st.write('Er ging iets fout met het laden van een trainingsbestand:',filename)
				
				#don't show checkbox for classifiers if trainingtexts are showed
				if option6 == False:
					#save filename in keeper var for later use
					keeper[noext[0]]['CSV'] = filename
					#show checkbox for on/off classifier
					keeper[noext[0]]['show'] = st.checkbox(noext[0],value=True)
					#create column for classifier in data table
					data[noext[0]+' pos'] = ""
					data[noext[0]+' neg'] = ""				
		else:
			st.write('Geen trainingsbestanden aanwezig, plaats deze (*.csv) in de hoofdmap.')


#loop through all texts
def analyse_texts():
	#for every text
	for ind in data.index: 
		#for every classifier
		for key in keeper:
			#create blob from text with classifier
			blob = TextBlob(str(data['Tekst'].values[ind]),classifier=keeper[key]["Classifier"])
			#calculate probability for classifier
			prob_dist = keeper[key]["Classifier"].prob_classify(str(data['Tekst'].values[ind]))
			#add probability number for pos / neg to data table
			data[key+' pos'].values[ind] = round(prob_dist.prob("pos"),2)
			data[key+' neg'].values[ind] = 0-round(prob_dist.prob("neg"),2)
			
			#show the text in sentences with pos / neg per classification
			if option2:
				#for every sentence in blob text
				for sub in blob.sentences:
					#calculate probability per text
					nr = keeper[key]["Classifier"].prob_classify(str(sub))
					#show sentence, classifier and probability numbers
					st.write(sub,key,': ',sub.classify(),' (pos: ',round(nr.prob("pos"), 2), ' neg: ',round(nr.prob("neg"), 2),')')
	
	#show table with all data if checked in checkbox
	if option1: st.table(data)



def write_graph():
	#remove Tekst from table and use date as index for graph
	cleartable = data[data.columns.difference(['Tekst'])].rename(columns={'Datum':'index'}).set_index('index')		
	for key in keeper:
		#show only classifiers which are checked
		if keeper[key]['show'] == False:
			try:
				#drop unchecked columns
				cleartable.drop(key+' pos',axis='columns', inplace=True)
				cleartable.drop(key+' neg',axis='columns', inplace=True)
			except:
				print('niet gelukt indiv.')
		
		#if unchecked show negatives
		if option3 == False:
			try:
				#drop negative columns
				cleartable.drop(key+' neg',axis='columns', inplace=True)
			except:
				print('niet gelukt option 3')
		#if unchecked show positives
		if option4 == False:
			try:
				#drop positive columns
				cleartable.drop(key+' pos',axis='columns', inplace=True)
			except:
				print('niet gelukt option 4')
			
	#show chart based on cleartable	
	st.area_chart(cleartable,height=500)			
	

############################################################
#the program starts here

#try to load main text file; then load other functions
try:
	#load text.csv
	data = pd.read_csv(maintextfile, sep=';', parse_dates=True)
	#don't show all option if trainingfiles are shown
	if option6 == False and option5:
			option1 = st.checkbox('Laat tabel met positieve en negatieve scores zien.')
			option2 = st.checkbox('Laat per zin de positieve en negatieve score zien.')
except:
	st.write('Geen text.csv aanwezig, plaats deze in de hoofdmap.')
else:
	try:
		load_classifiers()
		
		#don't run other function if trainingfiles are shown
		if option6 == False:
			analyse_texts()
			write_graph()
	except Exception as e:
		st.write('Er is een probleem in één van de functies.',e)

		





#####################################################
#end of script