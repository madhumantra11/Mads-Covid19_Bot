import json
import os
from flask import Flask, request, make_response
from flask_cors import cross_origin
from bs4 import BeautifulSoup
from logger import logger
from DataRequests import MakeApiRequests
from SendEmail import sendEmail
from email_templates import templatereader
from SendEmail.sendEmail import EmailSender

app = Flask(__name__)

# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    #print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeApiRequest(query):
    api = MakeApiRequests.Api()
    if query =="world":
        return api.makeApiRequestsforWorldwide()
    if query == "headlines":
        return api.makeApiRequestsgetCovidHeadlines()
    if query =="state":
        return api.makeApiRequestsforIndianStates()
    if query == "helpline_numbers":
        return api.makeApiRequestsgetHelplinenumbers()
    else:
        return api.makeApiRequestforCounrty(query)

# processing the request from dialogflow
def processRequest(req):
    global webhookresponse
    log = logger.Log()
    sessionID = req.get( 'responseId' )
    result = req.get("queryResult")
    user_says=result.get("queryText")
    ##log.write_log(sessionID, "User Says: "+user_says,webhookresponse,intent)
    parameters = result.get("parameters")
    cust_name=parameters.get("cust_name")
    #print(cust_name)
    cust_contact = parameters.get("cust_contact")
    cust_email=parameters.get("cust_email")
    course_name=parameters.get("course_name")
    intent = result.get("intent").get('displayName')

    if (intent=='country_selection'):
        cust_country = parameters.get("cust-country")
        fulfillmentText, deaths_data, testsdone_data = makeApiRequest( cust_country )
        webhookresponse = "***Covid Report*** \n\n" +\
                           " New cases :" + str( fulfillmentText.get( 'new' ) ) + \
                           "\n" + " Active cases : " + str(
            fulfillmentText.get( 'active' ) ) + "\n" + " Critical cases : " + str( fulfillmentText.get( 'critical' ) ) + \
                          "\n" + " Recovered cases : " + str(
            fulfillmentText.get( 'recovered' ) ) + "\n" + " Total cases : " + str( fulfillmentText.get( 'total' ) ) + \
                          "\n" + " New Deaths : " + str( deaths_data.get( 'new' ) ) + "\n" + " Total Deaths : " + str(
            deaths_data.get( 'total' ) ) + \
                          "\n" + " Total Test Done : " + str(
            testsdone_data.get( 'total' ) ) + "\n\n*******END********* \n "
        print( "Country Name :", cust_country )
        print( webhookresponse )
        ##email_sender = EmailSender()
        ##template = templatereader.TemplateReader()
        ##email_message = cust_country + webhookresponse + template.read_course_template()
        ##email_sender.sendEmail( cust_email, email_message )
        ##fulfillmentText = "We have sent the Covid19 related information on your email address.Thanks for getting in touch with us."
        log.write_log(sessionID, "Current Cases", webhookresponse, intent)
        return {
            "fulfillmentTextMessages":[
                {
                    "text":{
                        "text":[
                            cust_country
                            ]
        }
        },
        {
                    "text":{
                        "text":[
                            webhookresponse
                            ]
        }
        },
        {
            "text":{
                "text":[
                    "Do you want me to share COVID-19 related information on your email id? Please chose from the below \n 1. Sure! \n 2. No. Thanks!"
                    ]
            }
        }
        ]
        }
    elif intent == "Welcome" or intent == "continue_conversation" or intent == "not_send_email" or intent == "endConversation" \
                    or intent == "Fallback" or intent == "FAQ" :
        fulfillmentText = result.get( "fulfillmentText" )
        log.write_log(sessionID, user_says, fulfillmentText, intent)

    elif intent == "Send_Email":
        fulfillmentText = result.get( "fulfillmentText" )
        log.write_log( sessionID, "Sure send email", fulfillmentText, intent)
        email_sender = EmailSender()
        template = templatereader.TemplateReader()
        email_message = template.read_course_template()
        email_sender.sendEmail( cust_email, email_message )
        fulfillmentText = "We have sent the Covid19 related information on your email address.Thanks for getting in touch with us."
        log.write_log(sessionID, "Sure send email", fulfillmentText, intent)
        return {
                 "fulfillmentText" : fulfillmentText
        }
    elif intent == "worldwide_data":
        fulfillmentText = makeApiRequest("world")
        webhookresponse = "***Worldwide Cases Report*** \n\n" + " Recovered :" + str( fulfillmentText.__getitem__( 'recovered' ) ) + \
                           "\n" + " Deaths : " + str(fulfillmentText.__getitem__( 'deaths' ) ) + "\n" + " Confirmed cases : " + str( fulfillmentText.__getitem__( 'confirmed' ) ) + \
                          "\n" + "Last Checked :" + str(fulfillmentText.__getitem__('lastChecked') ) + "\n" + "Last Reported :" + str( fulfillmentText.__getitem__( 'lastReported' ) ) + \
                          "\n\n*******END********* \n "
        print(webhookresponse)
        log.write_log(sessionID, "Worldwide Cases", webhookresponse, intent)
        return {

            "fulfillmentTextMessages":[
                {
                    "text":{
                        "text":[
                            webhookresponse
                            ]
        }
        },
        {
            "text":{
                "text":[
                    "Do you want me to share COVID-19 related information on your email id? Please chose from the below \n 1. Sure! \n 2. No. Thanks!"
                    ]
            }
        }
        ]
        }
    elif intent == "COVID_Headlines":
        fulfillmentText = makeApiRequest("headlines")
        ##webhookresponse=fulfillmentText
        ##webhookresponse = "***COVID Headlines*** \n\n" + str(webhookresponse) +\
          ##                "\n\n*******END*******\n"
        for webhookresponse in fulfillmentText:
            print("**", webhookresponse)

        log.write_log( sessionID, "COVID Headlines", webhookresponse, intent )
        return {
            "fulfillmentTextMessages": [
                {
                    "text": {
                        "text": [
                            webhookresponse
                        ]
                     }
                },
                {
                    "text": {
                        "text": [
                            "Do you want me to share COVID-19 related information on your email id? Please chose from the below \n 1. Sure! \n 2. No. Thanks!"
                        ]
                    }
                }
            ]
        }
    elif intent == "indian_states":
        fulfillmentText = makeApiRequest( "state" )
        print( len( fulfillmentText ) )

        webhookresponse1 = ''
        webhookresponse2 = ''
        webhookresponse3 = ''
        for i in range(0, 11):
            webhookresponse = fulfillmentText[i]
            webhookresponse1 += "*********\n" + " State :" + str( webhookresponse['state']) + \
                                 "\n" + " Confirmed cases : " + str(webhookresponse[ 'confirmed' ] ) + "\n" + " Death cases : " + str( webhookresponse[ 'deaths' ] ) + \
                                "\n" + " Active cases : " + str(webhookresponse[ 'active' ] ) + "\n" + " Recovered cases : " + str(webhookresponse[ 'recovered' ] ) +\
                                "\n***********"
        for i in range(11, 21):
            webhookresponse = fulfillmentText[i]
            webhookresponse2 += "*********\n" + " State :" + str( webhookresponse[ 'state' ] ) + \
                                "\n" + " Confirmed cases : " + str(webhookresponse[ 'confirmed' ] ) + "\n" + " Death cases : " + str( webhookresponse[ 'deaths' ] ) + \
                                "\n" + " Active cases : " + str(webhookresponse[ 'active' ] ) + "\n" + " Recovered cases : " + str(webhookresponse[ 'recovered' ] ) +\
                                 "\n***********"
        for i in range(21, 38):
            webhookresponse = fulfillmentText[i]
            webhookresponse3 += "*********\n" + " State :" + str( webhookresponse[ 'state' ] ) + \
                                "\n" + " Confirmed cases : " + str(webhookresponse[ 'confirmed' ] ) + "\n" + " Death cases : " + str( webhookresponse[ 'deaths' ] ) + \
                                "\n" + " Active cases : " + str(webhookresponse[ 'active' ] ) + "\n" + " Recovered cases : " + str(webhookresponse[ 'recovered' ] ) +\
                                "\n**************"
        print( "***Statewise Cases*** \n\n" + webhookresponse1 + "\n\n" )
        print( "***Statewise Cases*** \n\n" + webhookresponse2 + "\n\n" )
        print( "***Statewise Cases*** \n\n" + webhookresponse3 + "\n\n*******END********* \n" )
        log.write_log( sessionID, "Indian State Cases", webhookresponse1, intent)
        return {
         "fulfillmentTextMessages":[
                {
                    "text":{
                        "text":[
                            webhookresponse1
                            ]
        }
        },
        {
            "text": {
                "text" :[
                    webhookresponse2
                    ]
            }
        },
             {
                 "text" :{
                     "text":[
                         webhookresponse3
                         ]
                 }
             },
             {
            "text":{
                "text":[
                    "Do you want me to share COVID-19 related information on your email id? Please chose from the below \n 1. Sure! \n 2. No. Thanks!"
                    ]
            }
        }
        ]
        }
    elif intent == "helpline_numbers":
        fulfillmentText = makeApiRequest( "helpline_numbers" )
        for webhookresponse in fulfillmentText:
            print( webhookresponse )
        log.write_log( sessionID, "HelplineNumbers", webhookresponse, intent )
        return {
            "fulfillmentTextMessages": [
                {
                    "text": {
                        "text": [
                            webhookresponse
                        ]
                    }
                },
                {
                    "text": {
                        "text": [
                            "Please find the Helpline Numbers. Do you want me to share COVID-19 related information on your email id? Please chose from the below \n 1. Sure! \n 2. No. Thanks!"
                        ]
                    }
                }
            ]
        }
    else:
        return {
            "fulfillmentText" : "Something went wrong, Let's start from beginning. Say Hi",
        }

if __name__ == '__main__':
 port = int(os.getenv('PORT',5000))
 print("Starting app on port %d" % port)
 app.run(debug=False, port=port, host='0.0.0.0')

##if __name__ == "__main__":
    ##app.run(port=5000, debug=True)# running the app on the local machine on port 5000



