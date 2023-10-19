class Book: 
	def __init__(self, author, title, publ_year, ISBN):
		self.author = author
		self.title = title
		self.publ_year = publ_year
		self.ISBN = ISBN
		self.status = "Tillgänglig"
		self.returnDate = 0 #används för att räkna när man behöver lämna tillbaka böcker
		self.rentedTo = "" #persN av en person som lånar en bok

	def present(self):
		pres = "Författare - " + self.author + "\nTitel - " + self.title + "\nUtgivningsår - " + str(self.publ_year) + "\nISBN - " + str(self.ISBN) 
		return pres

#accessors
	def getReturnDate(self):
		return self.returnDate  


	def getTitle(self):
		return self.title	

	def getAuthor(self):
		return self.author

	def getPubl_year(self):
		return self.publ_year	

	def getISBN(self):
		return self.ISBN

	def getStatus(self):
		return self.status

	def getRentedTo(self):
		return self.rentedTo


#mutators
	def setReturnDate(self, returnDate):
		self.returnDate = returnDate

	def setAuthor(self, author):
		self.author = author 

	def setTitle(self, title):
		self.title = title 

	def setPubl_year(self, publ_year):
		self.publ_year = publ_year	

	def setStatus(self, status):
		self.status = status


	def setRentedTo(self, rentedTo):
		self.rentedTo = rentedTo