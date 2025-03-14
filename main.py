import math

def to_rpn(expression_list):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "%": 2, "^": 3}
    functions = {"sqrt", "root", "sin", "cos", "tan", "asin", "acos", "atan"}
    
    output = []
    operators = []

    for i, token in enumerate(expression_list):
        token = token.lower()
        if token.isdigit() or "." in token:
            output.append(token)
        elif token in functions:
            operators.append(token)   
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()

            if operators and operators[-1] in functions:
                output.append(operators.pop())
        elif token in precedence:
            while (operators and operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
        else:
            if output and output[-1].isdigit():
                output.append("*")
            operators.append(token)

    while operators:
        output.append(operators.pop())

    return output

def calculate_rpn(rpn_list):
    stack = []

    for token in rpn_list:
        if token.replace(".", "").isdigit():
            stack.append(float(token))
        elif token in {"+", "-", "*", "/", "%", "^"}:
            b = stack.pop()
            a = stack.pop()

            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                stack.append(a / b)
            elif token == "%":
                stack.append(a % b)
            elif token == "^":
                stack.append(a ** b)
        elif token == "root":
            b = stack.pop()
            a = stack.pop()
            stack.append(a ** (1 / b))
        elif token in {"sqrt", "sin", "cos", "tan", "asin", "acos", "atan"}:
            a = stack.pop()

            if token == "sqrt":
                stack.append(math.sqrt(a))
            elif token == "sin":
                stack.append(math.sin(math.radians(a)))
            elif token == "cos":
                stack.append(math.cos(math.radians(a)))
            elif token == "tan":
                stack.append(math.tan(math.radians(a)))
            elif token == "asin":
                stack.append(math.asin(math.radians(a)))
            elif token == "acos":
                stack.append(math.acos(math.radians(a)))
            elif token == "atan":
                stack.append(math.atan(math.radians(a)))

    return stack[0] if stack else None

expressionInput = input("Enter Expression: ")
expressionList = []
current_chunk = ""

for i, char in enumerate(expressionInput):
    if char.isalnum() or char == ".":
        current_chunk += char
    else:
        if current_chunk:
            expressionList.append(current_chunk.lower())
            current_chunk = ""
        if char.strip():
            if char == "(" and expressionList and (
                expressionList[-1].isdigit() or expressionList[-1] == ")"
            ):
                expressionList.append("*")
            expressionList.append(char.lower())

if current_chunk:
    expressionList.append(current_chunk.lower())

rpn_result = to_rpn(expressionList)
if float(calculate_rpn(rpn_result)) == int(calculate_rpn(rpn_result)):
    print("Result:", int(calculate_rpn(rpn_result)))
else:
    print("Result:", calculate_rpn(rpn_result))
