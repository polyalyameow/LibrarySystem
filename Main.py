import os #importerar för att radera info som användaren inte behöver längre 
import re

import inquirer # importerar pick för att skapa en meny i terminalen
import random # generera ISBN för böcker
import re #regex för att validera e-postadress
from datetime import date, timedelta, datetime #räkna återlämningsdatum

from Book import Book 
from Account import *

#LOGGA IN 
def login():
#	options = ["[PERSONAL]", "[BESÖKARE]"] #val av inloggningar
#	option, index = pick.pick(options, "Logga in", indicator='=>', default_index=0)

	login_choices = ["PERSONAL", "BESÖKARE"]


	questions = [inquirer.List('login_choice', message="Logga in som", choices=login_choices)]
	answers = inquirer.prompt(questions)
	option = answers['login_choice']

	if option == "PERSONAL":
		print("PERSONAL")
	elif option == "BESÖKARE":
		print("BESÖKARE")
	signingIn = True
	while(signingIn):
		if option == "PERSONAL":
			password = input("\nPassword: ") 
			if password == "iLoveBooks": #kollar lösenord
				print("\nVälkommen till systemet!")
				signingIn = False #breaking the loop (personal)
				persRun()
		else:
			print("\nVälkommen till biblioteket!")
			signingIn = False	#breaking the loop (besökare)
	return option 

#PERSONAL_MENY
def persRun():
	persRunning = True
	while persRunning:
		#input("\nTRYCK PÅ VALFRI KNAPP FÖR ATT FORTSÄTTA")
		os.system('cls')

		questions = [
			inquirer.List('action',
						  message="Välj en åtgärd",
						  choices=["LÄGGA TILL EN BOK", "REDIGERA EN BOK", "RADERA EN BOK", "LISTA BÖCKER", "TILLBAKA"]
						  )
		]
		answers = inquirer.prompt(questions)
		choice = answers['action']

		if choice == "LÄGGA TILL EN BOK":
			addBooks()
		if choice == "REDIGERA EN BOK":
			editBooks()	
		if choice == "RADERA EN BOK":
			removeBooks()
		if choice == "LISTA BÖCKER":
			allBooks()
		if choice == "TILLBAKA":
			persRunning = False





#LÄGGA TILL BÖCKER
def addBooks():
#	options = ["LÄGGA TILL EN BOK", "TILLBAKA"]
#	choice, index = pick.pick(options, indicator='=>', default_index=0)
	options = [
		inquirer.List('action',
					  message="Fortsätt om du vill lägga till en bok",
					  choices=["LÄGGA TILL EN BOK", "TILLBAKA"])
	]

	answers = inquirer.prompt(options)
	choice = answers['action']

	if choice == "LÄGGA TILL EN BOK":
		name = str(input("Författarens namn och efternamn: "))
		title = input("Bokens titel: ")
		publ_year = validYear()
		ISBN = ISBNController()

		
		options = ["ja","nej"]
		booksO = Book(name, title, publ_year, ISBN) #håller input
	#	variable, index = pick.pick(options, "\nÄr du säker på att du vill lägga till "+ booksO.getTitle() + " av " + booksO.getAuthor() + " ?", indicator='=>', default_index=0)

		options = [
			inquirer.List('action',
						  message="\nÄr du säker på att du vill lägga till "+ booksO.getTitle() + " av " + booksO.getAuthor() + " ?",
						  choices=["ja", "nej"])
		]

		answers = inquirer.prompt(options)
		variable = answers['action']

		if variable == "ja":
			books.append(booksO) #skickar info till listan med alla böcker
			os.system('cls')
			print(booksO.present()) #presenterar information om boken
			print("\nBOKEN ÄR TILLAGD") 
			input("\nTRYCK PÅ VALFRI KNAPP FÖR ATT FORTSÄTTA")	
		elif variable == "nej":
			
			os.system('cls')
			print("\nINTE TILLAGD!") 			
			input("\nTRYCK PÅ VALFRI KNAPP FÖR ATT FORTSÄTTA")	

		elif choice == "TILLBAKA":
			login()


