from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('data.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            sommeil INTEGER,
            etude INTEGER
        )
    ''')
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        age = request.form["age"]
        sommeil = request.form["sommeil"]
        etude = request.form["etude"]

        conn = sqlite3.connect('data.db')
        conn.execute("INSERT INTO students (age, sommeil, etude) VALUES (?, ?, ?)",
                     (age, sommeil, etude))
        conn.commit()
        conn.close()

        return redirect("/stats")

    return render_template("index.html")

@app.route("/stats")
def stats():
    conn = sqlite3.connect('data.db')

    data = conn.execute("SELECT sommeil, etude FROM students").fetchall()

    if len(data) == 0:
        return "Aucune donnée disponible"

    sommeil_vals = [d[0] for d in data]
    etude_vals = [d[1] for d in data]

    stats = {
        "moy_sommeil": round(sum(sommeil_vals)/len(sommeil_vals), 2),
        "moy_etude": round(sum(etude_vals)/len(etude_vals), 2),
        "min_sommeil": min(sommeil_vals),
        "max_sommeil": max(sommeil_vals),
        "min_etude": min(etude_vals),
        "max_etude": max(etude_vals),
    }

    conn.close()

    return render_template("stats.html",
                           stats=stats,
                           sommeil=sommeil_vals,
                           etude=etude_vals)

if __name__ == "__main__":
    init_db()
    app.run()
