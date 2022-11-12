import math
import random
# Authors: Samuel Mirakov, Wade Li
# Date: October 24, 2022
# Class: Applied Machine Learning NLP
# Professor: Alla Rozovskaya

###########################################################################################################
'''									ID3 Decision Tree Algorithm 										'''

class Node:
	
	def __init__(self):
		self.children = []
		self.edge = []
		self.value = 'A'

	def isLeaf(self):
		return self.children == []

	def __str__(self):
		return self.value

# Training function: calculates the entropy
def calculate_Entropy(list):
    sum = 0.0
    for i in list:
        sum += -(i) * math.log(i, 2)
    return sum

# Training function: Adds words to dictionary, binary
def add_to_Dictionary(dict, value, label):
    if value in dict:
        if label == 'whether':
            dict[value][0] += 1
        else:
            dict[value][1] += 1
    else:
        if label == 'whether':
            dict[value] = [1, 0]
        else:
            dict[value] = [0, 1]

# Training function: Creates a tree with ID3- Decision Tree Algorithm,
# Finds feature w/ highest info gain --> Root
def calculate_ID3_Tree(root, features, height, bagOfWords):
	dict = {'whether': 0, 'weather': 0}
	list = []
	for i in range(len(features)):
		if features[i][len(features[i])-1] == 'whether':
			dict.update({'whether': dict['whether'] + 1})
		else:
			dict.update({'weather': dict['weather'] + 1})
	if height == 0:
		if dict['weather'] > dict['whether']:
      # weather will be predicted if majority is weather
			root.value = 'weather'
		else:
      # whether will be predicted if majority is whether
			root.value = 'whether'
		return
	for i in dict:
		if dict[i] != 0:
			list.append(dict[i] * 1.0 / (len(features)))
	current_entropy = calculate_Entropy(list)
	information_Gain = 0.0
	column = -1
	keys = []	
	for i in range(len(features[0]) - 1):
		dict = {}
		sum = 0.0
		for j in range(len(features)):
			add_to_Dictionary(dict, bagOfWords[i] + str(features[j][i]), features[j][len(features[j]) - 1])
		for j in dict:
			if dict[j][0] == 0 or dict[j][1] == 0:
				continue
			list = []
			total = dict[j][0] + dict[j][1]
			list.append(dict[j][0] * 1.0 / total)
			list.append(dict[j][1] * 1.0 / total)
			sum += calculate_Entropy(list) * (total * 1.0 / (len(features) - 1))
		if current_entropy - sum > information_Gain:
			information_Gain = current_entropy - sum
			column = i
			keys = dict.keys()
	root.value = bagOfWords[column]
	for i in keys:
		list2 = []
		bagOfWords_copy = bagOfWords[:]
		bagOfWords_copy.pop(column)
		nextNode = Node()
		for j in features:
			if j[column] == int(i[len(i)-1:]):
				list2.append(j[:])
		for j in range(len(list2)):
			list2[j].pop(column)
		root.children.append(nextNode)
		root.edge.append(i[len(i)-1:])
		flag = True
		for j in range(len(list2) - 1):
			if list2[j][len(list2[j]) - 1] != list2[j + 1][len(list2[j]) - 1]:
				flag = False
		if flag:
			nextNode.value = list2[0][len(list2[0]) - 1]
		else:	
			calculate_ID3_Tree(nextNode, list2, height - 1, bagOfWords_copy)

# function for printing the tree
def print_Tree(root, edge, level):
	if level > 1:
		s = ''
	else:
		s = edge
	for i in range(level):
		s += '	'
		if i == level - 2:
			s += edge
	print(s + str(root))
	for i in range(len(root.children)):
		print_Tree(root.children[i], root.edge[i], level + 1)
  
# Test function for testing accuracy of predictions
def accuracy_Test(root, data):
	count = 0
	for i in data:
		if i[-1] == predict_Label(root, i):
			count += 1
	return count * 1.0 / len(data)

# Test function for predicting the labels 
def predict_Label(root, s):
	if root.isLeaf():
		return root.value
	temp = s[bagOfWords.index(root.value)]
	if temp == int(root.edge[0]):
		return predict_Label(root.children[0], s)
	return predict_Label(root.children[1], s)

