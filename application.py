from flask import Flask, redirect

app=Flask(__name__, static_folder='web', static_url_path='/')

@app.route('/')
def home():
    return redirect('/index.html')

