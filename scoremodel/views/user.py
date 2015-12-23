from flask import render_template, flash, redirect
from scoremodel import app
from scoremodel.forms.login import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def v_login():
    form = LoginForm()
    return render_template('login.html',
                           title='Aanmelden',
                           form=form)

