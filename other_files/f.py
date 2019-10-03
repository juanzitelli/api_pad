from flask import Flask
from flask import render_template, request, make_response


app = Flask(__name__)

# primer hello
@app.route("/hello1")
def hello1():
    return "Hello World!"


# primer index
@app.route("/")
def index():
   return render_template("index.html")

# student
@app.route('/student/')
def student():
   return render_template('student.html')

# resultado2 es llamado dede la página anterior: student.html
@app.route('/result2',methods = ['POST', 'GET'])
def result2():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    p = post_id + 100
    return 'Post %d' % p

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)


@app.route('/index3')
def inde3():
   return render_template('index2.html')


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']

    resp = make_response(render_template('readcookie.html'))
    resp.set_cookie('userID', user)

    return resp