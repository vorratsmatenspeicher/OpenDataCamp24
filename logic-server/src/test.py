import session


def main():
    s = session.create_session()
    while 1:
        prompt = input(" --> ")
        s.get_response(prompt)


if __name__ == "__main__":
    main()
