from src import app, db

if __name__ == '__main__':
    db.drop_all(app=app)
    db.create_all(app=app)

    app.run(debug=True)
    