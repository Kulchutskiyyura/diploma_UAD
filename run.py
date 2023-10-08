from application import app


if __name__ == "__main__":
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.run(debug=True)