#KOLLAR ATT ISBN ÄR UNIK 								
def ISBNController():
	isbn = random.randint (1000000000000, 9999999999999)
	check = True
	while check:
		ISBNTaken = False
		for b in books:
			if isbn == b.getISBN():
				ISBNTaken = True

		if ISBNTaken == True:
			print("Detta ID finns redan. Försök igen")
		else:
			check = False
	return isbn	

# KOLLAR OM ANVÄNDAREN HAR ANGETT SIFFROR SAMT ÅR SOM EXISTERAR		
def validYear():
	while True:	
		try:
			publ_year = int(input("Utgivningsår: "))
			if type(publ_year) is int:
				if int(publ_year)>=1700 and int(publ_year) <=2023:
					return int(publ_year)
				else: 
					print("\nSKRIV IN ETT RIKTIGT ÅR\n")	
		except:
			print("\nENDAST HELTAL ÄR TILLÅTNA\n")

		

#REDIGERA BÖCKER															
def editBooks():  														
#	options = ["SÖK", "TILLBAKA"]
#	choice, index = pick.pick(options, "REDIGERA BÖCKER", indicator='=>', default_index=0)

	options = [
		inquirer.List('action',
					  message="REDIGERA BÖCKER",
					  choices=["SÖK", "TILLBAKA"])
	]

	answers = inquirer.prompt(options)
	choice = answers['action']

	if choice  == "SÖK": #sök-algoritmen
		searchWord = input("Ange författarens namn eller bokens titel för att hitta boken: ").capitalize() #ange namnet på boken eller författaren för att hitta rätt bok
		found = False
		alla = [] #lista för att hålla info 
		for b in books:
			if (searchWord in b.getAuthor()) or (searchWord in b.getTitle()):
				found = True
				alla.append(b.getTitle() + ", " + b.getAuthor() + ", ISBN: " + str(b.getISBN()))

		if found == False:
				print("INGA BÖCKER HITTADES")
		# använder try för att undvika traceback from pick.pick om boken inte har hittats i options
		try:	
			options = alla
			answers = inquirer.prompt(options)
			choice = answers['action']
			#choice, index = pick.pick(options, indicator='=>', default_index=0)
		
			for b in books: 	
				if (choice == b.getTitle() + ", " + b.getAuthor()  + ", ISBN: " + str(b.getISBN())):
					found = True

					#options = ["NAMN","TITELN", "UTGIVNINGSÅR", "TILLBAKA"]
					#variable, index = pick.pick(options, b.present() + "\n\n VÄLJ DEN BOK SOM SKA REDIGERAS", indicator='=>', default_index=0)

					options = [
						inquirer.List('action',
									  message="\n\n VÄLJ DEN BOK SOM SKA REDIGERAS",
									  choices=["NAMN", "TITELN", "UTGIVNINGSÅR", "TILLBAKA"])
					]

					answers = inquirer.prompt(options)
					variable = answers['action']

					if variable == "NAMN": #redigerar namn
						os.system('cls')
						nName = input("Författarens nya namn och efternamn: ")
						x = nName 
						
						#options = ["ja","nej"]
						#confirm, index = pick.pick(options, "Stämmer det att författarens förnamn och efternamn är " + x + " ?", indicator='=>', default_index=0)

						options = [
							inquirer.List('action',
										  message="Stämmer det att författarens förnamn och efternamn är " + x + " ?",
										  choices=["ja","nej"])
						]

						answers = inquirer.prompt(options)
						confirm = answers['action']
						
						if confirm == "ja":
							os.system('cls')
							b.setAuthor(nName) 
							print(b.present())
							input()
						if confirm == "nej":
							os.system('cls')
							input("TILLBAKA")


						
					elif variable == "TITELN": #redigerar titel
						os.system('cls')
						nTitle = input("Ny titel: ")	
						x = nTitle 
						
						#options = ["ja","nej"]
						#confirm, index = pick.pick(options, "Stämmer det att den nya titeln är " + x + " ?", indicator='=>', default_index=0)

						options = [
							inquirer.List('action',
										  message="Stämmer det att den nya titeln är " + x + " ?" + x + " ?",
										  choices=["ja", "nej"])
						]

						answers = inquirer.prompt(options)
						confirm = answers['action']
						
						if confirm == "ja":
							os.system('cls')
							b.setTitle(nTitle) 
							print(b.present())
							input()
						if confirm == "nej":
							os.system('cls')
							input("TILLBAKA")
						
					elif variable == "UTGIVNINGSÅR": #redigerar utgivningsår
						os.system('cls')
						nYear = input("Nytt utgivningsår: ")
						x = nYear 
						
						#options = ["ja","nej"]
						#confirm, index = pick.pick(options, "Stämmer det att det nya utgivningsåret är " + x + " ?", indicator='=>', default_index=0)

						options = [
							inquirer.List('action',
										  message="Stämmer det att det nya utgivningsåret är " + x + " ?",
										  choices=["ja", "nej"])
						]

						answers = inquirer.prompt(options)
						confirm = answers['action']
						
						if confirm == "ja":
							os.system('cls')
							b.setPubl_year(nYear) 
							print(b.present())
							input()
						if confirm == "nej":
							os.system('cls')
							input("TILLBAKA")

					elif  variable == "TILLBAKA":
						os.system('cls')
						input()	

		except:
			print("FÖRSÖK IGEN")
			input()
	if choice  == "TILLBAKA":
		input("\nTRYCK PÅ VALFRI KNAPP FÖR ATT FORTSÄTTA")

