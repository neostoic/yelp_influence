"""
Utilities for file manipulation, graph processing, etc.
"""

import json
import networkx
import itertools


def highest_degree_node_in_graph(graph):
	"""
	Given a NetworkX graph, returns the node with highest degree.
	"""
	max_degree = 0
	max_degree_node = None
	for node, degree in graph.degree_iter():
		if degree > max_degree:
			max_degree = degree
			max_degree_node = node

	return max_degree_node


def read_graph_from_yelp_JSON_file(file_name='yelp_academic_dataset_user.json'):
	"""
	Given a Yelp dataset user file (with users in JSON format), returns a NetworkX
	graph of the users and their friendships.
	"""
	users_file = open(file_name)
	users = [json.loads(line) for line in users_file.readlines()]

	graph = networkx.Graph()
	for user in users:
		user_ID = user['user_id']
		graph.add_node(user_ID)
		for friend_ID in user['friends']:
			graph.add_edge(user_ID, friend_ID)

	return graph


def output_graph_to_D3_JSON_file(file_name='users_graph.json'):
	"""
	Given a NetworkX graph, writes the graph to a JSON file in a format suitable
	for displaying a D3 force-directed graph.
	"""
	JSON = {'nodes': [], 'links': []}
	for user_ID in graph.nodes_iter():
		JSON['nodes'] += [{'name': user_ID}]
	for friend_1_ID, friend_2_ID in graph.edges_iter():
		JSON['links'] += [{'source': friend_1_ID, 'target': friend_2_ID, 'value': 1}]

	with open(file_name, 'w') as output_file:
		json.dump(JSON, output_file)




