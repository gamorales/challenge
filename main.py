from commands import Commands

SHELL = '\033[96m'
ENDC = '\033[0m'

response = {}


def main():
    global response

    while True:
        try:
            word = input(f"{SHELL}challenge >>>{ENDC} ").lower()
            params = word.strip().split(" ")

            if word == "exit":
                break
            elif word == "help":
                Commands.print_help()
            elif word.startswith("print"):
                if len(params) > 1:
                    print(response.get('filter').get(params[1], {}))
                else:
                    if response.get("data", []):
                        print(f"\n{response.get('data')}")
                    else:
                        print(f"\nNo data loaded!")
            elif len(params) > 1:
                cmd = Commands(params[0], params[1:])
                response = cmd.run_command(response)
                print("\n"+str(response.get("msg", ""))+"")
            else:
                print(word)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
