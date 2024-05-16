from flask import Flask, render_template

app = Flask("Olá")

@app.route('/')
def ola():
    return render_template('ola.html')