import time

def old_format_direct_messages(new_direct_messages):
	old_direct_messages = []
	for new_direct_message in new_direct_messages:
		old_direct_message = {}
		old_direct_message['id'] = int(new_direct_message['id'])
		old_direct_message['id_str'] = new_direct_message['id']
		old_direct_message['text'] = new_direct_message['message_create']['message_data']['text']
		old_direct_message['sender_id'] = int(new_direct_message['message_create']['sender_id'])
		old_direct_message['sender_id_str'] = new_direct_message['message_create']['sender_id']
		# todo complete user object - sender
		old_direct_message['sender'] = {
			'id': old_direct_message['sender_id'],
			'id_str': old_direct_message['sender_id_str']
		}
		# todo user sender screen name
		old_direct_message['recipient_id'] = int(new_direct_message['message_create']['target']['recipient_id'])
		old_direct_message['recipient_id_str'] = new_direct_message['message_create']['target']['recipient_id']
		# todo complete user recipient screen name
		old_direct_message['recipient'] = {
			'id': old_direct_message['recipient_id'],
			'id_str': old_direct_message['recipient_id_str']
		}
		old_direct_message['created_at'] = time.ctime(float(new_direct_message['created_timestamp']))
		old_direct_message['entities'] = new_direct_message['message_create']['message_data']['entities']

		old_direct_messages.append(old_direct_message)

	return old_direct_messages

