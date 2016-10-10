import numpy as np 

# Since acl.txt is sorted by target paper
# We need reverse_acl.txt to bshow sorted source paper
dirt = "data_paper/"
def reverse_acl_txt(source_dir, target_dir):
	with open(source_dir + "acl.txt", 'rb') as file:
		_list = file.readlines()
	_list.sort()
	with open(target_dir + "reverse_acl.txt", 'wb') as file:
		file.writelines(_list)
#reverse_acl_txt(dirt, dirt)

# obtain total paper number by useing paper_ids.txt
def total_paper_num(source_dir):
	with open(source_dir + "paper_ids.txt", 'rb') as file:
		_list = file.readlines()
	return len(_list)
paper_num = total_paper_num(dirt)

def give_paper_id(source_dir, size):
	paper_id = {}
	id_paper = {}
	with open(source_dir + "paper_ids.txt", 'rb') as file:
		_list = file.readlines()
		_list.sort()
		for i in range(size):
			ele = _list[i]
			cut_pos = ele.find('	'.encode("ascii"))
			ele = ele[:cut_pos].decode("ascii")
			paper_id[ele] = i
			id_paper[i] = ele
	return paper_id, id_paper
dic, reverse_dic = give_paper_id(dirt, paper_num)

def construct_matrix(size):
	matrix = np.zeros((size, size))
	with open(dirt + "reverse_acl.txt") as file:
		_list = file.readlines()
		for ele in _list:
			cut_pos1 = ele.find(' ')
			cut_pos2 = cut_pos1 + 5
			source_paper = ele[:cut_pos1]
			target_paper = ele[cut_pos2:-1]
			matrix[dic[source_paper]][dic[target_paper]] = 1
		temp = np.zeros((size, 1))
		for i in range(size):
			temp[i] = matrix[i].sum()
		for _ele in _list:
			_cut_pos1 = _ele.find(' ')
			_cut_pos2 = _cut_pos1 + 5
			_source_paper = _ele[:_cut_pos1]
			_target_paper = _ele[_cut_pos2:-1]
			matrix[dic[_source_paper]][dic[_target_paper]] = 1 / temp[dic[_source_paper]]			
	return matrix
mat = construct_matrix(paper_num)

def cal_pagerank(size, matrix, alpha, loop_times):
	vec_result = np.ones((size, 1)) * (1.0 / size)
	vec_e = np.ones((size, 1)) * (1.0 / size)
	matrix_t = np.transpose(matrix)
	for i in range(loop_times):
		print("step: ", i)
		vec_result = np.dot(matrix_t, vec_result) * alpha + (1 - alpha) * vec_e
	return vec_result

result = cal_pagerank(paper_num, mat, 0.8, 100)

with open(dirt + "paper_pagerank.txt", "wb") as file:
	buff = []
	cnt = 0
	for i in range(paper_num):
		buff.append(("paper: " + reverse_dic[cnt] + " pagerank: " + str(result[cnt][0]) + '\n').encode('ascii'))
		cnt = cnt + 1
	file.writelines(buff)
	print(cnt)