#TA BORT BÖCKER
def removeBooks():
	# använder try för att undvika traceback from pick.pick om boken inte har hittats i options
	try:
		#options = ["SÖK EN BOK SOM DU VILL TA BORT", "TILLBAKA"] #sök-algoritm
		#choice, index = pick.pick(options, "TA BORT EN BOK", indicator='=>', default_index=0)

		options = [
			inquirer.List('action',
						  message="TA BORT EN BOK",
						  choices=["SÖK EN BOK SOM DU VILL TA BORT", "TILLBAKA"])   #sök-algoritm
		]

		answers = inquirer.prompt(options)
		choice = answers['action']

		if choice  == "SÖK EN BOK SOM DU VILL TA BORT":
			searchWord = input("Sök: ").capitalize()
			#found = False
			alla = []
			for b in books:
				if (searchWord in b.getAuthor()) or (searchWord in b.getTitle()):
					alla.append(b.getTitle() + ", " + b.getAuthor() + ", ISBN: " + str(b.getISBN()))
					#found = True
			options = alla
			answers = inquirer.prompt(options)
			choice = answers['action']

			for b in books: 	
				if (choice == b.getTitle() + ", " + b.getAuthor()  + ", ISBN: " + str(b.getISBN())):
					#options = ["ja","nej"]
					#confirm, index = pick.pick(options, b.present()+ "\n" + "\nÄr du säker på att du vill ta bort "+ b.getTitle() + " av " + b.getAuthor() + ", ISBN: " + str(b.getISBN()) + "?", indicator='=>', default_index=0)
					options = [
						inquirer.List('action',
									  message= b.present()+ "\n" + "\nÄr du säker på att du vill ta bort "+ b.getTitle() + " av " + b.getAuthor() + ", ISBN: " + str(b.getISBN()) + "?",
									  choices=["ja", "nej"])
					]

					answers = inquirer.prompt(options)
					confirm = answers['action']


					if confirm == "ja":
						books.remove(b)
						os.system('cls')
						print("Boken " + b.getTitle() + " av " + b.getAuthor() + " har tagits bort")
						input()
					elif confirm == "nej":
						print("Tillbaka")	
		if choice  == "TILLBAKA":
			input("\nTRYCK PÅ VALFRI KNAPP FÖR ATT FORTSÄTTA")

	except:
		print("INGA BÖCKER HITTADES. FÖRSÖK IGEN")
		input()					



#LISTA ALLA BÖCKER
def allBooks():
	for obj in books:
		print('----------------\n' + obj.present())
	input("\nTRYCK PÅ VALFRI KNAPP FÖR ATT FORTSÄTTA")	


