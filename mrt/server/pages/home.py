"""
The welcome page
"""

from flask import render_template

from mrt.server.mrt_app import mrt_app


@mrt_app.route('/hello', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
