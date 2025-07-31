def show_options():
    print("1.show books")
    print("2.show authors")
    print("3.add book")
    print("4.add author")
    print("5.add author")


def get_prompt(prompt: str) -> int:
    while True:
        try:
            num = int(input(prompt))
            return num
        except ValueError:
            print("you entered an invalid input")


while True:
    show_options()
    print()

    get_prompt("enter number for operation:")
