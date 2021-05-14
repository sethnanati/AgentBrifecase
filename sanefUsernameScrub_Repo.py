from Validator import addressChecker, dataValidator
import config as dbconn
from time import sleep
from config import cdlDB
import re

def userNameFix():
    sanefConnection = dbconn.getSanefDBConnection()
    cursor2 = sanefConnection.cursor()


    sql = """SELECT * FROM Mblob WHERE RESPCODE NOT IN ('00' ,'32')"""
    cursor2.execute(sql)
    row = cursor2.fetchall()
    for rows in row:
        print(rows[27])
        if str(rows[27]) == 'Agent username exist':
            print(rows[27], 'yes')
            sql2 = f"""UPDATE Mblob SET USERNAME = '{rows[3]}', RESPMSG = '', RESPCODE = '' WHERE ADDITIONALINFO2 = '{rows[3]}'"""
            print(sql2)

        else:
            print(rows[27], 'No')


    cursor2.execute(sql2)
    sanefConnection.commit()
    print('data Updated successfully')
    sleep(2)

    cursor2.close()
    sanefConnection.close()


userNameFix()
