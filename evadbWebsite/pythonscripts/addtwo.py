import sys

def addTwo(num1, num2):
    return num1 + num2


if __name__ == "__main__":
    number1 = sys.argv[1]
    number2 = sys.argv[2]

    summation = addTwo(int(number1), int(number2))
    print(summation, end="")
    sys.stdout.flush()
