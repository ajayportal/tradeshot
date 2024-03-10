from datetime import datetime

user_name = 'P443114'
password = '1234'
api_key= 'lTAcYaux'
feed_token = None
token_map = None
sec ='FD62Z4BWIAA3XBAP6HJJCGSZKE'
telegramapi = 'bot5788829070:AAF1otqZLfmEsxjj1Uq2y7609_aBS5jyuLk'
telegramchatid = '-1001622974584'
quantity = '50'
Robo_CE_PE_Buy_SL = '6'
Robo_CE_PE_Buy_Tgt = '12'
    
    
dt = datetime.now()
today=dt.strftime('%A')
if today=="Monday" or today=="Tuesday":
    sl_perc="135"
    
    
if today=="Wednesday" or today=="Friday":
    sl_perc="128"
    
if today=="Thursday" or today=="Saturday" or today=="Sunday":
    sl_perc="118"