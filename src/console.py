

def ask_name():
    name = input("Input your name below\n+ Name:  ")
    if not name:
        print('Will swtich to DEFAULT name: Daniel')
        name = 'Daniel'
    print(name)
    return name


def ask_message():
    message = input("Input your message below\n+Message:  ")
    if not message:
        ask_message()
    else:
        return message


# ask_message()
