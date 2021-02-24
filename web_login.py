from flask import Flask, render_template, request, redirect, session, flash, url_for
import psycopg2
#from passlib.hash import md5_crypt
#from passlib.hash import bcrypt
#from passlib.hash.bcrypt import bcrypt
from base64 import b64encode, b64decode
import codecs
import sys
import crypt
import bcrypt

from flask_login import login_required, current_user, login_manager, LoginManager
from flask_login import logout_user

app = Flask(__name__)
app.secret_key = b'2%N@0^by##@!k)vx~'
#login_manager = LoginManager()

# This shows first page when browser loads. Need to index.html
@app.route('/')
def index():
	if 'username' in session:
		username = session['username']
	return render_template('sign_up.html')


# This should  be what happens when you click the registration button
#app.route('/registration', methods=['GET', 'POST'])
#def registration():
#	return render_template('/registration_success.html')



# This should should now give you login button to redirect you to index page
#@app.route('/registered_login', methods=['POST'])
#def registered_login()
#	return redirect(url_for('index'))



# This looks into a user logging in a web application. Need to change the def and form action to /login and login()
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

	if request.method == "POST":
		username = request.form['username']
		email = request.form['email']
		user_password = request.form['password']
		#db_email = ""

		conn2 = psycopg2.connect("dbname='dnecs' user='admin' password='Nes@2089' host='localhost' port='5432'")
        	# Open a cursor to perform database operations
		cur2 = conn2.cursor()
		#print(conn2.get_dsn_parameters(),"\n")
		cur2.execute("""SELECT email, username FROM userlogin WHERE password=crypt(%s, password);""", [user_password])

		#for email_char in str(cur2.fetchone()):
		#	db_email += email_char
		#print("DB MATCH =", db_email, email)
		db_email = str(cur2.fetchone())
		
		if not request.form['email'] or not request.form['password']:
			flash('Please enter all the fields', 'error')
			#return render_template('/sign_up.html')
		elif email in db_email and username in db_email:
			session['username'] = username
			conn2.commit()
			print("emails and passwords Match")
			conn2.close()
			# START A SESSION
			return render_template('/dnecs.html', username=username)
		else:
			print("No Match")
			flash('Wrong username/password', 'error')

		return render_template('/sign_up.html')
	else:
		print("Please enter email/passowrd")


# This looks into the dnecs.html page after logging. This is line maine page after log in
@app.route('/dnecs')
def dnecs():
	return render_template('dnecs.html')


# This looks into logout button after user has logged in. Logout button goes back to index login form.
@app.route('/logout')
def logout():
	# remove the username from the session if it is there
	session.pop('username', None)
	return redirect(url_for('index')) 


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
