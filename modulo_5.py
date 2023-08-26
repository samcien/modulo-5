from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('dictionario.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS palabras (
            palabra text,
            significado text
            )""")
conn.commit()
conn.close()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_word', methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        palabra = request.form['palabra']
        significado = request.form['significado']
        conn = sqlite3.connect('dictionary.db')
        c = conn.cursor()
        c.execute("INSERT INTO palabras (palabra, significado) VALUES (?, ?)", (palabra, significado))
        conn.commit()
        conn.close()
        return 'Palabra agregada correctamente.'
    else:
        return render_template('add_word.html')


@app.route('/all_words')
def all_words():
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute("SELECT * FROM palabras")
    palabras = c.fetchall()
    conn.close()
    return render_template('all_words.html', palabras=palabras)


@app.route('/search_word', methods=['GET', 'POST'])
def search_word():
    if request.method == 'POST':
        word = request.form['search_word']
        conn = sqlite3.connect('dictionary.db')
        c = conn.cursor()
        c.execute("SELECT * FROM palabras WHERE palabra=?", (word,))
        palabras = c.fetchall()
        conn.close()
        return render_template('search_word.html', palabras=palabras)
    else:
        return render_template('search_word_form.html')


@app.route('/delete_word/<palabra>', methods=['POST'])
def delete_word(palabra):
    conn = sqlite3.connect('dictionary.db')
    c = conn.cursor()
    c.execute("DELETE FROM palabras WHERE palabra=?", (palabra,))
    conn.commit()
    conn.close()
    return redirect(url_for('all_words'))


if __name__ == '__main__':
    app.run(debug=True)
