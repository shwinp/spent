import sys
import gspread
import re
import os
from subprocess import call
from oauth2client.service_account import ServiceAccountCredentials

def print_summary(sheet,addmode):
     print("")
     print("%s\t%s\t%s\t%s" % ('---','------','------','---------'))
     print("%s\t%s\t%s\t%s" % ('Cat','Budget','Actual','Remaining'))
     print("%s\t%s\t%s\t%s" % ('---','------','------','---------'))
     
     if addmode == 'f':
          rownum = [4]
     elif addmode == 'g':
          rownum = [6]
     elif addmode == 'm':
          rownum = [7]
     else:
          rownum = [4,6,7]

     for rowspan in rownum:
          print("%s\t%s\t%s\t%s" % (sheet.cell(rowspan,1).value[0:4],sheet.cell(rowspan, 4).value, sheet.cell(rowspan, 5).value, sheet.cell(rowspan, 7).value)) 
     print("")

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.path.dirname(__file__),'client_editor.json'), scope)
client = gspread.authorize(creds)

sheet = client.open("General Budget Per Paycheck").sheet1
#print_summary(sheet,'b')


while True:
     addmode = input('Mode ([f]ood,[g]as,[m]isc,[b]alance,[fw]ise,[mw]ise,[fm]art,[mm]art,e[X]it)? ')
     if addmode == 'f':
          rownum = 4 
          colnum = 'E'
     elif addmode == 'g':
          rownum = 6
          colnum = 'E'
     elif addmode == 'm':
          rownum = 7
          colnum = 'E'
     elif addmode == 'b':
          rownum = -1
          colnum = 'E'
     elif addmode == 'fw':
          rownum = 3
          colnum = 'K'
     elif addmode == 'mw':
          rownum = 3
          colnum = 'J'
     elif addmode == 'fm':
          rownum = 7
          colnum = 'K'
     elif addmode == 'mm':
          rownum = 7
          colnum = 'J'
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
          dadata = sheet.acell(str(str(colnum) + str(rownum)), value_render_option='FORMULA').value
          if len(dadata.strip()) == 0:
              dadata = "=0"
          sheet.update_acell(str(str(colnum) + str(rownum)), str(str(dadata) + str(addstring)))

          if addmode in ["f","g","m"]: 
            davalue = sheet.acell(str("G" + str(rownum)), value_render_option='UNFORMATTED_VALUE').value
            if davalue < 0:
              sheet.update_acell(str("G" + str(rownum)), "0")

          #istransfer = input("Init Transfer to Visa (y/N)?")
          #if istransfer == "y":
          #    call(["termux-sms-send","-n 93557","t " + re.sub(r"(\+|-)","",addstring) + " chk to visa"])

          print_summary(sheet,addmode)
     else:
          print("")
          if addmode == 'x':
              break
          elif addmode == 'b':
              print_summary(sheet,addmode)
          else:
              print("*** Invalid Input ***")
              print("")

     
     print("")
#dadata = sheet.get_all_records()
