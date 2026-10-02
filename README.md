# HW2B Login Form

This is my login-form project for HW 2-B. It uses HTML, CSS, and JavaScript for a basic Juice Shop-style login page, with a Python Flask backend that checks submissions and verifies a demo account.

## Features

- Email and password fields.
- JavaScript checks for empty fields, an email containing `@`, and a password with at least 8 characters.
- The same checks on the server, even when a request skips JavaScript.
- Parameterized SQLite queries that keep submitted values separate from SQL instructions.
- Salted bcrypt password hashing and password verification.
- Plain-text status messages displayed with `textContent`.
- A 72-byte UTF-8 password limit to match bcrypt's input limit.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Flask routes, server validation, SQLite lookup, and bcrypt checks |
| `templates/index.html` | Login page, styling, and JavaScript |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Excludes the virtual environment, database, and generated files |
| `README.md` | Project explanation and setup instructions |

## How to run

Python 3.11 was used for this project. Download or clone this repository, then open a terminal in the repository's root folder.

### Windows

Run these commands one at a time:

```bat
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

### macOS or Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Keep the terminal running while using the page. Press Ctrl+C in the terminal to stop the server.

On first launch, the app creates `users.db` and adds a demo account. Its stored password is a salted bcrypt hash.

## Demo account

| Field | Value |
| --- | --- |
| Email | `student@example.com` |
| Password | `StudentPass123!` |

These are public demo credentials for this local assignment. A successful login shows a confirmation message; this demo does not create a persistent session or a protected dashboard.

## Tests performed

| Test | Observed result |
| --- | --- |
| Submit the correct demo credentials | `Login successful.` |
| Submit empty fields in the browser | JavaScript displays `Email and password are required.` |
| Send empty fields directly to the backend | HTTP 400 with `Email and password are required.` |
| Submit the SQL injection input below with an incorrect password | HTTP 401 with `Invalid email or password.` |

To check server-side validation from a second Windows terminal:

```bat
curl.exe -i --data-urlencode "email=" --data-urlencode "password=" http://127.0.0.1:5000/login
```

For the SQL injection attempt, I entered this email on my own local login page:

```text
student@example.com' OR 1=1 --
```

I entered `WrongPass123!` as the password and clicked **Log in**. The login was rejected. The email lookup uses a `?` placeholder instead of putting the email directly into the SQL string, and the password is checked using bcrypt.

The screenshots and the assignment's three write-ups are included in my separate PDF submission.

## Dependencies

- Flask
- bcrypt
- SQLite through Python's built-in `sqlite3` module

