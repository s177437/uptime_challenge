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
    print result
