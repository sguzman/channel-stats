import grpc
import logging

import lib
import lib.env
import lib.server_pb2 as server_pb2
import lib.server_pb2_grpc as server_pb2_grpc
import lib.log


def run():
	port: str = lib.env.port
	addr: str = f'localhost:{port}'
	logging.debug('Calling %s', addr)

	channel = grpc.insecure_channel(addr)
	stub = server_pb2_grpc.ViewsStub(channel)
	response = stub.view(server_pb2.ChannelID(name='UCL7DDQWP6x7wy0O6L5ZIgxg'))
	print("Greeter client received: " + response.message)


def main():
	logging.info('hi')
	run()
	logging.info('bye')


if __name__ == '__main__':
	main()
