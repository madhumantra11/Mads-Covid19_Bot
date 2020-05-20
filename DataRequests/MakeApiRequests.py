import requests
import json
class Api:
    def __init__(self):
        pass

    def makeApiRequestforCounrty(self, country_name):
        url = "https://covid-193.p.rapidapi.com/statistics"
        querystring = {"country": country_name}
        headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': "15263c1e77msh408ed2560d9f1c9p123c23jsn0fc0b44e64ea"
        }
        response = requests.request( "GET", url, headers=headers, params = querystring )
        js = json.loads( response.text )
        print( "******", js )
        result = js.get( 'response' )[ 0 ]
        print( result.get( 'cases' ) )
        print( "*" * 20 )
        return result.get( 'cases' ), result.get( 'deaths' ), result.get( 'tests' )

    '''def makeApiRequestsgetHistoryData(self, date,country_name):
      url = "https://covid-193.p.rapidapi.com/history"
      querystring = {"day": "date", "country": "country_name"}
      headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': "15263c1e77msh408ed2560d9f1c9p123c23jsn0fc0b44e64ea"
        }
      response = requests.request( "GET", url, headers =headers, params = querystring)
      js = json.loads( response.text )
      print( "******", js )
      result = js.get( 'response' )[ 0 ]
      print( result.get( 'cases' ) )
      print( "*" * 20 )
      return result.get( 'cases' ), result.get( 'deaths' ), result.get( 'tests' )'''

    def makeApiRequestsforIndianStates(self):
        url = "https://covid19-data.p.rapidapi.com/india"
        headers = {
            'x-rapidapi-host': "covid19-data.p.rapidapi.com",
            'x-rapidapi-key': "482a8f8516msh16204eb9d1f4f68p1a9146jsnf33914c7300e"
        }
        response = requests.request( "GET", url, headers=headers )
        js = json.loads( response.text )
        print( "******", js )
        return js

    def makeApiRequestsforWorldwide(self):
        url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
        headers = {
            'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
            'x-rapidapi-key': "15263c1e77msh408ed2560d9f1c9p123c23jsn0fc0b44e64ea"
        }
        response = requests.request( "GET", url, headers=headers )
        js = json.loads( response.text )
        print( "******", js )
        result = js.get('data')
        return result

    def makeApiRequestsgetHelplinenumbers(self):
        url = "https://covid-19-india.p.rapidapi.com/helpline_numbers"
        headers = {
            'x-rapidapi-host': "covid-19-india.p.rapidapi.com",
            'x-rapidapi-key': "15263c1e77msh408ed2560d9f1c9p123c23jsn0fc0b44e64ea"
        }
        response = requests.request( "GET", url, headers=headers )
        js = json.loads( response.text )
        print( "******", js )
        result1 = js.get('contact_details')
        return result1

    def makeApiRequestsgetCovidHeadlines(self):
        url = "https://covid-19-india.p.rapidapi.com/headlines"
        headers = {
            'x-rapidapi-host': "covid-19-india.p.rapidapi.com",
            'x-rapidapi-key': "15263c1e77msh408ed2560d9f1c9p123c23jsn0fc0b44e64ea"
        }
        response = requests.request( "GET", url, headers=headers )
        js = json.loads( response.text )
        print( "******", js )
        result = js.get( 'headlines' )
        return result




                    #print( '**',i )










