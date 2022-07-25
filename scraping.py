import configparser
from links import list_links
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient
from telethon import functions, types

# In the same way, you can also leave such channel
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon import connection, utils

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest

# Считываем учетные данные
# async def dump_all_participants(channel):
# 	"""Записывает json-файл с информацией о всех участниках канала/чата"""
# 	offset_user = 0    # номер участника, с которого начинается считывание
# 	limit_user = 20  # максимальное число записей, передаваемых за один раз
#
# 	all_participants = []   # список всех участников канала
# 	filter_user = ChannelParticipantsSearch('')
#
# 	while True:
# 		participants = await client(GetParticipantsRequest(channel,
# 			filter_user, offset_user, limit_user, hash=0))
# 		if not participants.users:
# 			break
# 		all_participants.extend(participants.users)
# 		offset_user += len(participants.users)
#
# 	all_users_details = []   # список словарей с интересующими параметрами участников канала
#
# 	for participant in all_participants:
# 		all_users_details.append({"id": participant.id,
# 			"first_name": participant.first_name,
# 			"last_name": participant.last_name,
# 			"user": participant.username,
# 			"phone": participant.phone,
# 			"is_bot": participant.bot})
#
# 	for i in all_users_details:
# 		print(i)
		# print(f'**********************\n', i['message'], f'\n\n')
#
# 	# with open('channel_users.json', 'w', encoding='utf8') as outfile:
# 	# 	json.dump(all_users_details, outfile, ensure_ascii=False)


async def dump_all_messages(channel, limit_msg):

	"""Записывает json-файл с информацией о всех сообщениях канала/чата"""
	offset_msg = 0    # номер записи, с которой начинается считывание
	# limit_msg = 1   # максимальное число записей, передаваемых за один раз

	all_messages = []   # список всех сообщений
	total_messages = 0
	total_count_limit = limit_msg  # поменяйте это значение, если вам нужны не все сообщения

	message = None
	while True:
		history = await client(GetHistoryRequest(
			peer=channel,
			offset_id=offset_msg,
			offset_date=None, add_offset=0,
			limit=limit_msg, max_id=0, min_id=0,
			hash=0))
		if not history.messages:
			break
		messages = history.messages   # может здесь не в цикле должно быть? Отступ уменьшить?
		for message in messages:
			if not message.message:  # если сообщение пустое, например "Александр теперь в группе"
				break
			all_messages.append(message.to_dict())
		offset_msg = messages[len(messages) - 1].id
		total_messages = len(all_messages)
		if total_count_limit != 0 and total_messages >= total_count_limit:
			break

	chat = await client.get_entity(message.chat_id)  # Получаем чат по ИД
	chat_username = f'@{chat.username} | {chat.title}'

	results_list = []
	for i in all_messages:
		title = i['message'].partition(f'\n')[0]
		body = i['message'].replace(title, '').replace(f'\n\n', f'\n')
		date = i['date'].strftime('%d.%m.%y %H:%M')
		results_dict = {
			'chat_name': chat_username,
			'title': title,
			'body': body,
			'date': date
		}
		results_list.append(results_dict)

	return results_list


async def main(list_links, limit_msg):
	results_list = []
	# n = 1
	for link in list_links:
		url = link
		# print(f'\n{n} - url = ', url)
		# n += 1
		try:
			channel = await client.get_entity(url)
		except Exception:
			private_url = url.split('/')[-1]
			await client(ImportChatInviteRequest(private_url))
			channel = await client.get_entity(url)

		results_list = await dump_all_messages(channel, limit_msg)
	return results_list


config = configparser.ConfigParser()
config.read("config.ini")

api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
phone = '+375296449690'

client = TelegramClient(username, api_id, api_hash)
client.start()

with client:
	client.loop.run_until_complete(main(list_links, limit_msg=1))
