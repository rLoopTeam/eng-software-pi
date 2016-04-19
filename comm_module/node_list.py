"""docstring for NodeManager"""
addresses = {
	'gs_in':'tcp://127.0.0.1:5556',
	'gs_out':'tcp://127.0.0.1:5557',
	'comm_in':'tcp://127.0.0.1:5558',
	'comm_out':'tcp://127.0.0.1:5559',
	'cmd_in':'tcp://127.0.0.1:5560',
	'cmd_out':'tcp://127.0.0.1:5561',
	'tele_out':'tcp://127.0.0.1:5562'
}

addresses_as_tuples = {
	'gs_in': ('tcp', '127.0.0.1', 5556),
	'gs_out': ('tcp', '127.0.0.1', 5557),
	'comm_in': ('tcp', '127.0.0.1', 5558),
	'comm_out': ('tcp', '127.0.0.1', 5559),
	'cmd_in': ('tcp', '127.0.0.1', 5560),
	'cmd_out': ('tcp', '127.0.0.1', 5561),
	'tele_out': ('tcp', '127.0.0.1', 5562)
}



def get_address(key):
	if key in addresses:
		return addresses[key]
	else:
		print("Key %s doesn't exist"%key)

def get_address_as_tuple(key):
	if key in addresses_as_tuples:
		return addresses_as_tuples[key]
	else:
		print("Key %s doesn't exist"%key)

	
	