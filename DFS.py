import os
import sqlite3 as sql
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, jsonify
#import flask.ext.wtf
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import socket
import thread

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
	PASSWORD='default'	# Many Users can access the server systems, But only admin can make a initiate a Server 
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
	"""Connects to the Database."""
	db = sql.connect(app.config['DATABASE'])
	db.execute('CREATE TABLE IF NOT EXISTS Users()')	
	# We need a table for maintaining the Users list
	
	db.execute('CREATE TABLE IF NOT EXISTS Files()')
	# A table to track the changes made to the Files **Time, Date, Users, file-type
	
	db.execute('CREATE TABLE IF NOT EXISTS Servers()')	
	# A table to maintain the details of the servers **Memory used in the servers
	return db


def close_db(db):
	db.commit()
	db.close()


@app.route('/login', methods=['GET', 'POST'])
def home():
	db=connect_db()
	c=db.cursor()
	c.execute('SELECT Count() FROM ')
	R = c.fetchone()[0]

	if request.method == 'POST':
		g_usr=request.form.get('ID', None)
		if request.form.get('ID', None) != (app.config['USERNAME']):
			c.execute('SELECT Count() FROM Users')
			N=c.fetchone()
			c.execute('SELECT TID FROM Users')
			r=c.fetchall()
			for i in range(0,N[0]):
				m=str(r[i])
				q=request.form.get('ID', None)
				p="('"+q+"',)"
				if p == m:
					M=[m]
					c.execute('SELECT pswd FROM Users WHERE uname=?', (q,))
					pswd=c.fetchone()[0]
					if(request.form.get('pswd', None) == pswd):
						session['User'] = True
						connect_server()
						return redirect(url_for('user'))
					else:
						E='Invalid password'

		elif request.form.get('pswd', None) != app.config['PASSWORD']:
			F='Invalid password'
			
		else:
			session['Admin'] = True
			return redirect(url_for('admin'))
			
	close_db(db)
	return render_template('Login.html')

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
		return render_template('admin_dashboard.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
	db=connect_db()
	c=db.cursor()

	r=1
	
	if request.method == 'POST':
		fn=request.form.get('firstname')
		ln=request.form.get('lastname')
		g=request.form.get('gender')
		un = request.form.get('uname')

		c.execute("INSERT into Users VALUES( ?, ?, ?, ?)", (ln, fn, g, un,))


	close_db(db)
	if(session['Admin'] != True):
		return render_template('login.html')
	else:
		return render_template('New_User.html', adno=r)

def upload_file():
	# To upload files to the server


def make_server():
	# To make a server *Accessible by admin only


def initiate_server():
	# To start the server
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # Get local machine name
	port = 50000                # Reserve a port for your service.

	print 'Server started!'
	print 'Waiting for clients...'

	s.bind((host, port))        # Bind to the port
	s.listen(5)                 # Now wait for client connection.

	print 'Got connection from', addr
	while True:
	   c, addr = s.accept()     # Establish connection with client.
	   thread.start_new_thread(on_new_client,(c,addr))
	   #Note it's (addr,) not (addr) because second parameter is a tuple
	   #Edit: (c,addr)
	   #that's how you pass arguments to functions when creating new threads using thread module.
	s.close()


def close_server():
	# End a server


def connect_server():
	# To connect to the server *For User


def on_new_client(clientsocket,addr):
	# Actions done everytime a new user connects
	while True:
		msg = clientsocket.recv(1024)
		#do some checks and if msg == someWeirdSignal: break:
		print addr, ' >> ', msg
		msg = raw_input('SERVER >> ')
		#Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
		clientsocket.send(msg)
	clientsocket.close()


def remove_server():
	# To remove the system from the server list