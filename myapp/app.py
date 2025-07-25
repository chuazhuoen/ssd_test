from flask import Flask, render_template, request, redirect, session
import html

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def is_malicious(user_input):
    """Detect simple XSS/SQL patterns"""
    lowered = user_input.lower()

    # XSS patterns
    xss_signatures = [
        "<script", "</script", "onerror=", "onload=", "alert(", "javascript:", "<img", "<iframe", "<svg"
    ]
    
    # SQL injection patterns
    sql_signatures = [
        "--", ";--", "/*", "*/", "@@", "@", "char(", "nchar(", "varchar(", "nvarchar(",
        "alter ", "begin ", "cast(", "create ", "cursor ", "declare ", "delete ", "drop ",
        "end ", "exec ", "execute ", "fetch ", "insert ", "kill ", "open ", "select ", 
        "sysobjects", "syscolumns", "table ", "update "
    ]

    for sig in xss_signatures + sql_signatures:
        if sig in lowered:
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    user_input = ""

    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        
        if is_malicious(user_input):
            error = "Malicious input detected. Input cleared."
            user_input = ""  # clear the input
        else:
            session['user_input'] = html.escape(user_input)
            return redirect('/new')

    return render_template('home.html', error=error, user_input=user_input)

@app.route('/new')
def new_page():
    user_input = session.get('user_input', '')
    return render_template('new_page.html', user_input=user_input)
