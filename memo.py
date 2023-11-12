from flask import Flask, render_template, request, redirect

# インスタンス変数にuseridを設定する方法（非推奨）

app = Flask(__name__)

class MyApp:
    def __init__(self):
        self.userid = None

myapp_instance = MyApp()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global myapp_instance
    if request.method == 'POST':
        userid = request.form.get('userid')
        # other signup logic...

        # Set the userid in the MyApp instance
        myapp_instance.userid = userid
        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global myapp_instance
    if request.method == 'POST':
        userid = request.form.get('userid')
        # other login logic...

        # Set the userid in the MyApp instance
        myapp_instance.userid = userid
        return redirect('/')

    return render_template('login.html')

@app.route('/')
def home():
    global myapp_instance
    # Access the userid from the MyApp instance
    userid = myapp_instance.userid
    return render_template('home.html', userid=userid)

if __name__ == '__main__':
    app.run(debug=True)

