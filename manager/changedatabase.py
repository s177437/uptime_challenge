import couchdb


def modkey(dbname, groupname, value):
    couch = couchdb.Server("http://10.1.0.57:5984/")
    db = couch[dbname]
    map_fun = '''function(doc) {
                        if(doc.group=="''' + groupname + '''"){
                          emit(doc.group, doc._id);
                        }
                    }'''
    result = db.query(map_fun)
    documentid = ""
    for element in result:
        documentid = element["value"]
    doc = db[documentid]
    try:
        oldbalance = doc["Balance"]
        balance = oldbalance + value
        doc["Balance"] = balance
        print balance
    except KeyError:

        print "This user has no previous balance, creating balance"
        doc["Balance"] = value
    db[documentid] = doc




modkey("testaccounts", "group1", 300)
