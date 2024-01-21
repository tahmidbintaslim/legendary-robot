from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('status.html')  # HTML page showing status

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    # Logic to add or modify monitoring tokens/addresses
    pass

if __name__ == '__main__':
    app.run(debug=True)
