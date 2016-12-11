"""

Calculates Internet Provider approx. traffic per day use
If you have unlim unlim then you don't need it

"""
import sys
import traceback

from uztrafficcalc.providers.sarkor import Sarkor


# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    print("Выберите ваш интернет провайдер:\n" +
          "Internet provayderingizni tanlang:\n\n" +
          "1. Sarkor\n" +
          "2. UzOnline\n" +
          "3. TPS\n" +
          "4. Sharq\n" +
          "0. Exit")
    choice = input(">>  ")
    exec_menu(choice)

    return


# Execute menu
def exec_menu(choice):
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch][0](menu_actions[ch][1])
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return


def process(provider):
    if provider is None:
        print("Этот провайдер еще неработает.\nBu provayder hali ishlamaydi.")
        return

    # login
    while not provider.login(input("login: "), input("password: ")):
        print("Login or password incorrect.")

    provider.set_values()

    provider.print()


# Exit program
def exit():
    sys.exit()


# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': (process, Sarkor()),
    '2': (process, None),
    '3': (process, None),
    '4': (process, None),
    '0': exit,
}


def main():
    """
    main function
    """

    print("Добро подаловать на калькулятор траффикоф Узбекистана!\nO'zbekiston traffic kalkulyatoriga hush kelibsiz.\n")

    main_menu()


if __name__ == "__main__":

    # noinspection PyBroadException
    try:
        main()
    except KeyboardInterrupt:
        print("\nExecuting SIGINT (Ctrl - C)\n")
        sys.exit(0)
    except:
        print(traceback.format_exc())

    input("Press Enter to exit...")
