# Flask data migration example

The following will run the migrations (with seed data).

    pip install -r requirements.txt
    python app.py db upgrade


Model before migration

    class Test(db.Model):

        id = db.Column(db.Integer, primary_key=True)
        base64data = db.Column(db.String(128))


Model after migration

    class Test(db.Model):

        id = db.Column(db.Integer, primary_key=True)
        hexdata = db.Column(db.String(128))


Migrations:

 * 3eb7fb4efbda_.py Initialize db with seed data.
 * 2b97062d034f_.py Migrate base64data to hexdata
