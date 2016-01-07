class AddUsers() : 
	def readFile(self, filename) : 
		return [line.rstrip('\n') for line in open(filename)]

	def createUserObject(self) : 
		users=self.readFile("users")
		for user in users : 
			attributes={}
			attributes.update({"enabled":"0","Balance":0,"bonus":1, "bonus_time_cutoff":5,"configfile": "transsine.dat", "course":"infrastructure", "file":"index.php","filepath":"/root/uptime_challenge_master/worker/", "group":user, "hourly_rate":3, "ipaddress": "128.39.121.59", "last_check":1452109486.31, "members": ["Ole", "Stine", "Stian"], "offset": 25, "partial_ok_punishment_decrease":0.1, "semester": "A15", "Sentance": "Users:", "teacher": "Kyrre"})
			print attributes

a = AddUsers()
a.createUserObject()
