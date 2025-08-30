# Imports          #
from pythonosc import udp_client
from wonderwords import RandomWord
import requests
from bs4 import BeautifulSoup
from time import sleep
from colorama import Fore


# Client          #
client = udp_client.SimpleUDPClient(
    "127.0.0.1",
    9000
)


# Main Menu          #
while True:
    menu_prompt = input(
        Fore.CYAN+
        "\n\n| Select an option by number!"
        "\n\n1. | Custom Message!"
        "\n2. | Random Dictionary Definitions!"
        +Fore.RED+
        "\n3. | Close Script!"
        +Fore.CYAN+
        "\n\n> "
    )

    # Custom Message          #
    if menu_prompt == "1":
        while True:
            custom_message = input(
                "\n\n| Enter your custom message!"
                +Fore.YELLOW+
                "\n| Press ENTER to return to main menu"
                +Fore.CYAN+
                "\n\n> "
            )
            if custom_message.strip() == "":
                break
            client.send_message(
                "/chatbox/input",
                [
                    custom_message,
                    True
                ]
            )



    # Random Dictionary Definitions          #
    elif menu_prompt == "2":
        while True:
            try:
                loop_amount = int(input(
                    "\n\n| How many times would you like to loop?"
                    +Fore.YELLOW+
                    "\n| Input '0' to return to main menu."
                    +Fore.CYAN+
                    "\n\n> "
                ))
                if loop_amount == 0:
                    break
                elif loop_amount < 0:
                    print(
                        Fore.RED+
                        "\n\n| You can't loop negative numbers!"
                        +Fore.CYAN
                    )
                    sleep(2)
                    continue
            except ValueError:
                print(
                    Fore.RED+
                    "\n\n| Please enter a number!"
                    +Fore.CYAN
                )
                sleep(2)
                continue

            loops = 0
            for _ in range(loop_amount):
                while True:
                    try:
                        loops += 1

                        r = RandomWord()
                        search_term = r.word()

                        response = requests.get(
                            f"https://www.dictionary.com/browse/{search_term}",
                            headers={"User-Agent": "Mozilla/5.0"}
                        )

                        soup = BeautifulSoup(
                            response.text,
                            "html.parser"
                        )
                        message = soup.find(
                            "li",
                            class_="TOpzjFHcRBqzUMLLKa9s"
                        )


                        print(
                            f"\n\n| Loop Number: {loops}"
                            f"\n\n| Search Term: {search_term}"
                            f"\n| URL: {response.url}"
                        )
                        client.send_message(
                            "/chatbox/input",
                            [
                                f"{search_term}: {message.text[144:0:-1]}",
                                True
                            ]
                        )
                        sleep(15)
                        break
                    except AttributeError:
                        print(
                            Fore.RED+
                            "\n\n| Attribute Error! ( This is a debug print! )"
                            +Fore.CYAN
                        )
                        continue


    # Exit          #
    elif menu_prompt == "3":
        break


    else:
        print(
            Fore.RED+
            "\n\n| Invalid Input!"
            +Fore.CYAN
        )
        sleep(2)
        continue