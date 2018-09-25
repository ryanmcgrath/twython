import time
import json


def load_users():
	try:
		with open('users.json', 'r') as f:
			users = json.load(f)
			return users
	except ValueError as e:
		print(e)
		return {}


def save_users(users):
	with open('users.json', 'w') as f:
		print('users saved')
		json.dump(users, f)


def old_format_direct_messages(new_direct_messages, get_user_object):
	users = load_users()
	new_user = False
	old_direct_messages = []
	for new_direct_message in new_direct_messages:
		old_direct_message = {}
		old_direct_message['id'] = int(new_direct_message['id'])
		old_direct_message['id_str'] = new_direct_message['id']
		old_direct_message['text'] = new_direct_message['message_create']['message_data']['text']
		old_direct_message['sender_id'] = int(new_direct_message['message_create']['sender_id'])
		old_direct_message['sender_id_str'] = new_direct_message['message_create']['sender_id']

		if not new_direct_message['message_create']['sender_id'] in users.keys():
			print('NEW USERRRR')
			print('SENDER ===> ', new_direct_message['message_create']['sender_id'])
			print('USER.KEYS ==>', users.keys())
			print(new_direct_message['message_create']['sender_id'])
			sender_object = get_user_object(user_id=new_direct_message['message_create']['sender_id'])
			new_user = True
		else:
			sender_object = users[new_direct_message['message_create']['sender_id']]

		users[new_direct_message['message_create']['sender_id']] = sender_object
		old_direct_message['sender'] = sender_object
		old_direct_message['sender_screen_name'] = sender_object['screen_name']

		old_direct_message['recipient_id'] = int(new_direct_message['message_create']['target']['recipient_id'])
		old_direct_message['recipient_id_str'] = new_direct_message['message_create']['target']['recipient_id']

		if not new_direct_message['message_create']['target']['recipient_id'] in users.keys():
			print('NEW USERRRR')
			print('RECIPIENT ===> ', new_direct_message['message_create']['target']['recipient_id'])
			print('USER.KEYS ==>', users.keys())
			print(new_direct_message['message_create']['target']['recipient_id'])
			recipient_object = get_user_object(user_id=new_direct_message['message_create']['target']['recipient_id'])
			new_user = True
		else:
			recipient_object = users[new_direct_message['message_create']['target']['recipient_id']]

		users[new_direct_message['message_create']['target']['recipient_id']] = recipient_object
		old_direct_message['recipient'] = recipient_object
		old_direct_message['recipient_screen_name'] = recipient_object['screen_name']

		old_direct_message['created_at'] = time.ctime(float(new_direct_message['created_timestamp']))
		old_direct_message['entities'] = new_direct_message['message_create']['message_data']['entities']

		old_direct_messages.append(old_direct_message)

	if new_user:
		save_users(users)

	return old_direct_messages