# Test function for filling the list, using a random number 
def fill_List(features, newFeatureList, finish):
	x = random.randint(0, 17400 - finish)
	val = finish
	for i in range(len(features)):
		if val > 0 and i >= x:
			newFeatureList.append(features[i])
			val -= 1
		elif val == 0:
			break
  
# opens the train file
data = open('hw1.train.col',  errors = "ignore")
features = []
# 60-words used as features using the bag-of-word model
bagOfWords = ['the', 'a', 'or', 'warm', 'forecast', 'forecasts', 'not', 'cold', 'temperature', 'climate',
              'balloon', 'deciding', 'sunny', 'winter', 'foggy', 'cloudy', 'question', 'accurate', 'determined', 'conditions',
              'bad', 'hot', 'good', 'scorching', 'windy', 'snowy', 'then', 'air', 'humid', 'determines',
              'fall', 'autumn', 'summer', 'hottest', 'known', 'unknown', 'unsure', 'know', 'decide', 'undecided',
              'predict', 'prediction', 'unpredictable', 'dry', 'wet', 'rainy', 'showery', 'measurement', 'clear', 'unclear',
              'forecasters', 'report', 'reporters', 'temperatures', 'fahrenheit', 'celsius', 'disaster', 'choice', 'choose', 'both']

# creates a list for each line in the train file
for i in data:
    temp = []
    list = i.strip().split(' ', 2)
    newlist = list[2].split()
    
    if( int(list[1]) >= len(list[2].split())):
        pass
    else:
        for j in bagOfWords:
            if j in list[2]:
                temp.append(1) 
            else:
                temp.append(0)
        temp.append(list[0])        
        features.append(temp)
# Closes the train file
data.close()

# Opens the value file
dataTest = open('hw1.test.col',  errors = "ignore")
# Creates a list for each line in the test file
featuresTest = []
for i in dataTest:
	temp = []
	list = i.strip().split(' ', 2)
	if( int(list[1]) >= len(list[2].split())):
		pass
	else:
		for j in bagOfWords:
			if j in list[2]:
				temp.append(1) 
			else:
				temp.append(0)
		temp.append(list[0])        
		featuresTest.append(temp)
# Closes the test file
dataTest.close()

# creates decision tree
root = Node()
bag_Of_Words = bagOfWords[:]
bagOfWords.append('#')

# prints the decision tree
# the third parameter is the current depth limit, change to your liking.
# Uncomment to print tree
'''
calTree(root, features, 5, bagOfWords)
printTree(root, '', 0)
'''
#100% with depth of 3
print("prints accuracy of the entire tree w/ depth of 3:\t")
calculate_ID3_Tree(root, features, 3, bag_Of_Words)
print(accuracy_Test(root, featuresTest))

#100% with depth of 5
print("prints accuracy of the entire tree w/ depth of 5:\t")
calculate_ID3_Tree(root, features, 5, bag_Of_Words)
print(accuracy_Test(root, featuresTest))

#100% with no depth limit
print("prints accuracy of the entire tree w/ no depth limit:\t")
calculate_ID3_Tree(root, features, -1, bag_Of_Words)
print(accuracy_Test(root, featuresTest))

newFeatureList = []

#80% with depth of 3
fill_List(features, newFeatureList, 13920)
calculate_ID3_Tree(root, newFeatureList, 3, bag_Of_Words)
print("prints accuracy of 80-percent of the training examples: \t")
print(accuracy_Test(root, featuresTest))
del newFeatureList[:]

#50% with depth of 3
fill_List(features, newFeatureList, 8700)
calculate_ID3_Tree(root, newFeatureList, 3, bag_Of_Words)
print("prints accuracy of half the training examples:\t")
print(accuracy_Test(root, featuresTest))
del newFeatureList[:]

#20% with depth of 3
fill_List(features, newFeatureList, 3480)
calculate_ID3_Tree(root, newFeatureList, 3, bag_Of_Words)
print("prints accuracy of 20-percent of the training examples:\t")
print(accuracy_Test(root, featuresTest))
del newFeatureList[:]

#10% with depth of 3
fill_List(features, newFeatureList, 1740)
calculate_ID3_Tree(root, newFeatureList, 3, bag_Of_Words)
print("prints accuracy of 10-percent of the training examples:\t")
print(accuracy_Test(root, featuresTest))