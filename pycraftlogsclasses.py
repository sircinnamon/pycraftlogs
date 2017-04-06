class Report:
	def __init__(self, json):
		self.json = json
		self.id = json["id"]
		self.title = json["title"]
		self.owner = json["owner"]
		self.start = json["start"]
		self.end = json["end"]
		self.zone = json["zone"]

class Fight:
	def __init__(self, json, code, friendlies, enemies, friendlyPets, enemyPets, phases):
		self.json = json
		self.code = code
		self.id = json["id"]
		self.start_time = json["start_time"]
		self.end_time = json["end_time"]
		self.boss = json["boss"]
		self.size = json["size"]
		self.difficulty = json["difficulty"]
		self.kill = (json["kill"]=="true")
		self.partial = json["partial"]
		self.bossPercentage = json["bossPercentage"] #WCL api uses camelcase here but underscore for start_time... sometimes
		self.fightPercentage = json["fightPercentage"]
		self.lastPhaseForPercentageDisplay = json["lastPhaseForPercentageDisplay"]
		self.name = json["name"]

		self.friendlies = friendlies
		self.enemies = enemies
		self.friendlyPets = friendlyPets
		self.enemyPets = enemyPets
		self.phases = phases

class FightParticipant:
	def __init__(self, json, code):
		self.json = json
		self.code = code
		self.name = json["name"]
		self.id = json["id"]
		self.guid = json["guid"]
		self.type = json["type"]
		self.fights = FightAttendance(json["fights"])

class FightParticipantPet(FightParticipant):
	def __init__(self, json, code):
		self.json = json
		self.code = code
		self.name = json["name"]
		self.id = json["id"]
		self.guid = json["guid"]
		self.type = json["type"]
		self.fights = FightAttendance(json["fights"])
		self.petOwner = json["petOwner"]

class FightAttendance:
	def __init__(self, json):
		#json is a list of dictionaries, with possible ids, isntances and groups
		self.json = json
		self.attendedFights = []
		for x in json:
			self.attendedFights.append(x["id"])
	def getInstances(self, fightId):
		for x in json:
			if x["id"] == fightId:
				if x.has_key("instances"):
					return x["instances"]
				else:
					return 1
		return 0
	def getGroups(self, fightId):
		for x in json:
			if x["id"] == fightId:
				if x.has_key("groups"):
					return x["groups"]
				else:
					return 1
		return 0
	def attended(self, fightId):
		return (self.attendedFights.count(fightId)>0)