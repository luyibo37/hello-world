from random import randint

class Player():
	def __init__(self,name):
		self.name = name
		self._round = []

	@property
	def round(self):
		return self._round

	def add_round(self,trys=0):
		self._round.append(trys)

	def clear_round(self):
		self._round = []

	def add_trys(self,round_index):
		self._round[round_index] +=1

	def min_trys(self):
		return min(int(trys) for trys in self._round)

	def round_num(self):
		return len(self._round)

	def avg_trys(self):
		return float(sum(float(trys) for trys in self._round)/self.round_num())


def read_info(filepath):
	with open(filepath) as fin:
		file_data = fin.readlines()
	return file_data

def add_player_to_file(filepath,player):
	with open(filepath,'w') as fin:
		fin.write(player)

def play_game():
	print('新游戏，猜猜数字是几？')
	guess = randint(0,100)
	trys = 0
	while True:
		trys += 1
		print ('第 %d 次'% trys)
		num = input('请输入100以内整数: ')
		while not num.isdigit():
			num = input('请输入100以内整数: ')
		if int(num) > guess:
			print('输入太大\n')
		elif int(num) < guess:
			print('输入太小\n')
		else:
			print('猜中了！ 答案就是 %d ，本轮猜中一共用了 %d 次'%(guess, trys))
			break
	return trys

def play_round(player):
	while True:
		play = input('继续输入go，否则退出： ')
		if play == 'go':
			player.add_round(play_game())
			result_print(player)
		else:
			break

def result_print(player):
	print('玩家 %s, 一共玩了 %d 次游戏' % (player.name,player.round_num()))
	print('平均每轮 %.1f 次猜中 ！' % (player.avg_trys()))
	print('最好成绩 %d 次' % (player.min_trys()))

if __name__ == '__main__':
	#get player list
	player_file = r'player'
	players_info = read_info(player_file)
	player_names = []
	players = []
	for line in players_info:
		player_info = line.strip().split(' ')
		player_name = player_info[0]
		player_names.append(player_name)
		player = Player(player_name)
		for trys in player_info[1:]:
			player.add_round(int(trys.strip()))
		players.append(player)

	#start game or exit
	start = input('猜数字游戏: 开始(s) 或其他键退出 ')
	if start == 's':
		get_player = input('开始游戏，请输入玩家姓名：')
		if get_player in player_names:
			player_index = player_names.index(get_player)
			player = players[player_index]
			print('欢迎回来 %s，祝你游戏愉快！' % get_player)
			while True:
				player_status = input('加载记录(l)或重置记录(r): ')
				if player_status == 'l':
					break
				elif player_status == 'r':
					player.clear_round()
					break
		else:
			print('欢迎新玩家 %s'% get_player)
			players.append(Player(get_player))
			player_names.append(get_player)
			player_index = player_names.index(get_player)
			player = players[player_index]

		trys = play_game()
		player.add_round(trys)
		result_print(player)
		play_round(player)

		#save player info
		players_detail = ''
		for player in players:
			player_detail = player.name + ' ' + (' '.join(str(round) for round in player.round)) + '\n'
			players_detail = players_detail + player_detail
		add_player_to_file(player_file,players_detail)