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

    return output


def generate_tac(postfix):
    """Generates three-address code (TAC) for the given postfix expression."""
    stack = []
    temp_var_count = 1
    tac = []
    temp_map = {}

    for token in postfix:
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


def main():
    """Main function to take input, generate postfix and TAC, and print results."""
    expression = input("Enter an expression: ")
    postfix = infix_to_postfix(expression)
    tac = generate_tac(postfix)

    print("Postfix expression:", " ".join(postfix))
    print("Three-address code (TAC):")
    for instruction in tac:
        print(instruction)


if __name__ == "__main__":
    main()
