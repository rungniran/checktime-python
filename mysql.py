import pymysql
import datetime

con = pymysql.connect(host = "localhost", user = "root", password = "", db = "checktime" )

print("Attend (y) || Go out = (n) :")
x = input()

if x == 'y':
	while (True) :
		times = datetime.datetime.now()
		mycursor = con.cursor()
		T = times.strftime("%H:%M:%S")
		day = times.strftime("%d")
		namemonth = times.strftime("%B")
		month = times.strftime("%m")
		year = times.strftime("%Y")
		time = times.strftime("%d/%m/%Y")
		print(time)
		name = input("name = ")
		numberPersonnel = input("numberPersonnel = ")
		val = (name, numberPersonnel)
		sql = "SELECT * FROM listpersonnel WHERE name = (%s) and numberPersonnel = (%s)"
		mycursor.execute(sql, val)
		row = mycursor.fetchall()
		result = mycursor.rowcount
		# print (result)
		if result == 1:
			idListPersonnel = row[0][0]
			val = (idListPersonnel, day, month, year)
			sql = "SELECT * FROM worktime WHERE idListPersonnel = (%s) and day = (%s) and month = (%s) and year = (%s)"
			mycursor.execute(sql, val)
			result = mycursor.rowcount
			if result == 0:
				val = (idListPersonnel, T, day, month, year)
				sql = "INSERT INTO worktime (idListPersonnel, T, day, month, year) VALUES (%s, %s, %s, %s, %s)"
				mycursor.execute(sql, val)
				con.commit()
				print(numberPersonnel + " " + name + " Attend " + T )
				print("Success \n")
			else:
			    print("You make a list \n")	
		else:
			print("Not found name or numberPersonnel \n")
			

elif x == 'n':
	while (True) :
		times = datetime.datetime.now()
		mycursor = con.cursor()
		T = times.strftime("%H:%M")
		day = times.strftime("%d")
		namemonth = times.strftime("%B")
		month = times.strftime("%m")
		year = times.strftime("%Y")
		time = times.strftime("%d/%m/%Y")
		print(time)
		name = input("name = ")
		numberPersonnel = input("numberPersonnel = ")
		val = (name, numberPersonnel)
		sql = "SELECT * FROM listpersonnel WHERE name = (%s) and numberPersonnel = (%s)"
		mycursor.execute(sql, val)
		row = mycursor.fetchall()
		result = mycursor.rowcount
		print (result)
		if result == 1:
			val = (numberPersonnel, day, month, year)
			sql = "SELECT * FROM worktime WHERE idListPersonnel = (%s) and day = (%s) and month = (%s) and year = (%s)"
			mycursor.execute(sql, val)
			result = mycursor.rowcount
			row = mycursor.fetchall()
			if not row :
				print("No timestamp found upon entry.")
			elif result == 1:
				idWorkTime = row[0][0]
				val = (T, idWorkTime)
				sql = "UPDATE worktime  SET  Off_T  = (%s) WHERE idWorkTime = (%s)"
				mycursor.execute(sql, val)
				con.commit()
				print(numberPersonnel + " " + name + " get off " + T )
				print("Success \n")
			else:
			    print("You make a list \n")	
		else:
			print("Not found name or numberPersonnel \n")
		