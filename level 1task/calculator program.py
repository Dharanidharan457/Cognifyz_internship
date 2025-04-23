def calculator():
    print("Calculator Program")
    
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        op = input("Enter the operator (+, -, *, /, %): ")
        
        if op == '+':
            result = num1 + num2
            operation_name = "Addition"
        elif op == '-':
            result = num1 - num2
            operation_name = "Subtraction"
        elif op == '*':
            result = num1 * num2
            operation_name = "Multiplication"
        elif op == '/':
            if num2 == 0:
                print("Error: Division by zero is not allowed.")
                return
            result = num1 / num2
            operation_name = "Division"
        elif op == '%':
            if num2 == 0:
                print("Error: Modulo by zero is not allowed.")
                return
            result = num1 % num2
            operation_name = "Modulo"
        else:
            print("Invalid operator. Please use +, -, *, /, or %.")
            return
        
        print(f"\n{operation_name} Result:")
        print(f"{num1} {op} {num2} = {result}")
        
    except ValueError:
        print("Please enter valid numbers.")

if __name__ == "__main__":
    calculator()
    
#output
   #Calculator Program
   #Enter the first number: 9
   #Enter the second number: 8
   #Enter the operator (+, -, *, /, %): /
   #Division Result:
   #9.0 / 8.0 = 1.125