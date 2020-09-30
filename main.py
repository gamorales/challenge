from commands import Commands

SHELL = '\033[96m'
ENDC = '\033[0m'

response = {}


def main():
    global response

    while True:
        try:
            word = input(f"{SHELL}challenge >>>{ENDC} ").lower()

            if word == "exit":
                break
            elif word == "help":
                Commands.print_help()
            elif len(word.strip().split(" ")) > 1:
                word_list = word.strip().split(" ")
                cmd = Commands(word_list[0], word_list[1:])
                response = cmd.run_command(response)
                print("\n"+str(response.get("msg", ""))+"")
            elif word == "print":
                if response.get("data", []):
                    print(f"\n{response.get('data')}")
                else:
                    print(f"\n{response.get('msg')}")
            else:
                print(word)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
