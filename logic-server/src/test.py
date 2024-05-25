import sys

import session


def main():
    import logging

    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='%(asctime)s %(levelname)s:%(message)s',
    #     handlers=[
    #         logging.FileHandler("app.log"),
    #         logging.StreamHandler(sys.stdout)
    #     ]
    # )

    s = session.create_session()
    prompt = "Begrüße einen neuen Benutzer."
    role = "system"
    while 1:
        it = s.get_response(prompt, role)
        role = "user"

        for token in it:
            print(token, end="", flush=True)

        print()
        prompt = input(" --> ")


if __name__ == "__main__":
    main()
