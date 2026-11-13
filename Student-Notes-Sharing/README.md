# Student Notes Sharing Website

A simple FSD-2 project built with HTML, CSS, JavaScript, Python Flask and SQLite.

## Features
- Upload PDF, DOC, DOCX, PPT, PPTX and TXT notes
- Save note details in SQLite database
- Search notes by title or subject
- Download uploaded files
- Delete notes

## Run in VS Code / Windows

1. Install Python and Git.
2. Open this folder in VS Code.
3. Open Terminal and run:

```bash
python -m pip install -r requirements.txt
python app.py
```

4. Open `http://127.0.0.1:5000` in your browser.

## GitHub commands

```bash
git init
git add .
git commit -m "Student Notes Sharing Website"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## External lab: download and run

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Student-Notes-Sharing
python -m pip install -r requirements.txt
python app.py
```

The database is created automatically the first time the application runs. Uploaded files are stored in the `uploads` folder.
