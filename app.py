# app.py
from flask import Flask, render_template, request
import calculator

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    op = request.form.get("operation")
    try:
        if op == "sqrt":
            x = float(request.form.get("x", "0"))
            result = calculator.sqrt(x)
            expr = f"√{x}"
        elif op == "factorial":
            n = float(request.form.get("n", "0"))
            result = calculator.factorial(n)
            expr = f"{int(n)}!"
        elif op == "ln":
            x = float(request.form.get("x", "0"))
            result = calculator.ln(x)
            expr = f"ln({x})"
        elif op == "power":
            x = float(request.form.get("x", "0"))
            b = float(request.form.get("b", "1"))
            result = calculator.power(x, b)
            expr = f"{x}^{b}"
        else:
            return render_template("index.html", error="Unknown operation.")
        return render_template("index.html", result=result, expression=expr)
    except Exception as e:
        return render_template("index.html", error=str(e))
