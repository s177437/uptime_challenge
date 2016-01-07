import argparse
import couchdb
import textwrap
from argparse import RawDescriptionHelpFormatter
import sys
class AddUsers() : 
	def readFile(self, filename) : 
		return [line.rstrip('\n') for line in open(filename)]

	def createUserObject(self, filename) : 
		users=self.readFile(filename)
		for user in users : 
			attributes={}
			attributes.update({"enabled":"0","Balance":0,"bonus":1, "bonus_time_cutoff":5,"configfile": "transsine.dat", "course":"infrastructure", "file":"index.php","filepath":"/root/uptime_challenge_master/worker/", "group":user, "hourly_rate":3, "ipaddress": "128.39.121.59", "last_check":1452109486.31, "members": ["Ole", "Stine", "Stian"], "offset": 25, "partial_ok_punishment_decrease":0.1, "semester": "A15", "Sentance": "Users:", "teacher": "Kyrre"})
			print attributes
	def modify_key(self, dbservername, dbname, key, value, keytoupdate, valuetoupdate):
        	"""
        	This function updates any given key, value in the database. A unique key, value is passed as arguments to the
        	function. This is necessary to get the correct document back from the database. The document is then
         	updated with a given key, value.
        	:param dbservername:
        	:type dbservername:
        	:param dbname:
        	:type dbname:
        	:param key:
        	:type key:
        	:param value:
        	:type value:
        	:param keytoupdate:
        	:type keytoupdate:
        	:param valuetoupdate:
        	:type valuetoupdate:
        	:return:
        	:rtype:
        	"""
        	couch = couchdb.Server("http://" + dbservername + ":5984/")
        	db = couch[dbname]
        	map_fun = '''function(doc) {
                        if(doc.''' + key + '''=="''' + value + '''"){
                          emit(doc.''' + keytoupdate + ''', doc._id);
                        }
                    }'''
        	result = db.query(map_fun)
        	for element in result:
            		documentid = element["value"]
        	doc = db[documentid]
        	doc[keytoupdate] = valuetoupdate
        	db[documentid] = doc

parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''
EXAMPLE 
------------
python   add_users.py -modifyentry couchdb testaccounts group reportlab Balance 0 

This updates the balance of the user reportlab located in the testaccounts database on
the CouchDB server
------------
'''))
parser.add_argument('-a','--addusers', help='Add users from a list of usernames', required=False)
parser.add_argument('-modifyentry', help='Modify an entry in any database, need to be given in the follwing order: dbserver-hostname dbname searchkey searchvalue keytoupdate valuetoupdate', nargs='+', metavar="parameters", required=False)
parser.add_argument('--stop',  help='Exit program',required=False, action='store_true')
args=parser.parse_args()
run=AddUsers()
if args.addusers:
    print args
    run.createUserObject(args.addusers)
elif args.modifyentry : 
    run.modify_key(args.modifyentry[0], args.modifyentry[1], args.modifyentry[2],args.modifyentry[3],args.modifyentry[4],int(args.modifyentry[5]))
elif args.stop: 
    print "Exiting program"
    sys.exit(0)