##################################################################################

# BESÖKARENS_MENY
def guestRun():
	guestRunning = True
	while guestRunning:
		#input("\nTRYCK PÅ VALFRI KNAPP FÖR ATT FORTSÄTTA")
		os.system('cls')

		options = [
			inquirer.List('action',
						  message="MENY | BESÖKARE",
						  choices=["SKAFFA BIBLIOTEKSKONTO", "LÅNA", "MINA LÅN", "LÄMNA", "TILLBAKA"])
		]

		answers = inquirer.prompt(options)
		sel = answers['action']


#		options = ["SKAFFA BIBLIOTEKSKONTO", "LÅNA", "MINA LÅN", "LÄMNA", "TILLBAKA"]
#		sel,index = pick.pick(options, "MENY | BESÖKARE: ", indicator='=>', default_index=0)

		if sel == "SKAFFA BIBLIOTEKSKONTO":
			createLibraryAccount() 
		if sel == "LÅNA":

			PNumber = checkIn() #logga in med personnummer
			
			if PNumber == "avbryt": #alt för att gå till menyn
				
				input("Du har avbrutit processen. Tryck valfri knapp för att återgå till menyn")
			else:		
				borrowBook(PNumber)	#fortsätta med att låna böcker


		if sel == "MINA LÅN":
			PNumber = checkIn() #logga in med personnummer  
			if PNumber == "avbryt":
				input("Du har avbrutit processen. Tryck valfri knapp för att återgå till menyn")

			else:		
				myAccount(PNumber) #gå till Mina lån med angett persN

		if sel == "LÄMNA":
			returnBook()
		if sel == "TILLBAKA":
			guestRunning = False

# SKAPA ETT KONTO PÅ BIBLIOTEKET
def createLibraryAccount():  
	print("\nFör att bli lånetagare på vårt bibliotek, behöver du skaffa ett bibliotekskonto hos oss\n")
	nameN = input("Skriv in ditt förnamn: ").capitalize()
	surnameN = input("Skriv in ditt efternamn: ").capitalize()

	persN = checkPersN() 
	if persN == "avbryt":
		input("Du har avbrutit registreringen. Tryck valfri knapp för att återgå till menyn")
	else:		
		pinN = checkpinN()
		emailN = checkEmailN()
		phoneN = checkPhoneN()
		info = Account(nameN, surnameN, persN, pinN, emailN, phoneN) #info håller objekt av klassen Account 

		#options = ["ja","nej"]
		#confirm, index = pick.pick(options, "\nKONTROLLERA ATT ALL INFORMATION STÄMMER\n\n"+ info.present(), indicator='=>', default_index=0)

		options = [
			inquirer.List('action',
						  message="\nKONTROLLERA ATT ALL INFORMATION STÄMMER\n\n"+ info.present(),
						  choices=["ja", "nej"])
		]

		answers = inquirer.prompt(options)
		confirm = answers['action']

		if confirm == "ja":
			accounts.append(info) #lägger info i listan med andra objekt av klassen Accounts
			
		elif confirm == "nej":
			os.system('cls')
			changeInfo(info)

