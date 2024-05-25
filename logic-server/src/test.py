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
    while 1:
        prompt = input(" --> ")
        it = s.get_response(prompt)

        for token in it:
            print("TOKEN", token)


if __name__ == "__main__":
    main()
