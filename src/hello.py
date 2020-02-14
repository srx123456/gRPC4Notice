from os import path

import hello_pb2
import hello_pb2_grpc


class Hello(hello_pb2_grpc.HelloServicer):
    FILE_NAME = './db.txt'

    def write_file(self, name, message):
        with open(self.FILE_NAME, 'a+') as f:
            f.writelines(f'{name}, {message}\n\n')
            # print(file)
        return None

    def Greet(self, request, context):
        file = ''
        self.write_file(name=request.name, message=request.message)
        with open(self.FILE_NAME, 'rb') as f:
            file = f.read()
        print(file)
        yield hello_pb2.HelloResponse(data=file)
        # response = hello_pb2.HelloResponse(data=file)



# hel = Hello()
# hel.write_file(name='s', message='sd')
