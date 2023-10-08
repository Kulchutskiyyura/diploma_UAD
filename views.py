from flask import Flask, request, render_template, redirect, url_for, redirect, flash
import json


from application import app
from application import services

@app.route('/', methods=['POST', 'GET'])
def show_diff():
    """
    """
    diff = []

    if request.method == 'POST':
        if 'file_origin' not in request.files:
            flash('No file part')
            print(request.files)
            return b'error'
        file_origin = request.files['file_origin']
        file_check = request.files['file_check']
        if file_origin.filename == '' or file_check.filename == '':
            flash('No selected file')
            return b'error_no_filename'

        diff = services.get_diff(file_origin, file_check)
        print(diff)
        print("after diff")

    print(json.dumps(diff))
    return render_template('show_diff.html', diff=json.dumps(diff))
