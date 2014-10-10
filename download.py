#!/usr/bin/python
from pyGTrends import pyGTrends
import csv, datetime, time, getpass, sys
import re
import json
from pprint import pprint

# google_username = raw_input("Google username: ")
# google_password = getpass.getpass("Google password: ")

google_username = "eigenboy"
google_password = "quark123"

def getcountry():
    countries = []
    with open("countries.json") as f:
        contents = f.read().strip()
        data = json.loads(contents)
        for x in data["children"]:
            countries.append(x["id"])

    return countries


def read_csv_data( data ):
    """
        Reads CSV from given path and Return list of dict with Mapping
    """
    csv_reader = csv.reader( data )
    # Read the column names from the first line of the file
    fields = csv_reader.next()
    data_lines = []
    for row in csv_reader:
        items = dict(zip(fields, row))
        data_lines.append(items)
    return data_lines

def progressbar(it, prefix = "", size = 60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()
    
    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()

def getGTData( search_query , date, geo, cmpt, cid  , export, reqId ) :
    
    #output file name
    fnametag = "data/" + search_query + "_" + geo + "_suburban"
    if cid == "GEO_MAP_ANIMATION_0_2":
        fnametag= search_query + "_metro"

    q = search_query

    print "search_query  ",search_query
    print "date          ",date
    print "geo           ",geo
    print "q             ",q
    print "cmpt          ",cmpt
    print "cid           ",cid
    print "export        ",export
    print "reqId         ",reqId
    
    connector = pyGTrends( google_username, google_password )
    connector.download_report( ( search_query ) 
			   , date = date
                           , geo = geo
                           ,q = q, cmpt = cmpt, cid = cid, export = export, reqId = reqId 
    )
    rsp=connector.getData()
    print rsp
    #extract the json
    regex= 'animationResponse\((.+?)\);'
    pattern=re.compile(regex)
    json_rsp=re.findall(pattern,rsp)
    for j in json_rsp:
        json_rsp1 = j

        #print json_rsp1, "xxx\n"
        rsp = json.loads(json_rsp1)
        
        print rsp['data'][0], "xxx\n"
        print "first: ", rsp['data'][0]["frameData"], "xxx\n"
        print "second: ", rsp["data"][0]["timeStr"], "xxx\n"
        
        with open( fnametag + '_google_report.csv', 'w') as csv_out:
            csv_writer = csv.writer( csv_out )
            print len(rsp['data'])
            #outer loop
            
            for index in range(len(rsp['data'])):
                print rsp['data'][index]
                col4=rsp["data"][index]["timeStr"]
                
                for innerindex in range(len(rsp['data'][index]['frameData'])):

                    col1=rsp['data'][index]['frameData'][innerindex][0]
                    col2=rsp['data'][index]['frameData'][innerindex][1]
                    col3=rsp['data'][index]['frameData'][innerindex][2]
                    
                    #print col1,col2,col3,col4
                    csv_writer.writerow( [ col1 ] + [ col2 ]  + [ col3 ] + [ col4 ])

    print "File saved: %s " % ( fnametag + '_google_report.csv' )

def getGoogleTrendData( search_queries , date, geo , cmpt, cid,  export, reqId ) :

    for search_term in progressbar( search_queries, "Downloading: ", 40 ):
        for geo in progressbar( countries, "Downloading: ", 40 ):
            getGTData(search_query = search_term, date = date, geo = geo, cmpt = 'q', cid  = cid,  export = export, reqId =reqId )
	#time.sleep(2)  # Delay for x seconds    
    return True


if __name__=="__main__":

    list_of_queries = ["google+maps"]
    
    search_queries = list_of_queries
    # countries = getcountry()
    countries = ["IN", "US", "DE"]

    date="all"
    # geo=countries[2]
    cmpt = 'q'
    cid  = "GEO_MAP_ANIMATION_0_1"
    export = "6"
    reqId ='0'  


    
    #choice for metro
    # is_metro = raw_input("Metro(y/n): ")
    # if is_metro == 'y':
    #    cid = "GEO_MAP_ANIMATION_0_2"
    #    reqId = '1'
    
    # Remove duplicate entries in the list if there are any...
    list_of_queries = list( set( list_of_queries ) )
    if getGoogleTrendData( search_queries , date, geo, cmpt, cid , export , reqId  ) :
        print "Google Trend Data aquired."
        