#KOLLAR OM INFO STÄMMER OCH GER MÖJLIGHET ATT ÄNDRA DEN IFALL NÅT INTE STÄMMER
def changeInfo(info):
	

	#options = ["FÖRNAMN","EFTERNAMN", "PERSONNUMMER", "PIN KOD", "E-POSTADRESS", "TELEFONNUMMER", "TILLBAKA"]
	#variable, index = pick.pick(options, "VÄLJ DET SOM DU VILL REDIGERA\n", indicator='=>', default_index=0)

	options = [
		inquirer.List('action',
					  message="VÄLJ DET SOM DU VILL REDIGERA\n",
					  choices=["FÖRNAMN","EFTERNAMN", "PERSONNUMMER", "PIN KOD", "E-POSTADRESS", "TELEFONNUMMER", "TILLBAKA"])
	]

	answers = inquirer.prompt(options)
	variable = answers['action']

	if variable == "FÖRNAMN":
		changedName = input("Skriv in ditt förnamn: ").capitalize()
		info.setName(changedName)
		
		#options = ["ja","nej"]
		#confirm, index = pick.pick(options, "Stämmer det att ditt namn är "+ info.getName() + "?", indicator='=>', default_index=0)
		options = [
			inquirer.List('action',
						  message="Stämmer det att ditt namn är "+ info.getName() + "?",
						  choices=["ja", "nej"])
		]

		answers = inquirer.prompt(options)
		confirm = answers['action']


		if confirm == "ja":
			accounts.append(info)
			os.system('cls')
			print(info.present())
			changeInfo(info)
		if confirm == "nej":
			os.system('cls')
			changeInfo(info)
	if variable == "EFTERNAMN":
		changedSurname = input("Skriv in ditt efternamn: ").capitalize()
		info.setSurname(changedSurname)
		

		#options = ["ja","nej"]
		#confirm, index = pick.pick(options, "Stämmer det att ditt efternamn är "+ info.getSurname() + "?", indicator='=>', default_index=0)

		options = [
			inquirer.List('action',
						  message="Stämmer det att ditt efternamn är "+ info.getSurname() + "?",
						  choices=["ja", "nej"])
		]

		answers = inquirer.prompt(options)
		confirm = answers['action']

		if confirm == "ja":
			accounts.append(info)
			os.system('cls')
			print(info.present())
			changeInfo(info)
		if confirm == "nej":
			os.system('cls')
			changeInfo(info)

	if variable == "PERSONNUMMER":
		changedPersN = checkPersN()
		if changedPersN == "avbryt":
			input("Du har avbrutit registreringen. Tryck valfri knapp för att återgå till menyn")
		else:
			info.setPersN(changedPersN)
			
			#options = ["ja","nej"]
			#confirm, index = pick.pick(options, "Stämmer det att ditt personnummer är "+ str(info.getPersN()) + "?", indicator='=>', default_index=0)

			options = [
				inquirer.List('action',
							  message="Stämmer det att ditt personnummer är "+ str(info.getPersN()) + "?",
							  choices=["ja", "nej"])
			]

			answers = inquirer.prompt(options)
			confirm = answers['action']

			if confirm == "ja":
				accounts.append(info)
				os.system('cls')
				print(info.present())
				input()
				changeInfo(info)
			if confirm == "nej":
				os.system('cls')
				changeInfo(info)

	if variable == "PIN KOD":
		changedPin = checkpinN()
		info.setPin(changedPin)
		 
		#options = ["ja","nej"]
		#confirm, index = pick.pick(options, "Stämmer det att din pin kod är "+ str(info.getPin()) + "?", indicator='=>', default_index=0)

		options = [
			inquirer.List('action',
						  message="Stämmer det att din pin kod är "+ str(info.getPin()) + "?",
						  choices=["ja", "nej"])
		]

		answers = inquirer.prompt(options)
		confirm = answers['action']


		if confirm == "ja":
			accounts.append(info)
			os.system('cls')
			print(info.present())
			changeInfo(info)
		if confirm == "nej":
			os.system('cls')
			changeInfo(info)


	if variable == "E-POSTADRESS":
		changedEmail = checkEmailN()
		info.setEmail(changedEmail)

		#options = ["ja","nej"]
		#confirm, index = pick.pick(options, "Stämmer det att din e-postadress är "+ str(info.getEmail()) + "?", indicator='=>', default_index=0)

		options = [
			inquirer.List('action',
						  message="Stämmer det att din e-postadress är "+ str(info.getEmail()) + "?",
						  choices=["ja", "nej"])
		]

		answers = inquirer.prompt(options)
		confirm = answers['action']

		if confirm == "ja":
			accounts.append(info)
			os.system('cls')
			print(info.present())
			changeInfo(info)
		if confirm == "nej":
			os.system('cls')
			changeInfo(info)


	if variable == "TELEFONNUMMER":
		changedPhone = checkPhoneN()
		info.setPhone(changedPhone)

		#options = ["ja","nej"]
		#confirm, index = pick.pick(options, "Stämmer det att ditt telefonnummer är "+ str(info.getPhone()) + "?", indicator='=>', default_index=0)

		options = [
			inquirer.List('action',
						  message="Stämmer det att ditt telefonnummer är "+ str(info.getPhone()) + "?",
						  choices=["ja", "nej"])
		]

		answers = inquirer.prompt(options)
		confirm = answers['action']

		if confirm == "ja":
			accounts.append(info)
			os.system('cls')
			print(info.present())
			changeInfo(info)
		if confirm == "nej":
			os.system('cls')
			changeInfo(info)


	if variable == "TILLBAKA":
		input()


