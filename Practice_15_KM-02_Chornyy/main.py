from factorial import factorial
from exp_root import exponentiation, root
from logarithm import logarithm

def ask_for_num(msg, msg1, P, integer=False):
    while True:
        try:
            inp = float(input(msg))
            if integer:
                inp = int(inp)
            if P(inp):
                raise ValueError
            break
        except ValueError:
            print(msg1)
    return inp

def main():
    print("Welcome to my calculator")
    print("Choose the function:")
    print("For factorial enter 1")
    print("For square of number enter 2")
    print("For cube of number enter 3")
    print("For square root enter 4")
    print("For cubic root enter 5")
    print("For logarithm enter 6")
    print("For 10-th logarithm enter 7")
    print("For natural logarithm enter 8")
    inp = ask_for_num("Your choise: ", "Incorrect input. Enter integer from 1 to 8", lambda x: (x < 1) or (x > 8), True)
    if inp == 1:
        print("You`re choosen factorial")
        print("Result: ", factorial.fact(ask_for_num("Your number: ", "Incorrect input. Enter natural number", lambda x: x < 0, True)))
    elif inp == 2:
        print("You`re choosen square of number")
        print("Result: ",exponentiation.exp2(ask_for_num("Your number: ", "Incorrect input. Enter number", lambda x: False, False)))
    elif inp == 3:
        print("You`re choosen cube of number")
        print("Result: ",exponentiation.exp3(ask_for_num("Your number: ", "Incorrect input. Enter number", lambda x: False, False)))
    elif inp == 4:
        print("You`re choosen square root")
        print("Result: ",root.root2(ask_for_num("Your number: ", "Incorrect input. Enter positive number", lambda x: x < 0, False)))
    elif inp == 5:
        print("You`re choosen cubic root")
        print("Result: ",root.root3(ask_for_num("Your number: ", "Incorrect input. Enter number", lambda x: False, False)))
    elif inp == 6:
        print("You`re choosen logarithm")
        a = ask_for_num("Your base: ", "Incorrect input. Enter base that != 1 and > 0", lambda x: (x == 1) or (x <= 0), False)
        b = ask_for_num("Your number: ", "Incorrect input. Enter positive number", lambda x: (x <= 0), False)
        print("Result: ",logarithm.log(a, b))
    elif inp == 7:
        print("You`re choosen 10-th logarithm")
        print("Result: ",logarithm.lg(ask_for_num("Your number: ", "Incorrect input. Enter positive number", lambda x: (x <= 0), False)))
    elif inp == 8:
        print("You`re choosen natural logarithm")
        print("Result: ",logarithm.ln(ask_for_num("Your number: ", "Incorrect input. Enter number", lambda x: (x <= 0), False)))

if __name__ == "__main__":
    main()