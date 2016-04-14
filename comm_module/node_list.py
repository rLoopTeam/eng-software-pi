class NodeList():
	
	"""docstring for NodeManager"""
	nodes = {
		'gs_in':'tcp://127.0.0.1:5556',
		'gs_out':'tcp://127.0.0.1:5557',
		'comm_in':'tcp://127.0.0.1:5558',
		'comm_out':'tcp://127.0.0.1:5559',
		'cmd_in':'tcp://127.0.0.1:5560',
		'cmd_out':'tcp://127.0.0.1:5561',
		'tele_out':'tcp://127.0.0.1:5562'
	}

	def get_node(self, key):
		if key in self.nodes:
			return self.nodes[key]

		
		