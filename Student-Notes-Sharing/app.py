from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "student-notes-secret"
UPLOAD_FOLDER = "uploads"
ALLOWED = {"pdf", "doc", "docx", "ppt", "pptx", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def connect():
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    return db

def create_table():
    db = connect()
    db.execute("""CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        subject TEXT NOT NULL,
        filename TEXT NOT NULL
    )""")
    db.commit()
    db.close()

@app.route("/")
def home():
    search = request.args.get("search", "")
    db = connect()
    notes = db.execute(
        "SELECT * FROM notes WHERE title LIKE ? OR subject LIKE ? ORDER BY id DESC",
        (f"%{search}%", f"%{search}%")
    ).fetchall()
    db.close()
    return render_template("index.html", notes=notes, search=search)

@app.route("/upload", methods=["POST"])
def upload():
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    file = request.files.get("file")

    if not title or not subject or not file or not file.filename:
        flash("Please complete all fields and choose a file.")
        return redirect(url_for("home"))

    filename = secure_filename(file.filename)
    if "." not in filename or filename.rsplit(".", 1)[1].lower() not in ALLOWED:
        flash("Allowed files: PDF, DOC, DOCX, PPT, PPTX and TXT.")
        return redirect(url_for("home"))

    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    db = connect()
    db.execute("INSERT INTO notes (title, subject, filename) VALUES (?, ?, ?)",
               (title, subject, filename))
    db.commit()
    db.close()
    flash("Notes uploaded successfully!")
    return redirect(url_for("home"))

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    db = connect()
    note = db.execute("SELECT filename FROM notes WHERE id=?", (note_id,)).fetchone()
    if note:
        path = os.path.join(app.config["UPLOAD_FOLDER"], note["filename"])
        if os.path.exists(path):
            os.remove(path)
        db.execute("DELETE FROM notes WHERE id=?", (note_id,))
        db.commit()
        flash("Note deleted.")
    db.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
