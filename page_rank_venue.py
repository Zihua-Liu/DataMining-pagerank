import numpy as np

dirt = "data_venue/"

# obtain total paper number by useing paper_ids.txt
#def total_paper_num(source_dir):
	#with open(source_dir + "paper_ids.txt", 'rb') as file:
		#_list = file.readlines()
	#return len(_list)
paper_num = 20989

def read_acl_meta_data(directory):
	dic = {}
	with open(directory + "acl-metadata.txt", 'rb') as file:
		for i in range(paper_num):
			paper_id = file.readline()
			cut_pos = paper_id.find('{'.encode("ascii"))
			paper_id = paper_id[cut_pos + 1:-2].decode("ascii")
			#print(paper_id)

			author = file.readline()
			cut_pos = author.find('{'.encode("ascii"))
			author = author[cut_pos + 1:-2]
			author = author.split(';'.encode("ascii"))
			cnt = 0
			for ele in author:
				#print(ele[0:1])
				if ele[0:1] == b' ':
					#print(ele)
					author[cnt] = ele[1:]
				cnt = cnt+1
			#print(author)

			title = file.readline()
			cut_pos = title.find('{'.encode("ascii"))
			title = title[cut_pos + 1:-2]
			#print(title)

			venue = file.readline()
			cut_pos = venue.find('{'.encode("ascii"))
			venue = venue[cut_pos + 1:-2]
			#print(venue)

			year = file.readline()
			cut_pos = year.find('{'.encode("ascii"))
			year = year[cut_pos + 1:-1].decode("ascii")
			temp = year[-1:]
			if temp == '}':
				year = year[:-1]
			else:
				file.readline()
			#print(year)
			file.readline()
			dic[paper_id] = [author, title, venue, year]
	return dic
whole_information_dictionary = read_acl_meta_data(dirt)

def build_venue_id_dictionary(directory):
	dic = {}
	reverse_dic = {}
	cnt = 0
	for ele in whole_information_dictionary:
		venue = whole_information_dictionary[ele][2]
		if not venue in dic.keys():
			dic[venue] = cnt
			reverse_dic[cnt] = venue
			cnt = cnt+1
	return dic, reverse_dic

venue_id_dictionary, id_venue_dictionary = build_venue_id_dictionary(dirt)

#print(venue_id_dictionary)
def build_matrix(size, directory):
	matrix = np.zeros((size, size))
	with open(directory + "acl.txt", 'rb') as file:
		_list = file.readlines()
		for ele in _list:
			cut_pos1 = ele.find(' '.encode("ascii"))
			cut_pos2 = cut_pos1 + 5
			source_paper = ele[:cut_pos1].decode("ascii")
			target_paper = ele[cut_pos2:-1].decode("ascii")
			if source_paper in whole_information_dictionary.keys():
				source_venue = whole_information_dictionary[source_paper][2]
			if target_paper in whole_information_dictionary.keys():
				target_venue = whole_information_dictionary[target_paper][2]
			matrix[venue_id_dictionary[source_venue]][venue_id_dictionary[target_venue]] = matrix[venue_id_dictionary[source_venue]][venue_id_dictionary[target_venue]] + 1
		for i in range(size):
			if matrix[i].sum() != 0:
				matrix[i] = matrix[i] / matrix[i].sum()
	return matrix

matrix = build_matrix(len(venue_id_dictionary), dirt)
print(matrix)

def cal_pagerank(size, matrix, alpha, loop_times):
	vec_result = np.ones((size, 1)) * (1.0 / size)
	vec_e = np.ones((size, 1)) * (1.0 / size)
	matrix_t = np.transpose(matrix)
	for i in range(loop_times):
		print("step: ", i)
		vec_result = np.dot(matrix_t, vec_result) * alpha + (1 - alpha) * vec_e
		print(vec_result)
	return vec_result

result = cal_pagerank(len(venue_id_dictionary), matrix, 0.8, 100)

with open(dirt + "venue_pagerank.txt", "wb") as file:
	buff = []
	cnt = 0
	for i in range(len(venue_id_dictionary)):
		buff.append("venue:  ".encode("ascii") 
			+ id_venue_dictionary[cnt] 
			+ "	pagerank: ".encode("ascii")
			 + str(result[cnt][0]).encode("ascii")
			  + '\n'.encode("ascii"))
		cnt = cnt + 1
	file.writelines(buff)
	print(cnt)
print("Finish calculating the pagerank of venue")
print(id_venue_dictionary[482])