# LOGGA IN I SYSTEMET
def checkIn():                  
	print("DU BEHÖVER LOGGA IN FÖRST")
	
	retvalue = 0 #personnummer eller 0 om man inte vill ange persn
	match = False
	locked = True 

	while locked: #loopar fram tills program får korrekt persN alt. loopen avbryts vid avbryt-kommando
		PNumber = checkPersN()
		if PNumber == "avbryt": #alt för att gå till menyn
			retvalue = PNumber
			break 
		else: #alt för att gå till menyn	
			Ppin = checkpinN()	
			for account in accounts:
				if (account.getPersN() == PNumber) and (account.getPin() == Ppin): #kollar att båda persN och pin kod stämmer
						name = account.getName().upper()
						surname = account.getSurname().upper()
						os.system('cls')
						
						match = True
				
			if match == True:
				print ("\nVÄLKOMMEN TILL BIBLIOTEKET, " + name + " " + surname + "\n") 
				locked = False
				retvalue = PNumber 
			else:
				print("\nDu har angett fel personnummer och/eller pin kod. Testa igen!")	
	#input()
	return retvalue

# KOLLAR OM PERSONNUMMER BESTÅR AV 10-12 SIFFROR
def checkPersN():
	result = 0
	matched = False

	while matched == False:			
			persN = input("\nSkriv avbryt för att avbryta.\nPersonnummer: ")
			if persN == "avbryt": #alt för att gå till menyn
				result = persN
				matched = True
			else:
				try:
					if type(int(persN)) is int: #kollar om persN består av siffror
						if len(str(persN)) == 10 or len(str(persN)) == 12:
							result = int(persN)
							matched = True
						
						else: 
							print("\nSKRIV IN ETT RIKTIGT PERSONNUMMER\n")	
				except:
					print("\nENDAST HELTAL ÄR TILLÅTNA\n")
	
	return result	


#KOLLAR OM PIN KOD BESTÅR AV FYRA SIFFROR
def checkpinN():
	while True:	
		try:
			pinN = int(input("Ange din pin kod (4 siffror): "))
			if type(pinN) is int:
				if len(str(pinN)) == 4:
					return int(pinN)
				else: 
					print("\nPIN KOD MÅSTE VARA FYRA SIFFROR\n")	
		except:
			print("\nENDAST HELTAL ÄR TILLÅTNA\n")

# KOLLAR FORMAT FÖR E-POSTADRESS
def checkEmailN():
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' #e-postadress format 
	while True:	
		emailN = input("Ange din e-postadress: ")	
		if(re.fullmatch(regex, emailN)): #matchar input med angett formaten
			return emailN
			False
		else:
			print("\nOGILTIG E-POSTADRESS\n")	

#KOLLAR FORMAT FÖR TELEFONNUMMER
def checkPhoneN():
	while True:
		phoneN = input("Ange ditt telefonnummer: ")

		if (len(str(phoneN)) != 10) or ((phoneN[:2]) != "07"):
			print("\nOGILTIGT TELEFONNUMMER. VÄNLIGEN ANGE DITT TELEFONNUMMER I FORMAT 07XXXXXXXX\n")  
		else: 
			return (str(phoneN))

