# Psychiatric Text Analysis
Pythons script and web-app for text analysis of psychiatric medical texts. It's focus is the Dutch language, but it can be used for other languages and topics too. 

Python script en web-app voor tekst analyse van EPD rapportages in de GGZ / psychiatrie. Gericht op de Nederlandse taal, maar kan voor andere talen en andere onderwerpen gebruikt worden. 

See a working demo here:
https://share.streamlit.io/micheldejoode/psychiatrictextanalysis/main/tekstanalyse.py

# Installation
1. Make sure you have python installed. There are a lot of options here, I use WinPython, it's a portable version of python. The 'dot' version is only 24 mb. 
2. Download the zip file from github
3. Unpack somewhere where you can run the file with python
4. Open the python console and type:

'''shell
pip install -r requirements.txt
'''

6. Wait...
7. In the python console, type: streamlit run tekstanalyse.py
8. It should start a local webserver and show the app. 

# How it works
The script makes use of the python Textblob library, which is a natural language processing (NLP) API, and specific the classification part (Naive Bayes Analyzer). What this does is search for specific words in a text, to classify it. Textblob can be trained with training-sentences, to learn what words belong to a classification, and which words are the oposite of a classification. For example, the script can see the difference between 'she is depressed' and 'she is not depressed anymore'. 

Besides Textblob the script makes heavy use of Streamlit, a great package to quickly build an app around basic functionality. See the demo for an example. 

# Needed files
1. The script needs a text.csv file in the root folder, with in the first column the date of the text (american style, 2021-12-1), and in the second column the text itself. The script could easily be changed to use a JSON file or something else. 

2. The script looks for other .csv files in the root folder, which it automatically loads as training files. Every training file is used as one classification. The script uses the filename of the csv file as name for the classification. For example, for depression.csv, depression will be a classification. In this csv you need a word or sentence on every line, followed with a , then followed with the word pos or neg, to specify if that word or sentence is positive or negative for the classification. For example: she feels very depressed,pos will let the script know that those words are positive for the classification depression. 

By the way, Textblob will not use the exact sentences to search for, but look for the most important words. You have to play a little with it to see how it reacts on different texts.

After the script loads the text.csv and the training files, it will search for the classifications on every text. Then it will calculate how likely it is that the text can by classified positive or negative, and will give a number to it between -1 and +1. Those numbers are plotted in a graph. 

There are different ways to look more closely to this process by watching the table with numbers, watch the text sentence by sentence or watching the training files. This can all be done from the app. 

# What to do with it
Best use is to connect it to a Electronic Patients System / Elektronisch Patienten Dossier. Then:
First of all; you can search for classifications in unstructered texts. This is usefull to quicky see if symptoms or factors are increasing or decreasing. 
Second, you could use those data to further analyse correlations between symptoms and other factors, like some form of treatment and symptoms etc.
Third, you could use information about symptoms to search for the best treatment or diagnoses online, when connected to an online database. 

