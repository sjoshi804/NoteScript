from __future__ import print_function
import networkx as nx 
import scipy
import matplotlib.pyplot as plt
import nlp
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.tokenize import word_tokenize


#target = "A galaxy has black holes. The universe contains black holes. Black holes are regions and have strong gravity. Region is space and doesn't let light escape."
#target ="One of the consequences of Einstein’s general theory of relativity was a solution in which space-time curved so much that even a beam of light became trapped. These solutions became called black holes, and the study of them is one of the most intriguing fields of cosmology. Application of string theory to study black holes is one of the most significant pieces of evidence in favor of string theory."
#target ="One of the consequences of Einstein’s general theory of relativity was a solution in which space-time curved so much that even a beam of light became trapped."
#target ="A black hole is a region of spacetime exhibiting such strong gravitational effects that nothing—not even particles and electromagnetic radiation such as light—can escape from inside it. The theory of general relativity predicts that a sufficiently compact mass can deform spacetime to form a black hole. The boundary of the region from which no escape is possible is called the event horizon. Although the event horizon has an enormous effect on the fate and circumstances of an object crossing it, no locally detectable features appear to be observed. In many ways a black hole acts like an ideal black body, as it reflects no light. Moreover, quantum field theory in curved spacetime predicts that event horizons emit Hawking radiation, with the same spectrum as a black body of a temperature inversely proportional to its mass. This temperature is on the order of billionths of a kelvin for black holes of stellar mass, making it essentially impossible to observe."
#target = "A short story is a piece of prose fiction that can be read in one sitting. Emerging from earlier oral storytelling traditions in the 17th century, the short story has grown to encompass a body of work so diverse as to defy easy characterization. At its most prototypical the short story features a small cast of named characters, and focuses on a self-contained incident with the intent of evoking a \"single effect\" or mood. In doing so, short stories make use of plot, resonance, and other dynamic components to a far greater degree than is typical of an anecdote, yet to a far lesser degree than a novel. While the short story is largely distinct from the novel, authors of both generally draw from a common pool of literary techniques. "
target = "A star is type of astronomical object consisting of a luminous spheroid of plasma held together by its own gravity. The nearest star to Earth is the Sun. Many other stars are visible to the naked eye from Earth during the night, appearing as a multitude of fixed luminous points in the sky due to their immense distance from Earth. Historically, the most prominent stars were grouped into constellations and asterisms, the brightest of which gained proper names. Astronomers have assembled star catalogues that identify the known stars and provide standardized stellar designations. However, most of the stars in the Universe, including all stars outside our galaxy, the Milky Way, are invisible to the naked eye from Earth. Indeed, most are invisible from Earth even through the most powerful telescopes."
sentences, salience = nlp.syntax_text(target.lower())

