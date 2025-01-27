from flask import Flask, render_template, request, jsonify
import base64
import requests
from datetime import datetime
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/process-payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    print(f"Data from frontend {data}")
    package_name = data['packageName']
    package_amount = data['packageAmount']
    phone_number = data['phoneNumber']
    phone_number = phone_number.strip()

    if phone_number.startswith('07'):
        phone_number = '254' + phone_number[1:]
    
    response = sendStkPush(phone_number,package_amount)

    #Logging the received data
    print(f"Package: {package_name} @ {package_amount} for {phone_number}")

    return jsonify({"status":"success", "message":"Payment processed successfully"})




def generate_access_token():
    consumer_key = "J2EhCi7sG9XvBeSZKGGBEhQlaxRJn8c6"
    consumer_secret = "clS8XsGA3uibzTif"

    #choose one depending on you development environment
    #sandbox
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    #live
    # url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        
        encoded_credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

        # Send the request and parse the response
        response = requests.get(url, headers=headers).json()
        print(f"Your access token is {response['access_token']}")

        # Check for errors and return the access token
        if "access_token" in response:
            return response["access_token"]
        else:
            raise Exception("Failed to get access token: " + response["error_description"])
    except Exception as e:
        raise Exception("Failed to get access token: " + str(e)) 



def sendStkPush(phone_number,package_amount):
    token = generate_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortCode = "174379"  #sandbox -174379
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    stk_password = base64.b64encode((shortCode + passkey + timestamp).encode('utf-8')).decode('utf-8')

    
    
    #choose one depending on you development environment
    #sandbox
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    #live
    # url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    
    requestBody = {
        "BusinessShortCode": shortCode,
        "Password": stk_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline", #till "CustomerBuyGoodsOnline"
        "Amount": package_amount,
        "PartyA": phone_number,
        "PartyB": shortCode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://payment-test-1.onrender.com/callbackurl",
        "AccountReference": "account",
        "TransactionDesc": "test"
    }
    
    try:
        response = requests.post(url, json=requestBody, headers=headers)
        print(response.json())
        return response.json()
    except Exception as e:
        print('Error:', str(e))





import os
# Get the port from the environment variable or default to 5000
port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)