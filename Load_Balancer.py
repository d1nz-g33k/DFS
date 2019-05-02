"""
Load_Balancer.py manages the loads on different server_nodes connected

It connects different users to different servers based on load on each server_node.
If the load on server_node_1 is high you'll be connected to other nodes.
"""

import os
import sqlite3 as sql
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Markup, jsonify
#import flask.ext.wtf
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import socket
# import thread

if __name__ == "__main__":
	app.run()

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__)

"""
Nodes.db-> Contains the details of the nodes.
		-> Active nodes, UserID, Location of users, etc.
"""

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'Nodes.db'),
	SECRET_KEY='development key',
	USERNAME='admin',	# The username and password can be used to make the system a server 
	PASSWORD='default'	# Many Users can access the server systems, But only admin can add a Server 
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
	"""Connects to the Database."""
	db = sql.connect(app.config['DATABASE'])
	db.execute('CREATE TABLE IF NOT EXISTS Nodes(SID VARCHAR PRIMARY KEY NOT NULL, URL VARCHAR NOT NULL, LOC VARCHAR NOT NULL)')	
	# Table maintaining the Nodes list
	
	db.execute('CREATE TABLE IF NOT EXISTS Users(UID VARCHAR PRIMARY KEY NOT NULL, LOC VARCHAR NOT NULL, FOREIGN KEY(LOC) REFERENCES Nodes(LOC))')	
	# Table maintaining the Users list

	return db


def close_db(db):
	db.commit()
	db.close()


@app.route('/login', methods=['GET', 'POST'])
def home():
	db=connect_db()
	c=db.cursor()
	c.execute('SELECT Count() FROM Users')
	R = c.fetchone()[0]

	if request.method == 'POST':
		# g_usr=request.form.get('ID', None)
		# if request.form.get('ID', None) != (app.config['USERNAME']):
		# 	c.execute('SELECT Count() FROM Users')
		# 	N=c.fetchone()
		# 	c.execute('SELECT UID FROM Users')
		# 	r=c.fetchall()
		# 	for i in range(0,N[0]):
		# 		m=str(r[i])
		# 		q=request.form.get('ID', None)
		# 		p="('"+q+"',)"
		# 		if p == m:
		# 			M=[m]
		# 			# Check if username exists in the list
		# 			# If exists Check for the location and redirect to respective server_node
		# 			# Else Redirect to add user page
		# 			c.execute('SELECT LOC FROM Users WHERE UID=?', (q,))
		# 			loc=c.fetchone()[0]
		# 			c.execute('SELECT URL FROM Nodes WHERE LOC=?', (loc,))
		# 			url=c.fetchone()[0]
		# 			# connect_server()
		# 			url = url+'/login/'+q	# Add the details of the user to connect to the server_node
					# So that the server_node knows the UID already and the user needn't enter the ID again.
					# Make changes here later.
		q=request.form.get('ID', None)
		url = 'http://127.0.0.1:2000'
		url = url+'/login/'+q
		return redirect(url)

		# elif(request.form.get('ID', None) == (app.config['USERNAME'])):
		# 	return redirect(url_for('admin_login'))
		
	# else:
	# 	return redirect(url_for('home'))
	
	close_db(db)
	return render_template('Login.html')



@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session['Admin'] = False
	return home()


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
	if request.method == 'POST':
		print(request.form.get('pswd', None))
		if(request.form.get('pswd', None) == (app.config['PASSWORD'])):
			print("---Login_Admin---")
			session['Admin'] = True
			return redirect(url_for('admin'))
	return render_template('admin_login.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if(session['Admin'] != True):
		return redirect(url_for('home'))
	return render_template('lb_admin_dashboard.html')


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
	db=connect_db()
	c=db.cursor()

	r=1
	
	if request.method == 'POST':
		fn=request.form.get('firstname')
		ln=request.form.get('lastname')
		g=request.form.get('gender')
		un = request.form.get('UID')
		loc = request.form.get('LOC')

		# c.execute("INSERT into Users VALUES( ?, ?)", (un, loc,))
		# c.execute("SELECT URL FROM Nodes WHERE LOC=?", (loc,))
		# url=c.fetchone()[0]
		url = 'http://127.0.0.1:2000'
		url = url+'/'+fn+'/'+ln+'/'+g+'/'+un+'/'+loc 	# Make changes later

		return redirect(url)

	close_db(db)
	return render_template('Add_User.html')

@app.route('/add_server_node', methods=['GET', 'POST'])
def add_server_node():
	# To make a server *Accessible by admin only
	if session['Admin'] == True:
		
		db = connect_db()
		c = db.cursor()

		if request.method == 'POST':
			sid=request.form.get('sid')
			url=request.form.get('url')
			loc=request.form.get('loc')

			c.execute("INSERT into Nodes VALUES( ?, ?, ?)", (sid, url, loc,))
		close_db(db)
		return render_template('add_server_node.html')


# def initiate_server():
# 	# To start the server
# 	# Everytime a server starts the number of servers running is to be updated
# 	# Also the database must be updated to the latest version.  
# 	s = socket.socket()         # Create a socket object
# 	host = socket.gethostname() # Get local machine name
# 	port = 50000                # Reserve a port for your service.

# 	print 'Server started!'
# 	print 'Waiting for clients...'

# 	s.bind((host, port))        # Bind to the port
# 	s.listen(5)                 # Now wait for client connection.

# 	print 'Got connection from', addr
# 	while True:
# 	   c, addr = s.accept()     # Establish connection with client.
# 	   thread.start_new_thread(on_new_client,(c,addr))
# 	   #Note it's (addr,) not (addr) because second parameter is a tuple
# 	   #Edit: (c,addr)
# 	   #that's how you pass arguments to functions when creating new threads using thread module.
# 	s.close()


def connect_server():
	# To connect to the server *For User
	pass


# def on_new_client(clientsocket,addr):
# 	# Actions done everytime a new user connects
# 	while True:
# 		msg = clientsocket.recv(1024)
# 		#do some checks and if msg == someWeirdSignal: break:
# 		print addr, ' >> ', msg
# 		msg = raw_input('SERVER >> ')
# 		#Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
# 		clientsocket.send(msg)
# 	clientsocket.close()


def remove_server_node():
	# To remove the system from the server list
	pass
