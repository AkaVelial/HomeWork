from flask import Flask

app = Flask(__name__)

@app.route('/calc/<int:num1>/<int:num2>/<op>')
def calculator(num1, num2, op):
    if op == '+':
        return str(num1 + num2)
    elif op == '-':
        return str(num1 - num2)
    elif op == '*':
        return str(num1 * num2)
    elif op == '/':
        return str(num1 / num2)
    else:
        return "Invalid operator"

if __name__ == '__main__':
    app.run(debug=True)
