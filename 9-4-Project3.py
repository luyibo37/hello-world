import time
import os

def write_file(filepath,record):
	with open(filepath,'a') as fin:
		fin.write(record)


def read_file(filepath):
	with open(filepath) as fin:
		record = fin.readlines()
	return record


def insert_record(filepath,records):
	fout = '\n' + (' '.join(str(record) for record in records))
	write_file(filepath,fout)


if __name__ == '__main__':
	#create debt file
	debt_file = r'debt.txt'
	daily_file = r'daily.txt'
	debt_header = '结算日期 资产/万 负债/万 净资产/万'
	daily_header = '交易对象 收入 支出 应收款项 应付款项 交易时间'
	if not os.path.exists(debt_file):
		write_file(debt_file,debt_header)
	#create daily account file
	if not os.path.exists(daily_file):
		write_file(daily_file,daily_header)

	while True:
		#read all debt status to list
		all_debt_status = read_file(debt_file)[1:]
		#read all daily account record to list
		all_daily_status = read_file(daily_file)[1:]

		print ('1.查账；2.记账')
		service = input('请选择服务：')
		if service == '1':
			print('\n查账模式')
			print('1.查询近十笔交易记录')
			print('2.查询与某公司交易来往')
			print('3.查询最近资产负债状况')
			sub_service = input('请选择服务：')
			if sub_service == '1':
				try:
					out_daily_status = all_daily_status[-10:]
				except IndexError:
					out_daily_status = all_daily_status
				out_daily_status.reverse()
				print(daily_header)
				print(''.join(str(record) for record in out_daily_status))
			elif sub_service == '2':
				company_name = input('请输入公司名称：')
				searched_record = []
				record_num = 0
				for daily_record in all_daily_status:
					if daily_record.split(' ')[0] == company_name:
						record_num += 1
						searched_record.append(daily_record)
				print('\n与%s共有%d笔交易' % (company_name,record_num))
				for company_info in searched_record:
					record = company_info.strip().split(' ')
					print('交易时间：%s' % record[5]) #print trade date
					print('收入：%s' % record[1]) #print income
					print('支出：%s' % record[2])
					print('应收款项：%s' % record[3])
					print('应付款项：%s' % record[4])
					print('\n')
			elif sub_service == '3':
				if len(all_debt_status) > 1:
					current_debt_status = all_debt_status[-1]
					status_list = current_debt_status.strip().split(' ')
					print('\n最新资产：%s' % status_list[1]) #asset
					print('最新负债：%s' % status_list[2])
					print('最新净资产：%s' % status_list[3])
					print('最后更新时间：%s' % status_list[0])
				else:
					print('无资产信息')
			else:
				print('无此服务\n')
				continue
		elif service == '2':
			try:
				print ('\n记账模式')
				trade_date = time.strftime('%Y-%m-%d',time.localtime())
				trade_company = input('交易对象： ')
				income = int(input('收入/万： '))
				outcome = int(input('支出/万： '))
				receive = int(input('应收账款/万： '))
				charge = int(input('应出账款/万： '))
				records = [trade_company,income,outcome,receive,charge,str(trade_date)]
				#insert daily record to file
				insert_record(daily_file,records)

				#get latest debt status
				latest_debt_status = all_debt_status[-1].split(' ')
				settle_date = latest_debt_status[0]
				asset = int(latest_debt_status[1])
				debt = int(latest_debt_status[2])
				net = int(latest_debt_status[3])

				#set current asset value
				cur_settle_date = time.strftime('%Y-%m-%d',time.localtime())
				cur_asset = asset + income - outcome
				cur_debt = debt + charge - receive
				cur_net = cur_asset - cur_debt
				current_debt_status = [str(cur_settle_date),cur_asset,cur_debt,cur_net]
				insert_record(debt_file,current_debt_status)

				#print to console
				print('\n交易已记录')
				print('当前资产状况：')
				print('最新资产：%d' % cur_asset)
				print('最新负债：%d' % cur_debt)
				print('最新净资产：%d' % cur_net)
			except ValueError:
				print ('\n输入错误')
		else:
			print('无此服务\n')
			continue
		print('\n')
