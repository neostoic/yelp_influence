"""
Utilities for the following:

          +-----------+        +----- THIS FILE ------+
          | raw_data/ | -----> | read from file(s)    |
          +-----------+        | build Python objects |        +--------------+
                               |                      | <----> | applications |
    +-----------------+        | export analysis to   |        +--------------+
    | processed_data/ | <----> | images, D3, etc.     |
    +-----------------+        +----------------------+

IMPORTANT: All data retrieval should be done through this file.
"""
from utilities import *
from data_utilities import *


def read_user_graph(input_file_name=DEFAULT_RAW_USERS_FILE_NAME):
	"""
	Given a Yelp dataset user file, returns a graph of the users and their friendships.
	"""
	graph = networkx.Graph()

	with open(raw_data_absolute_path(input_file_name)) as users_file:

		for user_line in users_file:
			user = json.loads(user_line)
			graph.add_node(user['user_id'])
			for friend_ID in user['friends']:
				graph.add_edge(user['user_id'], friend_ID)

	return graph


def read_user_average_review_lengths(input_file_name=DEFAULT_REVIEW_LENGTHS_FILE_NAME):
	"""
	Given a processed review lengths file, returns a dictionary:
		{ user ID: user's average review length }
	"""
	return read_single_user_attribute(input_file_name=input_file_name, attribute_name='average_review_length')


def read_user_average_reading_levels(input_file_name=DEFAULT_READING_LEVELS_FILE_NAME):
	"""
	Given a processed reading levels file, returns a dictionary:
		{ user ID: user's average reading level }
	"""
	return read_single_user_attribute(input_file_name=input_file_name, attribute_name='average_reading_level')


def read_user_tip_counts(input_file_name=DEFAULT_TIP_COUNTS_FILE_NAME):
	"""
	Given a processed tip counts file, returns a dictionary:
		{ user ID: user's tip count }
	"""
	return read_single_user_attribute(input_file_name=input_file_name, attribute_name='tip_count')


def read_user_pageranks(input_file_name=DEFAULT_PAGERANKS_FILE_NAME):
	"""
	Given a processed reading levels file, returns a dictionary:
		{ user ID: user's PageRank }
	"""
	return read_single_user_attribute(input_file_name=input_file_name, attribute_name='pagerank')


def read_user_basic_attributes(input_file_name=DEFAULT_BASIC_ATTRIBUTES_FILE_NAME):
	"""
	Given a processed basic attributes file, returns a list of user dictionaries containing all
	basic user attributes.
	"""
	return read_multiple_user_attributes(input_file_name=input_file_name, attributes=BASIC_USER_ATTRIBUTES)


def read_users(input_file_name=DEFAULT_COMBINED_USERS_FILE_NAME, attributes=ALL_USER_ATTRIBUTES):
	"""
	Given a combined users file and a list of desired attributes, returns a list of user dictionaries
	containing only those attributes.
	"""
	return read_multiple_user_attributes(input_file_name=input_file_name, attributes=attributes)


def write_D3_graph(graph, output_file_name=DEFAULT_D3_GRAPH_FILE_NAME):
	"""Writes a given graph to a JSON file suitable for displaying a D3 force-directed graph."""
	D3_dictionary = {'nodes': [], 'links': []}

	[ D3_dictionary['nodes'].append( {'name': user_ID} ) for user_ID in graph.nodes_iter() ]
	[ D3_dictionary['links'].append( {'source': friend_1_ID, 'target': friend_2_ID, 'value': 1} ) for friend_1_ID, friend_2_ID in graph.edges_iter() ]

	with open(processed_data_absolute_path(output_file_name), 'w') as D3_graph_file:
		json.dump(D3_dictionary, D3_graph_file)

