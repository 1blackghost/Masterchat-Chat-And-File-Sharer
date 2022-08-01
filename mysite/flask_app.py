from datetime import timedelta
from datetime import datetime
from flask import *
import os
app=Flask(__name__)
app.secret_key='123'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
@app.route('/view')
def view():
	if 'user' in session:
		with open('files.txt','r') as f:
			d=eval(f.read())
		return render_template('upload.html',d=d)
	else:
		redirect(url_for('home'))

@app.route('/upload_file')
def upload():
    return render_template("file_upload_form.html")

@app.route('/success', methods = ['POST'])
def success():
	if 'user' in session:
		if request.method == 'POST':
			f = request.files['file']
			to="mysite/static/"+str(f.filename)
			f.save(to)
			name=f.filename
			with open('files.txt','r') as f:
				d=eval(f.read())
				user=session['user']
				d[name]=user
			with open('files.txt','w') as f:
				f.write(str(d))
			now=datetime.now()
			timenow=now.strftime("%H:%M %p")
			d2 = now.strftime("%B %d, %Y")
			with open('templates/messages.txt','a') as f:
			    f.write('NEW!>'+str(user)+':File Got Uploaded!'+str(name)+'----------'+str(timenow)+'--'+str(d2)+'\n')

			return redirect(url_for('home'))
@app.route('/old',methods=['GET','POST'])
def old():
	with open('old.txt','r') as f:
		red=f.read()
	return render_template('old.html',x=red)
@app.route('/update_decimal',methods=['POST'])
def update_decimal():
    file = open('templates/messages.txt', encoding="utf8")
    mess=file.readlines()
    mess.reverse()
    string=''
    for i in mess:
        string=string+i
    return jsonify('',render_template('random_decimal.html',d=string))
@app.route('/logoutfirst',methods=['GET','POST'])
def logoutfirst():
	return '''<h1>LOGIN PAGE</h1>
<p style="color:red">You Are Already Logged In Try Logging Out First!</p>
<form action='/' method="post">
	<p><input type='submit' value='Retry??' name='nm'/></p>
</form>'''
@app.route('/help',methods=['GET','POST'])
def help():
	return render_template('help.html')
@app.route('/about',methods=['GET','POST'])
def about():
	return render_template('about.html')
@app.route('/chatting',methods=['GET','POST'])
def chatting():
	if 'user' in session:
		if 'user' in session:
			user=session['user']
			with open('user.txt','r') as f:
				users=f.read()
			if user not in users:
				with open('user.txt','a') as f:
					f.write(str(user)+'\n')
			with open('user.txt','r') as f:
				users=f.read()
		try:
			username=session['user']
			if request.method=='POST':
				if not request.form['nm']=='':
					msg=request.form['nm']
					now=datetime.now()

					d2 = now.strftime("%B %d, %Y")
					timenow=now.strftime("%H:%M %p")
					with open('templates/messages.txt','a') as f:
					    f.write(str(username)+':'+str(msg)+'----------'+str(timenow)+'--'+str(d2)+str('\n'))
				else:
					redirect(url_for('/old'))
		except Exception as e:
			print(str(e))
		file = open('templates/messages.txt', encoding="utf8")
		mess=file.readlines()
		mess.reverse()
		string=''
		for i in mess:
		    string=string+i
		return render_template('mainthing.html',d=string,users=users)

	else:
		return redirect(url_for('login'))
@app.route('/startchat',methods=['GET','POST'])
def startchat():
	if 'user' in session:

		if 'user' in session:
			return redirect(url_for('chatting'))
		else:
			return render_template('start.html')
	else:
		return redirect(url_for('login'))
@app.route('/logout',methods=['GET','POST'])
def logout():
	str=''
	if 'user' in session:
		user=session['user']
		session.pop('user',None)
		with open('user.txt','r') as f:
			d=f.readlines()
		if user+'\n' in d:
			d.pop()
		with open('user.txt','w') as f:
			f.writelines(d)

	return redirect(url_for('login'))

@app.route('/loginerror',methods=['GET','POST'])
def loginerror():
	if request.method=='POST':
		if request.form['nm']=='':
			return redirect(url_for('loginerror'))
		else:
			session['user']=request.form['nm']
			name=request.form['nm']
			return redirect(url_for('home'))
	else:
		return render_template('chat1.html')
@app.route('/home')
def home():
	if 'user' in session:
		user=session['user']
		with open('user.txt','r') as f:
			users=f.read()
		if user not in users:
			with open('user.txt','a') as f:
				f.write(str(user)+'\n')
		with open('user.txt','r') as f:
			users=f.read()

		return render_template('home.html',user=user,users=users)
	else:
		return redirect(url_for(login))
@app.route('/',methods=['GET','POST'])
def login():
	if request.method=='POST':
		with open('user.txt','r') as f:
			d=f.readlines()
			print(d)
		if request.form['nm']=='':
			return redirect(url_for('loginerror'))
		elif request.form['nm']=='Retry??':
			return redirect(url_for('login'))
		elif str(request.form['nm'])+str('\n') in d:
			return redirect(url_for('logoutfirst'))
		else:
			session['user']=request.form['nm']
			name=request.form['nm']
			return redirect(url_for('home'))
	else:
		return render_template('chat.html')
if __name__=='__main__':
    app.run(debug=True)
