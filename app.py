from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from table_def import *
from copy import copy
import datetime
import sqlite3
import glob
import time
import os
from os import getcwd 
import re
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

engine = create_engine('sqlite:///shree.db', echo=True)

app = Flask(__name__)

@app.route('/')
def home():
     r1 = 0;
     r2 = 0;
     file1 = open("unigram_line","r")
     line_no = file1.read()
     r = csv.reader(open('./unigrams.csv')) # Here your csv file
     lines = list(r)
     word = lines[int(line_no)+1][0]
     gloss = lines[int(line_no)+1][2]

     file2 = open("adj_line","r")
     line_no = file2.read()
     r = csv.reader(open('./Adjective.csv')) # Here your csv file
     lines = list(r)
     adj_word = lines[int(line_no)+1][0]
     adj_gloss = lines[int(line_no)+1][1]


     file3 = open("verb_line","r")
     line_no = file3.read()
     r = csv.reader(open('./verbs.csv')) # Here your csv file
     lines = list(r)
     verb_word = lines[int(line_no)+1][0]
     verb_gloss = lines[int(line_no)+1][1]
     if not session.get('logged_in'):
          return render_template('login.html')
     else:
          return render_template('index.html', word=word, gloss=gloss, adj_word = adj_word, adj_gloss = adj_gloss, verb_word = verb_word, verb_gloss = verb_gloss )

@app.route("/newword")
def signuppage():
    return render_template('addword.html')

@app.route("/addword", methods=['POST'])
def addwordf():
     word = str(request.form['word'])
     gloss = str(request.form['gloss'])
     sentence = str(request.form['sentence'])
     s = [word, gloss, sentence]
     myFile = open('ex.csv', 'a')
     with myFile:
     	writer = csv.writer(myFile)
     	writer.writerow(s)
     flash('Your new entry is added successfully!')
     return render_template('addword.html')

@app.route('/annotate', methods=['POST'])
def annotate():
	POST_response = str(request.form['response'])
	file1 = open("unigram_line","r")
	line_no = file1.read()
	r = csv.reader(open('./unigrams.csv')) # Here your csv file
	lines = list(r)
	lines[int(line_no)+1][3] = str(POST_response)
	writer = csv.writer(open('./unigrams.csv', 'w'))
	writer.writerows(lines)
	line_no = int(line_no) + 1
	file2 = open("unigram_line","w")
	file2.write(str(line_no))
	return redirect(url_for('home'))



@app.route('/adjective', methods=['POST'])
def adjective():
	POST_response1 = str(request.form['primary_adj_response'])
	POST_response2 = str(request.form['secondary_adj_response'])
	file1 = open("adj_line","r")
	line_no = file1.read()
	r = csv.reader(open('./Adjective.csv')) # Here your csv file
	lines = list(r)
	lines[int(line_no)+1][2] = str(POST_response1)
	lines[int(line_no)+1][3] = str(POST_response2)
	writer = csv.writer(open('./Adjective.csv', 'w'))
	writer.writerows(lines)
	line_no = int(line_no) + 1
	file2 = open("adj_line","w")
	file2.write(str(line_no))
	return redirect(url_for('home'))


@app.route('/verb', methods=['POST'])
def verb():
	POST_response1 = str(request.form['primary_verb_response'])
	POST_response2 = str(request.form['secondary_verb_response'])
	file1 = open("verb_line","r")
	line_no = file1.read()
	r = csv.reader(open('./verbs.csv')) # Here your csv file
	lines = list(r)
	lines[int(line_no)+1][2] = str(POST_response1)
	lines[int(line_no)+1][3] = str(POST_response2)
	writer = csv.writer(open('./verbs.csv', 'w'))
	writer.writerows(lines)
	line_no = int(line_no) + 1
	file2 = open("verb_line","w")
	file2.write(str(line_no))
	return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def do_admin_login():

     POST_USERNAME = str(request.form['username'])
     POST_PASSWORD = str(request.form['password'])
     Session = sessionmaker(bind=engine)
     s = Session()
     query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
     result = query.first()
     if result:
         session['logged_in'] = True
     else:
         flash('wrong password!')
     return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=5000)
