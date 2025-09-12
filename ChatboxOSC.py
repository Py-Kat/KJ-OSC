from pythonosc import udp_client
from faker import Faker
import requests
from bs4 import BeautifulSoup
from time import sleep
from colorama import Style, Fore
import psutil
import GPUtil
import winreg
import keyboard
from threading import Event

# Client          #
client = udp_client.SimpleUDPClient(
    "127.0.0.1",
    9000
)


# Send To OSC          #
def osc_send(where: str, text: str, pass_prompt: bool, notify: bool) -> None:
    """Sends a message to OSC!"""
    client.send_message(
        where,
        [
            text,
            pass_prompt,
            notify
        ])


# Get CPU Info
def get_cpu_name():
    key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
    )
    cpu_name = winreg.QueryValueEx(key, "ProcessorNameString")
    return cpu_name


# Main Menu          #
while True:
    menu_prompt = input(
        Fore.CYAN+
        "\n\n| Select an option by number!"
        "\n\n1. | Custom Message!"
        "\n2. | Random Dictionary Definitions!"
        "\n3. | Hardware Info!"
        +Fore.RED+
        "\n4. | Close Script!"
        +Fore.CYAN+
        "\n\n| > "
    )

    # Custom Message          #
    if menu_prompt == "1":
        while True:
            custom_message = input(
                "\n\n| Enter your custom message!"
                +Fore.YELLOW+
                "\n| Press ENTER to return to main menu!"
                +Fore.CYAN+
                "\n\n| > "
            )
            if custom_message.strip() == "":
                break
            osc_send(
                "/chatbox/input",
                f"| {custom_message}",
                True,
                True
            )
            print(
                Fore.GREEN+
                f"\n\n| Sent To OSC: {custom_message}"
                +Fore.CYAN
            )
            sleep(1.5)

    # Random Dictionary Definitions          #
    elif menu_prompt == "2":
        stop = Event()
        breaking = False
        while True:
            stop.clear()
            if breaking:
                break
            try:
                loop_amount = int(input(
                    "\n\n| How many times would you like to loop?"
                    +Fore.YELLOW+
                    "\n| Input '0' to return to main menu!"
                    +Fore.CYAN+
                    "\n\n| > "
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

            user_key = input(
                "\n\n| Please choose the KEYBOARD KEY you would like to temporarily bind as the 'quit' key!"
                + Fore.YELLOW +
                "\n\n| To avoid possible errors, please only use a letter key for now! ( Ex. 'q' will be SHIFT+Q )"
                "\n| The first character in this input is what will be used! ( Ex. 'qwerty' will still be SHIFT+Q! )"
                + Style.RESET_ALL +
                "\n\n| > "
            )

            bound_key = user_key[:1:]

            print(
                Fore.RED+
                f"\n\n| Use SHIFT+{bound_key.upper()} to quit the loop!"
                "\n( For now, there is quite a delay to this. )"
                +Style.RESET_ALL+
                "\n\n| Press SPACEBAR to begin! ( Ex. 'q' )\n"
            )
            keyboard.wait(
                "space",
                suppress=True
            )

            keyboard.add_hotkey(
                f"shift+{bound_key}",
                lambda: stop.set(),
                suppress=True
            )

            loops = 0
            try:
                while not stop.is_set():
                    try:
                        for _ in range(loop_amount):
                            while True:

                                if stop.is_set():
                                    breaking = True
                                    break

                                try:
                                    loops += 1

                                    fake = Faker()
                                    search_term = fake.word()

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
                                        f"\n| Use SHIFT+{bound_key.upper()} to quit the loop."
                                        +Fore.GREEN+
                                        f"\n\n| Search Term: {search_term}"
                                        f"\n| URL: {response.url}"
                                        +Fore.CYAN
                                    )
                                    osc_send(
                                        "/chatbox/input",
                                        f"{search_term}: {message.text[0:144:1]}",
                                        True,
                                        False
                                    )
                                    sleep(15)
                                    break

                                except AttributeError:
                                    continue
                    finally:
                        stop.set()
            finally:
                keyboard.remove_all_hotkeys()

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
                "\n\n| > "
            )
            if hw_info_menu.strip() == "":
                break

            # CPU Info          #
            elif hw_info_menu == "1":
                print(
                    Fore.YELLOW+
                    "\n\n| This takes a second..."
                    +Fore.CYAN
                )
                name = get_cpu_name()
                percentage = psutil.cpu_percent(1)
                cpu_cores = psutil.cpu_count()
                osc_send(
                    "/chatbox/input",
                    f"| {name}"
                    f"\n| CPU Usage: {percentage}%"
                    f"\n| CPU Cores: {cpu_cores}",
                    True,
                    False
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
                swap = psutil.swap_memory().total / 1000000000
                osc_send(
                    "/chatbox/input",
                    f"| RAM Usage: {ram_percentage} %"
                    f"\n| RAM In-Use: {ram_in_use:.1f} GB"
                    f"\n| RAM Free: {ram_free:.1f} GB"
                    f"\n| Swap: {swap:.1f} GB",
                    True,
                    False

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
                        osc_send(
                            "/chatbox/input",
                            f"| {gpu_name}"
                            f"\n| GPU Usage: {gpu_usage * 100:.1f} %"
                            f"\n| VRAM In-Use: {vram_in_use:.1f} GB"
                            f"\n| VRAM Free: {vram_free:.1f} GB",
                            True,
                            False
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