# LÅNA EN BOK 	
def borrowBook(PNumber):
	#först logga in i systemet

	
		looping = True
		registredBooks = [] #håller titel + författare
		userBorrowedBooks = False #om anv väljer att bli klar utan att låna nåt
		isbns = [] #håller input

		while looping:
			#options = ["LÅNA NY BOK","KLAR"]
			#sel, index = pick.pick(options, "VÄLJ ALTERNATIV", indicator='=>', default_index=0)

			options = [
				inquirer.List('action',
							  message="VÄLJ ALTERNATIV",
							  choices=["LÅNA NY BOK","KLAR"])
			]

			answers = inquirer.prompt(options)
			sel = answers['action']

			if sel == "LÅNA NY BOK":
				scannedBook = input("\nScanna boken som du vill låna: ") # IMITATION AV ATT BOKEN SCANNAS. MAN BEHÖVER ANGE ISBN. 
				found = False
				for b in books:
			  		if (str(scannedBook) == str(b.getISBN())): #kollar om input matchar isbn i systemet
			  			if b.getStatus() == "Utlånad": 
			  				print("Boken är registrerad som utlånad. Kontakta personalen.")
			  				found = True #boken har hittats 
			  				input()
			  				os.system('cls')
			  			else:	
				  			b.setStatus("Utlånad")
				  			b.setRentedTo(PNumber) #länkar persN med en bok  	
				  			isbns.append(scannedBook)
				  			
				  			today = date.today() #kollar datum idag
				  			returnDate = today + timedelta(days=30) #kollar när boken måste lämnas tillbaka
				  			b.setReturnDate(returnDate)
				  			
				  			registredBooks.append(b.getTitle() + ", " +  b.getAuthor()) 
				  			userBorrowedBooks = True 
				  			found = True
				  			print(b.getTitle() + " är tillagd")

				  			input()
				  			os.system('cls')
				if found == False:
					os.system('cls')
					print("Boken hittades inte")


			if sel == "KLAR":

				looping = False #breaks the loop
				if userBorrowedBooks == True: #användaren har lånat en bok
					for reg in registredBooks:
						print(reg + " är nu utlånad till dig. Återlämningsdatum är " + str(returnDate))
					#options = ["SKRIVA UT ETT KVITTO","INGET KVITTO"]
					#sel, index = pick.pick(options, "VILL DU HA KVITTOT?", indicator='=>', default_index=0)

					options = [
						inquirer.List('action',
									  message="VILL DU HA KVITTOT?",
									  choices=["SKRIVA UT ETT KVITTO","INGET KVITTO"])
					]

					answers = inquirer.prompt(options)
					sel = answers['action']

					if sel == "SKRIVA UT ETT KVITTO":
						print("\nSkriver ut...") #immiterar utskrift
						input()
						os.system('cls')
						for reg in registredBooks:
							print("\n" + reg + " " + str(returnDate))
						for acc in accounts:
							if PNumber == acc.getPersN(): 
								for i in isbns: 
									acc.borrow(i) #går till func borrow in Acc och appendar isbn


					if sel == "INGET KVITTO":
						print("\n")
				print("\nHa en fin dag!")
				input()

# MINA LÅN
def myAccount(PNumber):
	for acc in accounts:
		if acc.getPersN() == PNumber: #kollar om användarens input matchar personnummer is sytemet

			for b in books:
				if str(b.getISBN()) in acc.getBorrowedBooks(): #kollar efter ISBN i lånade böcker
					print(b.getTitle() + " by " + b.getAuthor() + ". Återlämningsdatum är " + str(b.getReturnDate()))
			input()


def returnProcess():
	res = ""
	found = False

	scannedBook = input("\nScanna boken som du vill lämna: ") # IMITATION AV ATT BOKEN SCANNAS. MAN BEHÖVER ANGE ISBN. 
	for b in books:
		if (str(scannedBook) == str(b.getISBN())): #kollar om input stämmer överens med en av ISBN 
			if b.getStatus() == "Tillgänglig":	#om boken inte var utlånad från början
				print("Boken är inte utlånad.")
				found = True #hittar boken men den är inte utlånad

			else: 
				b.setStatus("Tillgänglig") #byta statusen
				rentTo = b.getRentedTo() #veta vem som har lånat boken (persN)
				b.setRentedTo("") 
				
				res = b.getTitle() + ", " +  b.getAuthor()
				
				print("Registrerad återlämning: ")
				print(res) 
				found = True #hittar och lämna tillbaka boken
				for acc in accounts:
					if str(acc.getPersN()) == str(rentTo): #kollar om persN som hängde ihop med boken finns i systemet
						acc.returned(scannedBook)	#boken tas bort från listan borrowedBooks

							
	if found == False: #om boken inte finns i systemet
		print("Boken har inte hittats i systemet")
	input()
	return res

