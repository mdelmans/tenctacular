from tentacular import device_callback, tenctarium

@device_callback('test')
def print_request(data, endpoint, uid):
	print(f'{uid}@{endpoint}:\n{data}')

tenctarium()