from flask import Flask, render_template, request

def infix_to_postfix(expr):
    stack = []
    output = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '(': 0, ')': 0}  # Include parentheses with precedence 0

    for token in expr.split():
        if token in precedence:
            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Pop the '('
            else:
                while stack and precedence[stack[-1]] >= precedence[token]:
                    output.append(stack.pop())
                stack.append(token)
        else:
            output.append(token)  # Operand case

    while stack:
        if stack[-1] not in '()':
            output.append(stack.pop())
        else:
            raise ValueError("Mismatched parentheses in expression")  # Handle unmatched parentheses

    return " ".join(output)


def generate_tac(postfix):
    """Generates three-address code (TAC) for the given postfix expression."""
    stack = []
    temp_var_count = 1
    tac = []
    temp_map = {}

    for token in postfix.split():
        if token.isalnum():  # Operand
            stack.append(token)
        else:  # Operator
            operand2 = stack.pop()
            operand1 = stack.pop()

            # Check if the operation result already exists in temp_map
            operation = f"{operand1} {token} {operand2}"
            if operation in temp_map:
                temp_var = temp_map[operation]
            else:
                temp_var = f"t{temp_var_count}"
                tac.append(f"{temp_var} = {operand1} {token} {operand2}")
                temp_map[operation] = temp_var
                temp_var_count += 1

            stack.append(temp_var)

    return tac


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Assuming you have an index.html template with an input field

@app.route("/generate", methods=["POST"])
def generate_code():
    if request.method == "POST":
        user_input = request.form["expression"]  # Assuming the input field name is "expression" in the template
        postfix_expression = infix_to_postfix(user_input)
        tac = generate_tac(postfix_expression)
        return render_template("result.html", code=tac, postfix=postfix_expression)  # Pass both postfix and TAC
    return "Invalid request method"

if __name__ == "__main__":
    app.run(debug=True)
