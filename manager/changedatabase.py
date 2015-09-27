import couchdb


def modkey(dbname, groupname, key, value):
    couch = couchdb.Server("http://10.1.0.57:5984/")
    db = couch[dbname]
    map_fun = '''function(doc) {
                        if(doc.group=="''' + groupname + '''"){
                          emit(doc.group, doc._id);
                        }
                    }'''
    result=db.query(map_fun)
    documentid=""
    for element in result : 
	documentid=element["value"]
    print documentid
    doc=db[documentid]
    doc["Balance"]=222
    db[documentid]=doc
modkey("testaccounts","group1", "","")
