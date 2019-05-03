import os
import sqlite3 as sql
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, jsonify
#import flask.ext.wtf
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import socket
# import thread
import scandir as sc

if __name__ == "__main__":
	app.run()

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__)

"""
Data.db -> Contains the data of the files present in the server systems and the info of last edited.
		-> Also contains the details of the users to authorize
"""

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'Data.db'),
	SECRET_KEY='development key',
	USERNAME='admin',	# The username and password can be used to make the system a server 
	PASSWORD='default'	# Many Users can access the server systems, But only admin can add a Server 
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)



def connect_db():
	"""Connects to the Database."""
	db = sql.connect(app.config['DATABASE'])
	db.execute('CREATE TABLE IF NOT EXISTS Users(UID VARCHAR PRIMARY KEY NOT NULL, LOC VARCHAR NOT NULL, fn VARCHAR NOT NULL, ln VARCHAR NOT NULL, g VARCHAR NOT NULL)')	
	# We need a table for maintaining the Users list
	
	# db.execute('CREATE TABLE IF NOT EXISTS Files()')
	# A table to track the changes made to the Files **Time, Date, Users, file-type

	# db.execute('CREATE TABLE IF NOT EXISTS Servers()')
	# Maintain details of data servers
	
	return db

def close_db(db):
	db.commit()
	db.close()


@app.route('/login/<uid>', methods=['GET', 'POST'])
def home(uid):

	db=connect_db()
	c=db.cursor()

	if request.method == 'POST':
		c.execute('SELECT Count() FROM Users')
		N=c.fetchone()
		c.execute('SELECT UID FROM Users')
		r=c.fetchall()
		for i in range(0,N[0]):
			m=str(r[i])
			q=uid
			p="('"+q+"',)"
			if p == m:
				M=[m]
				c.execute('SELECT pswd FROM Users WHERE uid=?', (q,))
				pswd=c.fetchone()[0]
				if(request.form.get('pswd', None) == pswd):
					session['User'] = True
					return redirect(url_for('user', uid=uid))
				else:
					E='Invalid password'
	close_db(db)
	return render_template('Node_Login.html')

@app.route('/login')
def re_route():
	# Change later
	# Route to load_balancer
	return redirect('https://www.google.com')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session['User'] = False
	session['Admin'] = False
	return home()


@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if(session['Admin'] != True):
		return render_template('login.html')
	else:
		return render_template('node_admin_dashboard.html')


@app.route('/user/<uid>', methods=['GET', 'POST'])
def user(uid):
	# if(session[uid] != True):
	# 	return redirect(url_for('home'))
	# create a session for the respective uid at login
	return render_template('user.html', uid=uid)

@app.route('/display_files', methods=['GET', 'POST'])
def display_files():
	data = sc.scandir(path='C:\\Users\\Dinesh\\Documents\\GitHub\\DFS\\DFS\\File_Access')
	# for f in data:
	return render_template('index.html', data=data)

def upload_file():
	# To upload files to the server
	pass

def delete_file():
	# To delete files from the server
	pass

def restore_file():
	# To restore files to the server
	pass

def data_node():
	# To make a server *Accessible by admin only
	pass

