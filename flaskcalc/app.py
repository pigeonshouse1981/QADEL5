from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operator = request.form['operator']

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "Error: Division by zero.", 400
            result = num1 / num2
        else:
            return "Invalid operator", 400

        return render_template('result.html', num1=num1, num2=num2, operator=operator, total=result)

    except ValueError:
        return "Invalid input. Please enter valid numbers.", 400
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
