class Account:
	def __init__(self, name, surname, persN, pin, email, phone):
		self.name = name 
		self.surname = surname
		self.persN = persN
		self.pin = pin
		self.email = email
		self.phone = phone
		self.borrowedBooks = [] 


	def present(self):
		pres = "Namn är " + self.name + " " + self.surname + "\nPersonnummer är " + str(self.persN) + "\nPinkod är " + str(self.pin) + "\nE-postadress är " + str(self.email) + "\nTelefonnummer är " + str(self.phone)
		return pres

	#tar bort en bok from borrowedBooks (res syns i mina lån)
	def returned(self, ISBN):
		self.borrowedBooks.remove(str(ISBN))

	# lägger till en bok till borrowedBooks (res syns i mina lån)

	def borrow(self, ISBN):
		self.borrowedBooks.append(str(ISBN))


#accessor
	def getName(self):
		return self.name 


	def getSurname(self):
		return self.surname


	def getPersN(self):
		return self.persN


	def getPin(self):
		return self.pin

	def getEmail(self):
		return self.email

	def getPhone(self):
		return self.phone

	def getBorrowedBooks(self):
		return self.borrowedBooks


#mutator

	def setName(self, name):
		self.name = name  


	def setSurname(self, surname):
		self.surname = surname

	def setPersN(self, persN):
		self.persN = persN 

	def setPin(self, pin):
		self.pin = pin 

	def setEmail(self, email):
		self.email = email

	def setPhone(self, phone):
		self.phone = phone

	def setBorrowedBooks(self, borrowedBooks):
		self.borrowedBooks = borrowedBooks