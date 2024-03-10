import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from datetime import datetime
import time
from st_on_hover_tabs import on_hover_tabs

st.set_page_config(layout="wide")




# Simulate some loading process (replace with your actual code)
import time
time.sleep(5)

with st.sidebar:
    selected = option_menu(
        menu_title="Trading",
        options=["Home", "Download", "Buy/Square-Off", "Sell/Square-Off", "Order Book"],
        icons=["house", "cloud-arrow-down-fill", "bag", "bag-fill", "book"],
        menu_icon="case",
        default_index=0,
         )
    
    
if selected == "Home":
    import streamlit as st
    import time


    

        
    
        
    
if selected == "Download":
    import requests
    from tqdm import tqdm
    import schedule
    st.title("Click download button to download json file")

    def download_file(url, filename):
        # Send a request to the URL to get the file size
        response = requests.head(url)
        file_size = int(response.headers.get('content-length', 0))
        
        # Open a progress bar
        
        
        # Make a request to download the file
        response = requests.get(url, stream=True)
        progress_bar = st.progress(0)
        status_text = st.empty()
        download_speed_text = st.empty()
        elapsed_time_text = st.empty()
        progress_text = st.empty()
        # Open a file for writing
        with open(filename, 'wb') as f:
            # Use tqdm to show progress
            with tqdm(total=file_size, unit='B', unit_scale=True) as pbar:
                start_time = time.time()
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
                        progress = min(int(100 * f.tell() / file_size), 100)
                        progress_bar.progress(progress)
                        status_text.text(f"Downloading... {progress}%")
                        elapsed_time = time.time() - start_time
                        download_speed = f"{(f.tell() / (1024 * elapsed_time)): .2f} KB/s"
                        download_speed_text.text(f"Download Speed: {download_speed}")
                        elapsed_time_text.text(f"Download Speed: {elapsed_time}")
                        remaining_time = (file_size - f.tell()) / (len(chunk) * 1024)  # Calculate remaining time in seconds
                        progress_text.text(f"Remaining Time: {remaining_time:.1f} seconds")
        
        success_alert = """
        <div style="position: relative;">
            <div style="display: inline-block; animation: slide-in 0.5s ease;">
                <div style="display: flex; align-items: center; background-color: #d4edda; border-color: #c3e6cb; color: #155724; padding: 0.75rem 1.25rem; border: 1px solid transparent; border-radius: 0.25rem;">
                    <span style="font-size: 1.5em; margin-right: 10px;">&#10004;</span> <!-- Tick mark symbol -->
                    <div>
                        <strong>Success!</strong> Your file download has completed.
                    </div>
                </div>
            </div>
        </div>

        <style>
        @keyframes slide-in {
            0% {
                transform: translateX(-100%);
                opacity: 0;
            }
            100% {
                transform: translateX(0%);
                opacity: 1;
            }
        }
        </style>
        """

        # Display the custom success alert
        st.write(success_alert, unsafe_allow_html=True)
        
        
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    
    
    
    if st.button("Download"):
        if url:
            filename = url.split("/")[-1]  # Extract filename from URL
            download_file(url, filename)
            
   
        


    

  
    
        
           
       
   
    
    
    
    
