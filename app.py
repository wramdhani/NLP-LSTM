import msvcrt
import os
from process import preparation, generate_response

#download nltk
preparation()
def get_bot_response():
    user_input = input("Kamu: ")
    result = generate_response(user_input)
    return result

if __name__ == "__main__":
    os.system('cls')
    while True:
        response = get_bot_response()
        print(f"Cece: {response}")

        if msvcrt.kbhit() and msvcrt.getch() == b'\x1b':
            print("Conversation ended")
            break
        