'''

sentence1 = {"galaxy": {"has":"black holes"}}
sentence2 = {"universe": {"contains":"black holes"}}
sentence3 = {"black holes":{"are":"region", "have":"strong gravity"}}
sentence4 = {"region":{"is":"space", "doesn't let": "light escape"}}
things = [sentence1,sentence2,sentence3,sentence4]
'''
def grapher(paragraphs, p_salience):

	allNodes = []
	nouns = []
	traversal_nouns = []
	para = paragraphs
	text = nx.DiGraph()
	salience = p_salience


	def addRemainingNodes():
		done = []
		for remaining in nouns:
			if remaining not in done:
				done.append(remaining)
				if not text.__contains__(remaining):
					text.add_node(remaining)
				remainingNodeHelper(remaining)

	def remainingNodeHelper(word):
		foundLink = False
		for sentence in para:
			if word in sentence:
				verbs = list(sentence[word].keys())
				for verb in verbs:
					obj = sentence[word][verb]
					if text.__contains__(obj):
						text.add_node(word,traversed=False)
						text.add_node(obj,traversed=False)
						text.add_edge(obj, word, label = verb, weightage = 1)
						uptrace(word)
						foundLink = True 
					else:
						text.add_node(word,traversed=False)
						text.add_node(obj,traversed=False)
						text.add_edge(word, obj, label = verb, weightage = 0)
						text.add_edge(obj, word, label = verb, weightage = -1)
		return foundLink

	def uptrace(word):
		for node in text.neighbors(word):
			if text.edges[word, node]['weightage'] == -1:
				text.remove_edge(parent, word)
				text.edges[word, node]['weightage'] = 1
				uptrace(node)
	'''
	def main():
		findNouns()
		traversal_nouns = nouns
		makeGraph()
		addRemainingNodes()
		makeNotes(1, "black holes", False)
	'''
	def findNouns():
		for sentence in para:
			subject = list(sentence.keys())[0]
			nouns.append(subject)
			nouns.extend(sentence[subject].values())

	def makeGraph():
		topics = [mostImportantToken]
		insertNode(mostImportantToken)


	def insertNode (word):
		for sentence in para:
			subjectPhrase = list(sentence.keys())[0]
			if word in subjectPhrase:
				removeAll(word, nouns)
				verbs = list(sentence[subjectPhrase].keys())
				for verb in verbs:
					obj = sentence[subjectPhrase][verb]						
					text.add_node(subjectPhrase,traversed=False)
					text.add_node(obj,traversed=False)
					text.add_edge(subjectPhrase, obj, weightage = 0, label = verb)
					if  obj != "":
						insertNode(obj)
					removeAll(obj, nouns)



	def removeAll (word, nouns):
		while nouns.count(word) != 0:
			nouns.remove(word)

	def removeAllNodes (subject, allNodes):
		while allNodes.count(subject) != 0:
			allNodes.remove(subject)

	def mostImportantWord():
		#return "black holes"
		salienceDict = {}
		#print(salience)	
		for d in salience:
			for key in d:
				try:
					salienceDict[key] += d[key]
				except:
					salienceDict[key] = d[key]


		biggest = ""

		for k in salienceDict:
			if biggest == "":
				biggest = k

			elif salienceDict[k] > salienceDict[biggest]:
				biggest = k

		tokenizer = word_tokenize(biggest)
		
		lm = WordNetLemmatizer()

		result = ""
		for token in tokenizer:
			lemma = lm.lemmatize(token)
			result += lemma +" "

		result = result[:len(result)-1]
		print("biggest: ",  result)
		return result
		

	def makeNotes(tabCount, headNode, isParent):
		if not isParent:
			text.nodes[headNode]['traversed'] = True
			removeAllNodes(headNode,allNodes)
			print (headNode)

		for child in text.neighbors(headNode):
			tabs = ""
			for x in range(0, tabCount):
				tabs += "\t"
			if  text.edges[headNode, child]['weightage'] == 1:
				if text.nodes[child]['traversed'] != True:
					print (tabs + " - " + child + " " + text.edges[headNode, child]['label'] + " it/them")
					text.nodes[child]['traversed'] = True
					removeAllNodes(child,allNodes)
					makeNotes(tabCount + 1, child, True)
			else:
				if text.nodes[child]['traversed'] != True:
					#print (tabs + " - " + text.edges[headNode, child]['label'], end = ' ' and text.nodes[child]['traversed'] != True)
					print (tabs + " - " + text.edges[headNode, child]['label'], end = ' ')
					text.nodes[child]['traversed'] = True
					removeAllNodes(child,allNodes)
					makeNotes(tabCount + 1, child, False)
		
		

	mostImportantToken = mostImportantWord()
	findNouns()
	traversal_nouns = nouns
	makeGraph()
	addRemainingNodes()

	found = False
	for sentence in para:
		subjects = list(sentence.keys())
		for tokens in subjects:
			if mostImportantToken in tokens:
				mostImportantToken = tokens
				found = True
				break
		if found:
			break

	allNodes=list(text.nodes());
	pos=nx.kamada_kawai_layout(text)
	nx.draw_networkx_nodes(text,pos,node_size=4500)
	nx.draw_networkx_edges(text,pos,width=3.0)
	nx.draw_networkx_labels(text,pos)
	nx.draw_networkx_edge_labels(text,pos,edge_labels=nx.get_edge_attributes(text,'label'))
	plt.title("Mind Map")
	plt.axis('off')
	plt.show()
	print (text.nodes.data())
	makeNotes(1, mostImportantToken, False)
	while(len(allNodes) != 0):
		makeNotes(1,allNodes[0],False)



grapher(sentences, salience)