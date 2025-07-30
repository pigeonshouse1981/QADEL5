from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/sum', methods=['POST'])
def sum_numbers():
    try:
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        total = num1 + num2
        return render_template('result.html', num1=num1, num2=num2, total=total)
    except ValueError:
        return "Invalid input. Please enter valid numbers.", 400

if __name__ == '__main__':
    app.run(debug=True)
