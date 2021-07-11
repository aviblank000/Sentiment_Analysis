from flask import Flask, redirect, url_for, render_template, request
import nltk
import csv
import numpy as np

app = Flask(__name__)

negative = []
with open("static/words_negative.csv", "r") as file:
	reader = csv.reader(file)
	for row in reader:
		negative.append(row)

positive = []
with open("static/words_positive.csv", "r") as file:
	reader = csv.reader(file)
	for row in reader:
			positive.append(row)

nltk.download('punkt')
def sentiment(text):
    temp = [] #
    text_sent = nltk.sent_tokenize(text)
    for sentence in text_sent:
        n_count = 0
        p_count = 0
        sent_words = nltk.word_tokenize(sentence)
        for word in sent_words:
            for item in positive:
                if(word == item[0]):
                    p_count +=1
            for item in negative:
                if(word == item[0]):
                    n_count +=1

        if(p_count > 0 and n_count == 0): #any number of only positives (+) [case 1]
            #print "+ : " + sentence
            temp.append(1)
        elif(n_count%2 > 0): #odd number of negatives (-) [case2]
            #print "- : " + sentence
            temp.append(-1)
        elif(n_count%2 ==0 and n_count > 0): #even number of negatives (+) [case3]
            #print "+ : " + sentence
            temp.append(1)
        else:
            #print "? : " + sentence
            temp.append(0)
    return temp

@app.route("/", methods =["POST","GET"])
def home():
	if request.method=="POST":
		txt = request.form["text"]
		res = sentiment(txt)
		return render_template("index.html", res=res )

	return render_template("index.html")

if __name__=="__main__":
	app.run(debug=True)