import sys
import gspread
import re
from subprocess import call
from oauth2client.service_account import ServiceAccountCredentials

def print_summary(sheet):
     print("")
     print("%s\t%s\t%s\t%s" % ('---','------','------','---------'))
     print("%s\t%s\t%s\t%s" % ('Cat','Budget','Actual','Remaining'))
     print("%s\t%s\t%s\t%s" % ('---','------','------','---------'))
     for rowspan in [3,5,6]:
          print("%s\t%s\t%s\t%s" % (sheet.cell(rowspan,1).value[0:4],sheet.cell(rowspan, 4).value, sheet.cell(rowspan, 5).value, sheet.cell(rowspan, 7).value)) 
     print("")

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_editor.json', scope)
client = gspread.authorize(creds)

sheet = client.open("General Budget Per Paycheck").sheet1
print_summary(sheet)


while True:
     addmode = input('Mode ([f]ood,[g]as,[m]isc,e[X]it)? ')
     if addmode == 'f':
          rownum = 3
     elif addmode == 'g':
          rownum = 5
     elif addmode == 'm':
          rownum = 6
     else:
          addmode = 'x'
          rownum = -1

     addstring = " "
     if rownum >= 0:
          addstring = input('Value to add: ')

     if (
          addstring.replace(".","",1).isnumeric() 
          or addstring[1:].replace(".","",1).isnumeric()
          and rownum >= 0
        ):
          if addstring[0:1] not in ('-','+'):
               addstring = '+' + addstring
          dadata = sheet.acell('E' + rownum, value_render_option='FORMULA')
          sheet.update_acell('E' + rownum, dadata + addstring)

          istransfer = input("Init Transfer to Visa (y/N)?")
          if istransfer == "y":
              call(["termux-sms-send","-n 93557","t " + re.sub(r"(\+|-)","",addstring) + " chk to visa"])

          print_summary(sheet)
     else:
          print("")
          if addmode == 'x':
              break
          else:
              print("*** Invalid Input ***")
              print("")

     if input("Another (y/N)? ") != "y":
          break
     
     print("")
#dadata = sheet.get_all_records()
