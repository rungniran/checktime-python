import pymysql
import datetime

times           = datetime.datetime.now()
con             = pymysql.connect(host = "localhost", user = "root", password = "", db = "checktime" )
mycursor        = con.cursor()
while True :
	name            = input("name = ")
	numberPersonnel = input("numberPersonnel = ")
	T               = times.strftime("%H:%M")
	day             = times.strftime("%d")
	month           = times.strftime("%m")
	year            = times.strftime("%Y")
	val             = (name, numberPersonnel)
	sql             = "SELECT * FROM listpersonnel WHERE name = (%s) and numberPersonnel = (%s)"
	mycursor.execute(sql, val)
	row    = mycursor.fetchall()
	result = mycursor.rowcount
	print (result)
	if result == 1:
		val = (numberPersonnel, day, month, year)
		sql = "SELECT * FROM worktime WHERE numberPersonnel = (%s) and day = (%s) and month = (%s) and year = (%s)"
		mycursor.execute(sql, val)
		result = mycursor.rowcount
		if result == 0:
			val         = (name, numberPersonnel, T, day, month, year)
			sql         = " INSERT INTO worktime (name, numberPersonnel, T, day, month, year) VALUES (%s, %s, %s, %s, %s, %s)"
			mycursor.execute(sql, val)
			con.commit()
			print("Success")
		else:
		    print("You make a list")	
	else:
		print("Not found name or numberPersonnel")
	