def returnBook():
	looping = True
	registeredBooks = []
	hasReturned = False #True om boken var återlämnad
	while looping:
		found = False
		#options = ["LÄMNA EN BOK","KLAR"]
		#sel, index = pick.pick(options, "VÄLJ ALTERNATIV", indicator='=>', default_index=0)

		options = [
			inquirer.List('action',
						  message="VÄLJ ALTERNATIV",
						  choices=["LÄMNA EN BOK","KLAR"])
		]

		answers = inquirer.prompt(options)
		sel = answers['action']

		if sel == "LÄMNA EN BOK":
			res = returnProcess()
			if res != "": #res behöver läggas till registeredBooks bara om det finns nån value
				registeredBooks.append(res)
				hasReturned = True
			
		if sel == "KLAR":
			looping = False #eftersom användaren blev klar med återlämningen
			if hasReturned == True: #om någon bok var återlämnad
				options = ["SKRIVA UT ETT KVITTO","INGET KVITTO"] 
				sel, index = pick.pick(options, "VILL DU HA ETT KVITTO?", indicator='=>', default_index=0)
				if sel == "SKRIVA UT ETT KVITTO":
					print("\nSkriver ut...")
					input()
					os.system('cls')
					print("Återlämnad " + str(date.today()))
					for reg in registeredBooks: 
						print("\n" + reg)
					input()
					

				if sel == "INGET KVITTO":
					os.system('cls')
					print("Ha en fin dag!")
					input()
				

#LISTA FÖR ATT HÅLLA REGISTRERINGAR
accounts = []
accounts.append(Account("Anna", "Wellington", 198503041265, 1454, "anna.wellington@gmail.com", "0765475445"))
accounts.append(Account("Kent", "Borås", 197801234065, 9897, "kent59@hotmail.se", "0772345743"))
accounts.append(Account("Maria", "Persson", 195611140612, 3445, "persmar@outlook.se", "0717457634"))



#LISTA FÖR ATT HÅLLA BÖCKER
books = []
books.append(Book("Virginia Woolf", "Mrs Dalloway", 1996, 3456789233456))
books.append(Book("Virginia Woolf", "Mrs Dalloway", 1996, 5678473956782))
books.append(Book("David Foster Wallace", "Infinite Jest", 2000, 5467375645456))
books.append(Book("David Foster Wallace", "A Supposedly Fun Thing I'll Never Do Again", 1997, 2345678345112))
books.append(Book("David Lipsky", "Although Of Course You End up Becoming Yourself", 2010, 2346784567223))
books.append(Book("Jonathan Franzen", "Crossroads", 2021, 5674758493210))
books.append(Book("Matilda Gustavsson", "Klubben", 2020, 3452347845678))
books.append(Book("Daniel Max", "Every love story is a ghost story", 2013, 5643278567834))
books.append(Book("Tolkien John Ronald Reuel", "The fellowship of the ring", 1991, 5634783456231))


accounts[0].borrow("2345678345112")
today = date.today()
returnDate = today + timedelta(days=30)
books[3].setStatus("Utlånad")
books[3].setReturnDate(returnDate)
books[3].setRentedTo("198503041265")
accounts[0].borrow("5634783456231")
books[8].setReturnDate(returnDate)
books[8].setStatus("Utlånad")
books[8].setRentedTo("198503041265")
###########################################

# START AV PROGRAMMET

while True:

	res = login()
	if res == "PERSONAL":
		persRun()
	elif res == "BESÖKARE":
		guestRun()