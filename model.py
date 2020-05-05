class Model:
	def __init__(self):
		self.fileName = None
	def isValid(self, fileName):
		try:
			file = open(fileName, 'r')
			file.close()
			return True
		except:
			return False
	def setFileName(self, fileName):
		if self.isValid(fileName):
			self.fileName = fileName
		else:
			self.fileName = ""
	def getFileName(self):
		return self.fileName