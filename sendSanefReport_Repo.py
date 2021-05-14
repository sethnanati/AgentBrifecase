import config as dbconn
import json
import requests
from signatureEncoding256 import encrypt_string, rand_string
import authorizationEncoding64
from cryptoAESLatest import encrypt
from config import endpointsVPN
from time import sleep
#from . import error
import re
from sanefResponseErrorLog import getRespCode

def createAgentAPI():
    # Get the sql connection for SANEF Database
    sanefConnection = dbconn.getSanefDBConnection()
    cursor2 = sanefConnection.cursor()

    sql = """SELECT * FROM Mblob WHERE RESPMSG IS NULL"""
    cursor2.execute(sql)
    row = cursor2.fetchall()

    dataMsg = {}

    for agentDBrowResult in row:
        data = agentDBrowResult
        if str(data[4]) != 'None':
            dataMsg['additionalInfo1'] = ''
            dataMsg['additionalInfo2'] = ''
            dataMsg['bvn'] = (data[4])
            dataMsg['city'] = str(data[5]).capitalize()
            dataMsg['emailAddress'] = str(data[6]).lower()
            dataMsg['latitude'] = '6.6000'
            dataMsg['longitude'] = '6.6000'
            dataMsg['lga'] = 'DEFAULT'
            dataMsg['state'] = str(data[10]).capitalize()#dataValidator(str(data[10]).capitalize())  # data[10]
            dataMsg['firstName'] = str(data[11]).capitalize()
            dataMsg['lastName'] = str(data[12]).capitalize()
            dataMsg['middleName'] = str(data[13]).capitalize()
            dataMsg['title'] = 'Mr'
            dataMsg['phoneList'] = ([str(data[15]).strip()])
            dataMsg['servicesProvided'] = ["CASH_IN", "CASH_OUT"]
            dataMsg["username"] = str(data[15]).lower().replace(" ", "")#data[19]
            dataMsg['streetNumber'] = str(data[20])
            dataMsg['streetName'] = str(data[21]).replace("/","")
            dataMsg['streetDescription'] = str(data[22]).replace("/","")
            dataMsg['ward'] = str('DEFAULT')
            dataMsg['password'] = '@Password1'
            #str(rand_string())

            json_data = json.dumps(dataMsg)
            #print('jsondata', json_data)
            print('=======sending create data Rest Message===============')

            try:
                #json.dumps(rdata)
                apiData = str(json.dumps(dataMsg)).encode('utf-8')
                serviceurl = endpointsVPN()['creatAgent']
                print('requestdata:', apiData)
                #print('url:', serviceurl)
                #sleep(2)

                base_data = encrypt(apiData)
                print('request:', base_data)
                headers = {"Authorization": authorizationEncoding64.authdecoded, "Signature": encrypt_string(),
                           "Content-Type": 'application/json', "Signature_Meth": 'SHA256'}
                response = requests.post(url=serviceurl, data=base_data, headers=headers, timeout=3)
                #print(response.text)
                error = response.text
                print(response.status_code)
                print(response.json())
                if response.status_code == 200:
                    code = response.json()['responseCode']
                    agentcode = response.json()['agentCode']
                    message = getRespCode()[code]
                else:
                    if response.status_code == 400:
                        if re.findall('code', error):
                            code = response.json()['responseCode']
                            agentcode = response.json()['code']
                            message = getRespCode()[code]
                        else:
                            code = response.json()['responseCode']
                            agentcode = ''
                            message = getRespCode()[code]
                    else:
                        code = ''
                        agentcode = ''
                        message = response.json()['message']

                print(code, agentcode, message)

                #print((str(message)[:32]))

                count = 0
                respparser = f"""UPDATE Mblob SET PASSWORD = '{dataMsg['password']}', AGENT_ID = '{agentcode}',
                                            RESPCODE = '{code}', RESPMSG = '{message}', USERNAME = '{str(data[15]).lower()}',
                                            ADDITIONALINFO3 = 'F' WHERE ADDITIONALINFO2 = '{str(data[3])}'"""
                print(respparser)

                try:
                    cursor2.execute(respparser)
                    count += cursor2.rowcount
                    print('Number of rows updated: ' + str(count))
                    # count += cursor2.rowcount
                    # print(count)
                    sanefConnection.commit()
                except ValueError as e:
                    print(e)
                    print(count, respparser)
                else:
                    print('Incomplete BVN_' + str(data[4]) + ' Data')

            except (requests.ConnectionError, requests.Timeout) as e:
                print(e)
            except requests.exceptions.HTTPError as e:
                print(e)


createAgentAPI()
