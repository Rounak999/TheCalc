from flask import Flask, render_template, request

app = Flask(__name__)

# Mathematical functions
def addition(a, b):
    return a + b

def mul(a, b):
    return a * b

def subs(a, b):
    return a - b

# Setting up the result variable
result = 0


@app.route("/", methods=["GET", "POST"])
def function_route():
    global result
    
    if request.method == "POST":
        if (request.form.get("operation")):
            # Get the operation and numbers from the form
            operation = request.form.get("operation")
            num1 = int(request.form.get("num1"))
            num2 = int(request.form.get("num2"))
            operation_string = f"{operation}({num1},{num2})"
        elif(request.form.get("operationfunction")):
            operation_string = request.form.get("operationfunction")


        # Restricting built-ins
        allowed_scope = {
            "addition": addition,
            "mul": mul,
            "subs": subs,
            "result": result,
            "__builtins__": None
        }
        
        # The exec code
        try:
            exec(f"result = {operation_string}", allowed_scope)
        except Exception as e:
            return f"Error: {e}"  # This will catch attempts to use disallowed functions

        # Update the global result with the modified value, if no error occurred
        result = allowed_scope.get("result", result)

        return render_template("result.html", result=result)
    
    # If GET request, show the form
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0",port=5000)
