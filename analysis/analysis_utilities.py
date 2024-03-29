"""
Utilities specifically for machine learning and data analysis.
"""
from utilities import *


def binarize_attribute(users, attribute):
	"""
	Given a list of user dictionaries and an attribute name, maps the designated attribute values
	of all users as follows:
		value = 0	-->		new value = 0
		value != 0	-->		new value = 1
	"""
	[ user.update( { attribute: int(bool(user[attribute])) } ) for user in users ]


def designate_attribute_as_label(users, attribute):
	"""
	Given a list of user dictionaries and an attribute name, replaces the designated attribute
	with a 'label' attribute which takes on the removed attribute's value.
	"""
	for user in users:
		user['label'] = user.pop(attribute)


def stratified_boolean_sample(users, label_name='label'):
	"""
	Given a list of user dictionaries with a Boolean label, returns a maximal sample of the users
	in which both labels are equally common.
	"""
	positive_samples = [user for user in users if user[label_name] == 1]
	negative_samples = [user for user in users if user[label_name] == 0]

	if len(positive_samples) < len(negative_samples):
		return positive_samples + random.sample(negative_samples, len(positive_samples))
	else:
		return random.sample(positive_samples, len(negative_samples)) + negative_samples


def remove_attribute(users, attribute):
	""" Deletes an attribute from all users in a list of user dictionaries. """
	[ user.pop(attribute, None) for user in users ]


def vectorize_users(users, attributes, label_name='label'):
	"""
	Given a list of user dictionaries, returns
		X : a list of vectors (lists), each representing the attribute values of a single user
		y : a list of corresponding correct labels for X

	NOTE: Output vectors respect ordering of input attributes: for every x in X, x[i] is the value
	of attribute attributes[i].
	"""
	user_vectors = []
	labels = []

	for user in users:
		user_vectors += [ [user[attribute] for attribute in attributes if attribute != label_name] ]
		labels += [ user[label_name] ]

	return user_vectors, labels


def partition_data_vectors(feature_vectors, labels, fraction_for_training=0.7):
	"""
	Given a list of feature vectors (lists) and their corresponding labels, returns:
		- A training set
		- A test set, disjoint from the training set
		- A recall test set (subset of test data labeled positive)

	NOTE: Does not sample randomly. Any randomization must be applied before using this utility.
	"""
	dataset_size = len(feature_vectors)
	training_set_size = int(fraction_for_training * dataset_size)
	test_set_size = dataset_size - training_set_size

	training_set = feature_vectors[0:training_set_size]
	training_set_labels = labels[0:training_set_size]
	test_set = feature_vectors[-test_set_size:]
	test_set_labels = labels[-test_set_size:]
	positive_test_set = [vector for i, vector in enumerate(test_set) if test_set_labels[i] == 1]
	positive_test_set_labels = [1]*len(positive_test_set)

	return training_set, training_set_labels, test_set, test_set_labels, positive_test_set, positive_test_set_labels


def normalize_users(users, excluded_attributes=[]):
	"""
	Given a list of user dictionaries whose attributes are numeric values, returns a list of
	users in which all attributes, EXCEPT those whose names are in excluded_attributes,
	are normalized to [0, 1].

	Normalization is done using min-max.
	"""
	excluded_attributes = set(excluded_attributes)

	# Find extreme values for each attribute
	max_user = {attribute: float('-infinity') for attribute in users[0].keys()}
	min_user = {attribute: float('infinity') for attribute in users[0].keys()}
	for user in users:
		for attribute, value in user.iteritems():
			if attribute not in excluded_attributes:
				max_user[attribute] = max(max_user[attribute], value)
				min_user[attribute] = min(min_user[attribute], value)

	# Normalize users
	for user in users:
		for attribute, value in user.iteritems():
			if attribute not in excluded_attributes:
				user[attribute] = float(value - min_user[attribute]) / (max_user[attribute] - min_user[attribute])

	return users


def show_histogram(values, value_name='Value', bins=100, range_to_display=(0,0), normed=False):
	if range_to_display == (0,0):
		n, bins, patches = pyplot.hist(values, bins=bins, normed=normed, facecolor='g', alpha=0.75)
	else:
		n, bins, patches = pyplot.hist(values, bins=bins, range=range_to_display, normed=normed, facecolor='g', alpha=0.75)
	pyplot.xlabel(value_name)
	pyplot.ylabel('Frequency')
	pyplot.title('Histogram of ' + value_name + 's')
	pyplot.axis('tight')
	pyplot.grid(True)
	pyplot.show()