if selected == "Buy/Square-Off":
    
    if st.button("CE"):
        from SmartApi import SmartConnect 
        import pyotp
        from logzero import logger
        import pandas as pd
        import login as l
        from datetime import datetime
        import time

        api_key = l.api_key
        username = l.user_name
        pwd = l.password
        smartApi = SmartConnect(api_key)
        try:
            token = l.sec
            totp = pyotp.TOTP(token).now()
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        correlation_id = "abcde"
        data = smartApi.generateSession(username, pwd, totp)

        if data['status'] == False:
            logger.error(data)
            
        else:
            # login api call
            # logger.info(f"You Credentials: {data}")
            authToken = data['data']['jwtToken']
            refreshToken = data['data']['refreshToken']
            # fetch the feedtoken
            feedToken = smartApi.getfeedToken()
            # fetch User Profile
            res = smartApi.getProfile(refreshToken)
            smartApi.generateToken(refreshToken)
            res=res['data']['exchanges']
            
            data = pd.read_json('OpenAPIScripMaster.json')
            nifty_token = data.query('name=="NIFTY" and exch_seg=="NSE"')
            nifty_token=nifty_token['token'].loc[nifty_token.index[0]]    

            ltp=smartApi.ltpData("NSE", "NIFTY", nifty_token)
            Ltp = ltp['data']['ltp']

            RTM = int(round(Ltp/50)*50)
            print("\nATM Strike Price is: "+str(RTM))
            

            option_info = data.query('name=="NIFTY" and exch_seg=="NFO" and strike==@RTM*100')
            exp_info = pd.DataFrame(option_info['expiry'])
            exp_info['expiry'] = pd.to_datetime(exp_info['expiry'])
            sorted_exp_info = exp_info.sort_values(by='expiry')
            new = pd.DataFrame(sorted_exp_info)
           
             
            ce_index=sorted_exp_info.index[0]
            pe_index=sorted_exp_info.index[1]
            ce_symbol= option_info.loc[ce_index]['symbol']
            ce_token=option_info.loc[ce_index]['token']
            pe_symbol= option_info.loc[pe_index]['symbol']
            pe_token=option_info.loc[pe_index]['token']
            
            #print(ce_symbol)
            
            
            if ce_symbol.endswith('CE'):
                ce_index=sorted_exp_info.index[0]
                pe_index=sorted_exp_info.index[1]
                ce_symbol= option_info.loc[ce_index]['symbol']
                ce_token=option_info.loc[ce_index]['token']
                pe_symbol= option_info.loc[pe_index]['symbol']
                pe_token=option_info.loc[pe_index]['token']
                
            else:
                ce_index=sorted_exp_info.index[1]
                pe_index=sorted_exp_info.index[0]
                ce_symbol= option_info.loc[ce_index]['symbol']
                ce_token=option_info.loc[ce_index]['token']
                pe_symbol= option_info.loc[pe_index]['symbol']
                pe_token=option_info.loc[pe_index]['token']
                
        def place_order(token,symbol,exch_seg,buy_sell,ordertype,price):
            orderparams = {
    			"variety": "NORMAL",
    			"tradingsymbol": symbol,
    			"symboltoken": token,
    			"transactiontype": buy_sell,
    			"exchange": exch_seg,
    			"ordertype": ordertype,
    			"producttype": "CARRYFORWARD",
    			"duration": "DAY",
    			"price": price,
    			"squareoff": "0",
    			"stoploss": "0",
    			"quantity": "100"
    			}
            
            orderId=smartApi.placeOrder(orderparams)
            st.success("\nThe order id is:  " + orderId)
        	
               
        place_order(ce_token,ce_symbol,'NFO','BUY','MARKET',0)
        
         
    if st.button("PE"):
        from SmartApi import SmartConnect 
        import pyotp
        from logzero import logger
        import pandas as pd
        import login as l
        from datetime import datetime
        import time

        api_key = l.api_key
        username = l.user_name
        pwd = l.password
        smartApi = SmartConnect(api_key)
        try:
            token = l.sec
            totp = pyotp.TOTP(token).now()
        except Exception as e:
            logger.error("Invalid Token: The provided token is not valid.")
            raise e

        correlation_id = "abcde"
        data = smartApi.generateSession(username, pwd, totp)

        if data['status'] == False:
            logger.error(data)
            
        else:
            # login api call
            # logger.info(f"You Credentials: {data}")
            authToken = data['data']['jwtToken']
            refreshToken = data['data']['refreshToken']
            # fetch the feedtoken
            feedToken = smartApi.getfeedToken()
            # fetch User Profile
            res = smartApi.getProfile(refreshToken)
            smartApi.generateToken(refreshToken)
            res=res['data']['exchanges']
            
            data = pd.read_json('OpenAPIScripMaster.json')
            nifty_token = data.query('name=="NIFTY" and exch_seg=="NSE"')
            nifty_token=nifty_token['token'].loc[nifty_token.index[0]]    

            ltp=smartApi.ltpData("NSE", "NIFTY", nifty_token)
            Ltp = ltp['data']['ltp']

            RTM = int(round(Ltp/50)*50)
            print("\nATM Strike Price is: "+str(RTM))
            

            option_info = data.query('name=="NIFTY" and exch_seg=="NFO" and strike==@RTM*100')
            exp_info = pd.DataFrame(option_info['expiry'])
            exp_info['expiry'] = pd.to_datetime(exp_info['expiry'])
            sorted_exp_info = exp_info.sort_values(by='expiry')
            new = pd.DataFrame(sorted_exp_info)
           
             
            ce_index=sorted_exp_info.index[0]
            pe_index=sorted_exp_info.index[1]
            ce_symbol= option_info.loc[ce_index]['symbol']
            ce_token=option_info.loc[ce_index]['token']
            pe_symbol= option_info.loc[pe_index]['symbol']
            pe_token=option_info.loc[pe_index]['token']
            
            #print(ce_symbol)
            
            
            if ce_symbol.endswith('CE'):
                ce_index=sorted_exp_info.index[0]
                pe_index=sorted_exp_info.index[1]
                ce_symbol= option_info.loc[ce_index]['symbol']
                ce_token=option_info.loc[ce_index]['token']
                pe_symbol= option_info.loc[pe_index]['symbol']
                pe_token=option_info.loc[pe_index]['token']
                
            else:
                ce_index=sorted_exp_info.index[1]
                pe_index=sorted_exp_info.index[0]
                ce_symbol= option_info.loc[ce_index]['symbol']
                ce_token=option_info.loc[ce_index]['token']
                pe_symbol= option_info.loc[pe_index]['symbol']
                pe_token=option_info.loc[pe_index]['token']
                
        def place_order(token,symbol,exch_seg,buy_sell,ordertype,price):
            orderparams = {
    			"variety": "NORMAL",
    			"tradingsymbol": symbol,
    			"symboltoken": token,
    			"transactiontype": buy_sell,
    			"exchange": exch_seg,
    			"ordertype": ordertype,
    			"producttype": "CARRYFORWARD",
    			"duration": "DAY",
    			"price": price,
    			"squareoff": "0",
    			"stoploss": "0",
    			"quantity": "100"
    			}
            
            orderId=smartApi.placeOrder(orderparams)
            st.success("\nThe order id is:  " + orderId)
        	
               
        place_order(pe_token,pe_symbol,'NFO','BUY','MARKET',0)        
            

if selected == "Order Book":
    from SmartApi import SmartConnect 
    import pyotp
    from logzero import logger
    import pandas as pd
    import login as l
    from datetime import datetime
    import time

    api_key = l.api_key
    username = l.user_name
    pwd = l.password
    smartApi = SmartConnect(api_key)
    try:
        token = l.sec
        totp = pyotp.TOTP(token).now()
    except Exception as e:
        logger.error("Invalid Token: The provided token is not valid.")
        raise e

    correlation_id = "abcde"
    data = smartApi.generateSession(username, pwd, totp)

    if data['status'] == False:
        logger.error(data)
        
    else:
        # login api call
        # logger.info(f"You Credentials: {data}")
        authToken = data['data']['jwtToken']
        refreshToken = data['data']['refreshToken']
        # fetch the feedtoken
        feedToken = smartApi.getfeedToken()
        # fetch User Profile
        res = smartApi.getProfile(refreshToken)
        smartApi.generateToken(refreshToken)
        res=res['data']['exchanges']
        
        orderbook = smartApi.orderBook()
        df = pd.DataFrame(orderbook['data'])
        st.write(df)