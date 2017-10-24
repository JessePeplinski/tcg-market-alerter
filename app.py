import requests, json
from pprint import pprint
from time import sleep
import os

def getRequest(endpoint):
    """ 
    Returns a response in json format
    Params: The endpoint 
    """

    headers = {
        "Accept": "application/json",
        "Authorization": "bearer 7TUFM5BG2ikyTr5RQzNvFm3ALKC_7PUzGNcybO91WWny93bEzmmeeze0iXJNSisEno42aN2CKJIQOBr52ZeUeyFABfo1lq0aQDhCMJfsMFmC_l-FRCTeIN1DpqOHvkIgLmq5hlvUBk-q11VzNQZzA8L1QY4JoAGXEnXa-SojXw_2elYfzgpstXxtph9FcStOPX4YX0L1uDNPQAbO7gYLcbiD1d7qIoIA6wK71TO_WoDa10v6z-m1tNmYmhw98odThrSbkxhRJD9ktSAGOX8IgelS6TnkrsUGkzgxZjtGcMu_YnW_391vR7zJWwIPY-8LFc8Ueg"
    }

    response = requests.get(endpoint, headers=headers)

    # print(response.json()) # use for testing and debugging

    return response.json()

def getProducts():
    """ 
    Returns all of the products from the API endpoint
    """
    return "http://api.tcgplayer.com/catalog/products"

# TODO: Eventually make this accept multiple product ids with *productID
def getProductPrice(productID):
    """ 
    Returns the price of a product from the API endpoint
    Params: The ID of the product
    """
    return "http://api.tcgplayer.com/pricing/product/" + str(productID)

def writeProductsToFile():
    """ 
    Write all of the products from an API request to a file, products.json
    """
    # Call getProducts() and save file as JSON. Could also put to DB or use MyJson, but writing to file for simplicity right now
    data = getRequest(getProducts())

    # Try to create file
    try:
        # Store data in JSON file 
        with open('products.json', 'w') as outfile:
            json.dump(data, outfile)
            print("JSON file for products created!")
    except:
        print("Could not dump JSON to file")
        raise

def writePricesToFile(productID):
    """ 
    Write all of the prices from an API request to a file, products.json
    Params: The ID of the product
    """
    # Call getProductPrice() and save file as JSON. Could also put to DB or use MyJson, but writing to file for simplicity right now
    # TODO: !! want to call a list of ID's here instead of just one. 
    data = getRequest(getProductPrice(productID))

    try:
        # Store data in JSON file 
        with open('prices.json', 'w') as outfile:
            json.dump(data, outfile)
            print("JSON file for prices created!")
    except:
        print("Could not dump JSON to file")
        raise


def checkPrices(productID, email):
    """
    Compare the API endpoint request with the stored file, prices.json, and check if the prices are different
    """
    
    # Get the API endpoint
    server_response = getRequest(getProductPrice(productID))

    # Store the file in a var
    with open('prices.json') as data_file:    
        local_response = json.load(data_file)

    print('SERVER RESPONSE')
    pprint(server_response) # prints the JSON from the server

    print('LOCAL RESPONSE')
    pprint(local_response) # prints the JSON stored locally
    
    # TODO: Eventually iterate through all of the array and change logic below here as well
    localMarketPrice = local_response["results"][0]["marketPrice"] # get the marketPrice of the 0th thing in the array from the file 
    serverMarketPrice = server_response["results"][0]["marketPrice"] # get the marketPrice of the 0th thing in the array from the file

    print('Server Price is {}' .format(serverMarketPrice))
    print('Local Price is {}' .format(localMarketPrice))

    # TODO: Would be cool to listen for lowMarketValue and HighMarketValue too
    # TODO: Print acutal product names and not just the product ID's with productName

    # Get the difference of the two numbers
    difference = abs(localMarketPrice - serverMarketPrice)

    if localMarketPrice > serverMarketPrice:
        message = 'ALERT: Local market price is higher than the server market price by ', difference, ' ! Now might be a good time to sell'
        print (message)
        sendEmail('Local market price is higher than the server market price!', message, email)

        # updateFile = input("Would you like to update the local file from the server now (recommended)? (y/n)")
        # if updateFile == 'y':
        #     writePricesToFile(productID)
        #     writeProductsToFile()

    elif localMarketPrice < serverMarketPrice:
        message = 'ALERT: Local market price is lower than the server market price by ', difference, ' ! Now might be a good time to buy'
        print(message)
        sendEmail('Local market price is lower than the server market price!', message, email)

        # updateFile = input("Would you like to update the local file from the server now (recommended)? (y/n)")
        # if updateFile == 'y':
        #     writePricesToFile(productID)
        #     writeProductsToFile()

    elif localMarketPrice == serverMarketPrice:
        print("Prices are the same.. nothing interesting happening")

def sendEmail(subject, message, email):
    key = 'key-ec1cc22400e9fa7af980b01329d5d1c2' # this should be private somewhere.. 
    sandbox = 'sandboxfe67e9fe7a4742e4ad0f14195632c088.mailgun.org' # this too probably

    # TODO: use newer API
    request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)

    # Send an email 
    request = requests.post(request_url, auth=('api', key), data={
        'from': 'alert@tcgplayer.com',
        'to': email,
        'subject': subject,
        'text': message
    })

def printProductsFromServer():
    """
    Print out the products and product ID's that are currently stored in the API
    """
    server_response = getRequest(getProducts())

    print('SERVER RESPONSE')
    # pprint(server_response) # prints the JSON from the server

    # Print out all the products and corresponding IDs
    for item in server_response["results"]:
        id = item["productId"]
        name = item["productName"]
        print('Product Name' , name , " | Product ID: ", id)

def main():
   
    printProductsFromServer()

    # Enter a card ID to listen for...
    productID = input("What is the card ID you would like to listen for? (currently only supports one ID): ")

    writePricesToFile(productID)
    writeProductsToFile()

    email = input("Great! Now, what is your email we should send price alerts to?" )

    print('Great! Every 5 seconds, we check for updates on the prices. We will let you know when product ID ' , productID, 'changes. ')
    print('Eventually, we will provide you a front-end app.')

    while True:
        print("Checking Prices...")
        checkPrices(productID, email)
        sleep(5)

if __name__ == "__main__":
    main()