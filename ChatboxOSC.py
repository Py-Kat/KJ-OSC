# Imports          #
from pythonosc import udp_client
from wonderwords import RandomWord
import requests
from bs4 import BeautifulSoup
from time import sleep
from colorama import Fore
import psutil
import GPUtil


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
        "\n3. | Hardware Info! ( Who cares? )"
        +Fore.RED+
        "\n4. | Close Script!"
        +Fore.CYAN+
        "\n\n> "
    )

    # Custom Message          #
    if menu_prompt == "1":
        while True:
            custom_message = input(
                "\n\n| Enter your custom message!"
                +Fore.YELLOW+
                "\n| Press ENTER to return to main menu!"
                +Fore.CYAN+
                "\n\n> "
            )
            if custom_message.strip() == "":
                break
            client.send_message(
                "/chatbox/input",
                [
                    f"| {custom_message}",
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
                    "\n| Input '0' to return to main menu!"
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
            breaking = False
            for _ in range(loop_amount):
                if breaking:
                    break
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
                            Fore.YELLOW+
                            f"\n\n| Loop Number: {loops} / {loop_amount}"
                            +Fore.RED+
                            "\n| Use CTRL+C to quit the loop."
                            +Fore.GREEN+
                            f"\n\n| Search Term: {search_term}"
                            f"\n| URL: {response.url}"
                            +Fore.CYAN
                        )
                        client.send_message(
                            "/chatbox/input",
                            [
                                f"{search_term}: {message.text[0:144:1]}",
                                True
                            ]
                        )
                        sleep(15)
                        break
                    except AttributeError as e:
                        print(
                            Fore.RED+
                            "\n\n| Attribute Error! ( This is a debug print! )"
                            f"\n\n{e}"
                            +Fore.CYAN
                        )
                        continue
                    except KeyboardInterrupt:
                        breaking = True
                        break


    # Hardware Info          #
    elif menu_prompt == "3":
        while True:
            hw_info_menu = input(
                "\n\n| Select an option by number!"
                +Fore.YELLOW+
                "\n| Press ENTER to return to main menu!"
                +Fore.CYAN+
                "\n\n1. | CPU Info"
                "\n2. | Memory Info"
                "\n3. | GPU Info"
                "\n\n> "
            )
            if hw_info_menu.strip() == "":
                break


            # CPU Info          #
            elif hw_info_menu == "1":
                percentage = psutil.cpu_percent(1)
                performance_cores = psutil.cpu_count(False)
                logical_cores = psutil.cpu_count() - performance_cores
                client.send_message(
                    "/chatbox/input",
                    [
                        f"| CPU Usage: {percentage}%"
                        f"\n| Performance Cores: {performance_cores}"
                        f"\n| Logical Cores: {logical_cores}",
                        True
                    ]
                )
                print(
                    Fore.GREEN+
                    "\n\n| Sent CPU Info!"
                    +Fore.CYAN
                )
                sleep(1.5)
                continue


            # RAM Info          #
            elif hw_info_menu == "2":
                ram_percentage = psutil.virtual_memory().percent
                ram_in_use = psutil.virtual_memory().used / 1000000000
                ram_free = psutil.virtual_memory().available / 1000000000
                client.send_message(
                    "/chatbox/input",
                    [
                        f"| RAM Usage: {ram_percentage} %"
                        f"\n| RAM In-Use: {ram_in_use:.1f} GB"
                        f"\n| RAM Free: {ram_free:.1f} GB",
                        True
                    ]
                )
                print(
                    Fore.GREEN+
                    "\n\n| Sent RAM Info!"
                    +Fore.CYAN
                )
                sleep(1.5)
                continue


            # GPU Info          #
            elif hw_info_menu == "3":
                gpus = GPUtil.getGPUs()
                if gpus:
                    for gpu in gpus:
                        gpu_name = gpu.name
                        gpu_usage = gpu.load
                        vram_in_use = gpu.memoryUsed / 1000
                        vram_free = gpu.memoryFree / 1000
                        client.send_message(
                            "/chatbox/input",
                            [
                                f"| GPU: {gpu_name}"
                                f"\n| GPU Usage: {gpu_usage * 100:.1f} %"
                                f"\n| VRAM In-Use: {vram_in_use:.1f} GB"
                                f"\n| VRAM Free: {vram_free:.1f} GB",
                            ]
                        )
                        print(
                            Fore.GREEN+
                            "\n\n| Sent GPU Info!"
                            +Fore.CYAN
                        )
                        sleep(1.5)
                        continue


                else:
                    print(
                        Fore.RED+
                        "\n\n| No GPU found!"
                        +Fore.CYAN
                    )
                    sleep(2)
                    continue


            else:
                print(
                    Fore.RED+
                    "\n\n| Invalid input!"
                    +Fore.CYAN
                )
                sleep(2)
                continue


    # Exit          #
    elif menu_prompt == "4":
        break


    else:
        print(
            Fore.RED+
            "\n\n| Invalid Input!"
            +Fore.CYAN
        )
        sleep(2)
        continue