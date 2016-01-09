import couchdb
import json

def fetchUsersAndBalance():
	couch = couchdb.Server("http://couchdb:5984/")
        db = couch["testaccounts"]
        map_fun = '''
	function(doc) {
  	if (doc.Balance && doc.group) {
    	emit(doc.group, doc.Balance);
 	 }
	}
        '''
        result = db.query(map_fun)
        returnvalues = {}
	for element in result : 
		returnvalues.update({element["key"]:element["value"]})
	sortedlist= sorted(returnvalues.items(), key=lambda x:x[1], reverse=True)
	final={"users":[dict(user=user,balance=balance)for user, balance in sortedlist]}
#	print json.dumps(final)
	return final
	
fetchUsersAndBalance()
