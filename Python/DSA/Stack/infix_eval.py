from Stack import ArrayStack


def infix_eval(expression):

    opr_prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 2, "(": 0}

    def _eval_operator(left_operand, right_operand, operator):
        if operator == "+":
            return left_operand + right_operand
        elif operator == "-":
            return left_operand - right_operand
        elif operator == "*":
            return left_operand * right_operand
        elif operator == "/":
            return left_operand / right_operand
        elif operator == "^":
            return left_operand**right_operand

    stack_operators = ArrayStack(len(expression))
    stack_operand = ArrayStack(len(expression))
    for char in expression:
        if char.isnumeric():
            stack_operand.push(int(char))
        elif char == "(":
            stack_operators.push(char)
        elif char == ")":
            while stack_operators.top() != "(":
                operator = stack_operators.pop()
                right_operand = stack_operand.pop()
                left_operand = stack_operand.pop()
                stack_operand.push(
                    _eval_operator(left_operand, right_operand, operator)
                )
            stack_operators.pop()
        elif char in opr_prec:
            while (
                not stack_operators.isempty()
                and opr_prec[char] <= opr_prec[stack_operators.top()]
            ):
                operator = stack_operators.pop()
                right_operand = stack_operand.pop()
                left_operand = stack_operand.pop()
                stack_operand.push(
                    _eval_operator(left_operand, right_operand, operator)
                )
            stack_operators.push(char)
        print(
            f"Iteration Status: Current Char is {char}\nstack_operand:{stack_operand}\nstack_operators:{stack_operators}",
            end=f"\n{'-'*50}\n",
        )
    while not stack_operators.isempty():
        operator = stack_operators.pop()
        right_operand = stack_operand.pop()
        left_operand = stack_operand.pop()
        stack_operand.push(_eval_operator(left_operand, right_operand, operator))

    return stack_operand.top()


if __name__ == "__main__":
    expression = "(3-5)*(2-8)"
    print(infix_eval(expression))
