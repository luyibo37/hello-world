import os

class Student():
	def __init__ (self,name,rank=0):
		self.name = name
		self.course_score={}
		self.rank = rank

	def sum_of_courses(self):
		return sum(float(self.course_score[course]) for course in self.course_score)

	def avg_of_courses(self):
		num = len(self.course_score)
		return self.sum_of_courses()/num

def read_report(filepath):
	with open(filepath,encoding='utf-8') as fin:
		file_data = fin.readlines()
	return file_data

def write_file(filepath,input_data):
	with open(filepath, 'a') as fin:
		fin.write(input_data)


if __name__ == '__main__':
	#read from file
	all_data = read_report(r'report.txt')
	out_file = 'result.txt'
	headers = all_data[0].strip().lstrip('\ufeff').split(' ')
	students = []
	for line in all_data[1:]:
		student_info = line.strip().split(' ')
		student_name = student_info[0]
		student = Student(student_name)
		for header_index in range(1,len(headers)):
			header = headers[header_index]
			student.course_score[header] = student_info[header_index]
		students.append(student)
	student_num = len(students)
	course_num = len(headers) - 1

	#sort student by sum of scores
	for j in range(0,student_num-1):
		for s in range(0,student_num-1):
			if students[s].sum_of_courses() < students[s+1].sum_of_courses():
				temp = students[s+1]
				students[s+1] = students[s]
				students[s] = temp
	for student_index in range(0,student_num):
		students[student_index].rank = student_index + 1

	#get avg data
	avgs = {}
	for header in headers[1:]:
		avg = []
		for student in students:
			avg.append(student.course_score[header])
		avgs[header] = sum(float(x) for x in avg)/student_num

	avgs['总分'] = sum(float(avgs[each_course]) for each_course in avgs)
	avgs['平均分'] = avgs['总分']/course_num
	avgs['名次'] = '0'
	avgs['姓名'] = '平均'

	students.insert(0,avgs)

	#append headers
	headers.insert(0,'名次')
	headers.append('总分')
	headers.append('平均分')
	#print headers
	print (' '.join(headers))
	add_str = ' '.join(headers)
	write_file(out_file,add_str)
	write_file(out_file, '\n')

	#print avg
	cur_str = ''
	for header in headers:
		if isinstance(avgs[header],float):
			this_data = str(format(avgs[header],'.1f'))
		else:
			this_data = str(avgs[header])
		cur_str = cur_str + ' ' + this_data
	print (cur_str)
	write_file(out_file,cur_str)
	write_file(out_file, '\n')
	#print students
	for student in students[1:]:
		cur_str = ''
		for header in headers:
			if header == '姓名':
				this_data = student.name
			elif header == '名次':
				this_data = str(student.rank)
			elif header == '平均分':
				this_data = str(format(student.avg_of_courses(),'.1f'))
			elif header == '总分':
				this_data = str(format(student.sum_of_courses(),'.1f'))
			else:
				this_data = str(format(float(student.course_score[header]),'.1f'))
			cur_str = cur_str + ' ' + this_data
		print (cur_str)
		write_file(out_file, cur_str)
		write_file(out_file,'\n')
