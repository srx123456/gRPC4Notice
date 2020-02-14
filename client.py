from __future__ import print_function
import logging
import threading
import time
import grpc

from io import BytesIO, open

import hello_pb2
import hello_pb2_grpc

from src.console import ask_name, ask_message

_count = 0

messages = []


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def for_loop():
    for message in messages:
        print(message)


def get_input():
    name = ask_name()
    message = ask_message()
    messages.append({"name": name, "message": message})
    print('Message Sent!!\n\nWould you like to send another one?[Yes/No] | [y/n]')
    another = input()
    if another.lower() == 'Yes' or another.lower() == 'y':
        get_input()
    else:
        return messages


def greet_with_message(stub, name, message):
    start_time = time.time()
    response = stub.Greet(hello_pb2.HelloRequest(name=name, message=message))
    elapsed_time = (time.time() - start_time) * 1000
    print(response, f'in {elapsed_time}secs')
    byte = [r for r in response][0].data
    with open('responses.txt', 'w+') as f:
        text = byte.decode(encoding='utf-8')
        f.write(text)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hello_pb2_grpc.HelloStub(channel)
        # for message in messages:
        messages_ = get_input()
        for message in messages_:
            greet_with_message(stub, name=message['name'], message=message['message'])


if __name__ == '__main__':
    logging.basicConfig()
    run()
    # for_loop()
