from docker import Client
cli = Client(base_url='tcp://192.168.153.80:2375')
print(cli.containers())