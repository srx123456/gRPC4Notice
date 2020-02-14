from __future__ import print_function
import logging
import threading
import time
import grpc

from io import BytesIO, open

import hello_pb2
import hello_pb2_grpc

_count = 0

messages = [{"name": "Dayo", "message": 'Thanks for using our service'},
            {"name": "Daniel", "message": 'Come a again sooner'},
            {"name": "Famuyiwa", "message": 'Thanks for coming back. Tres bien'}]


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


def greet_with_message(stub, name, message):
    start_time = time.time()
    response = stub.Greet(hello_pb2.HelloRequest(name=name, message=message))
    elapsed_time = (time.time() - start_time) * 1000
    print(response, f'in {elapsed_time}secs')
    for r in response:
        print(r)
    # with BytesIO(initial_bytes=response) as data:
    #     print(data)
    # count += 1
    # return response


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hello_pb2_grpc.HelloStub(channel)
        for message in messages:
            greet_with_message(stub, name=message['name'], message=message['message'])


if __name__ == '__main__':
    logging.basicConfig()
    run()
    # for_loop()
