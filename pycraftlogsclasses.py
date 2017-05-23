class Report(object):
    def __init__(self, json):
        self.json = json
        self.id = json["id"]
        self.title = json["title"]
        self.owner = json["owner"]
        self.start = json["start"]
        self.end = json["end"]
        self.zone = json["zone"]

class Fight(object):
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

class TrashFight(object):
    def __init__(self, json, code, friendlies, enemies, friendlyPets, enemyPets, phases):
        self.json = json
        self.code = code
        self.id = json["id"]
        self.start_time = json["start_time"]
        self.end_time = json["end_time"]
        self.boss = json["boss"]
        self.name = json["name"]

        self.friendlies = friendlies
        self.enemies = enemies
        self.friendlyPets = friendlyPets
        self.enemyPets = enemyPets
        self.phases = phases

class FightParticipant(object):
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
        super(FightParticipantPet,self).__init__(json, code)
        self.petOwner = json["petOwner"]

class FightAttendance(object):
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

#Table views: "damage-done", "damage-taken", "healing", 
#"casts", "summons", "buffs", "debuffs", "deaths", 
#"survivability", "resources", "resource-gains"

class TableEntry(object):
    #Superclass for standard table entries
    #damage-done, damage-taken, healing, casts, summons, deaths
    def __init__(self, json, code, totalTime):
        self.json = json
        self.code = code
        self.name = json["name"]
        self.id = json["id"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.itemLevel = json["itemLevel"] if json.has_key("itemLevel") else None #Hati screws this up too
        self.icon = json["icon"]
        self.gear = list(map(Gear, json["gear"])) if json.has_key("gear") else None #Hati comes up as a non pet but has no gear or talents
        self.talents = list(map(Talent, json["talents"])) if json.has_key("talents") else None # ...relatable
        self.totalTime = totalTime

class DamageDoneTableEntry(TableEntry):
    #Represents one entry on a damage-done table
    def __init__(self, json, code, totalTime):
        super(DamageDoneTableEntry,self).__init__(json, code, totalTime)
        self.total = json["total"]
        self.totalReduced = json["totalReduced"] if json.has_key("totalReduced") else 0
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if json.has_key("activeTimeReduced") else 0
        self.abilities = list(map(Ability,json["abilities"]))
        #exclude? May always be empty on this table
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.targets = list(map(BasicEntity,json["targets"]))
        self.pets = list(map(DamageDoneTableEntryPet, json["pets"])) if json.has_key("pets") else None

class DamageTakenTableEntry(TableEntry):
    #Represents one entry on a damage-taken table
    def __init__(self, json, code, totalTime):
        super(DamageTakenTableEntry,self).__init__(json, code, totalTime)
        self.total = json["total"]
        self.totalReduced = json["totalReduced"] if json.has_key("totalReduced") else 0
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if json.has_key("activeTimeReduced") else 0
        self.abilities = list(map(DamageTakenAbility,json["abilities"]))
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.sources = list(map(DamageTakenSource,json["sources"]))

class HealingTableEntry(TableEntry):
    #Represents one entry on a healing table
    def __init__(self, json, code, totalTime):
        super(HealingTableEntry,self).__init__(json, code, totalTime)
        self.total = json["total"]
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if json.has_key("activeTimeReduced") else 0
        self.overheal = json["overheal"]
        self.abilities = list(map(DamageTakenAbility,json["abilities"]))
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.targets = list(map(BasicEntity,json["targets"]))

class CastsTableEntry(TableEntry):
    #Represents one entry on a Casts table
    def __init__(self, json, code, totalTime):
        super(CastsTableEntry,self).__init__(json, code, totalTime)
        self.total = json["total"]
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if json.has_key("activeTimeReduced") else 0
        self.abilities = list(map(DamageTakenAbility,json["abilities"]))
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.targets = list(map(BasicEntity,json["targets"]))

class SummonsTableEntry(TableEntry):
    #Represents one entry on a Summons table
    def __init__(self, json, code, totalTime):
        super(SummonsTableEntry,self).__init__(json, code, totalTime)
        self.total = json["total"]
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if json.has_key("activeTimeReduced") else 0
        self.abilities = list(map(DamageTakenAbility,json["abilities"]))
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.targets = list(map(BasicEntity,json["targets"]))

class DeathsTableEntry(object):
    #Nonstandard table entry
    def __init__(self, json, code):
        self.json = json
        self.code = code
        self.name = json["name"]
        self.id = json["id"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.icon = json["icon"]
        self.timestamp = json["timestamp"]
        self.damage = DeathHistory(json["damage"])
        self.healing = DeathHistory(json["healing"])
        self.fight = json["fight"]
        self.deathWindow = json["deathWindow"]
        self.overkill = json["overkill"]
        self.events = list(map(Event,json["events"]))
        self.killingBlow = DeathKillingBlow(json["killingBlow"]) if json.has_key("killingBlow") else None

class AuraTableEntry(object):
    #represents an entry on buffs/debuffs table
    def __init__(self, json, code, useTargets, totalTime, startTime, endTime):
        self.json = json
        self.code = code
        self.name = json["name"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.abilityIcon = json["abilityIcon"]
        self.totalUptime = json["totalUptime"]
        self.totalUses = json["totalUses"]
        self.bands = list(map(AuraBand,json["bands"]))
        self.scanUseTargets = useTargets
        self.scanTotalTime = totalTime
        self.scanStartTime = startTime #start time of scan, not buff
        self.scanEndTime = endTime #end time of scan, not buff


class Gear(object):
    #Represents an equipped piece of gear
    def __init__(self, json):
        self.json = json
        self.id = json["id"]
        self.slot = json["slot"]
        self.itemLevel = json["itemLevel"]
        self.quality = json["quality"]
        self.icon = json["icon"]
        self.name = json["name"] if json.has_key("name") else None
        self.gems = list(map(Gem, json["gems"])) if json.has_key("gems") else None
        self.bonusIDs = json["bonusIDs"] if json.has_key("bonusIDs") else None
        self.permanentEnchant = json["permanentEnchant"] if json.has_key("permanentEnchant") else None
        self.permanentEnchantName = json["permanentEnchantName"] if json.has_key("permanentEnchantName") else None

class Gem(object):
    #represents a socketed gem
    def __init__(self, json):
        self.json = json
        self.id = json["id"]
        self.itemLevel = json["itemLevel"]
        self.icon = json["icon"]

class Talent(object):
    #represents a selected talent
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.abilityIcon = json["abilityIcon"]

class Ability(object):
    #Parent class for an ability
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.total = json["total"]
        self.type = json["type"]

class DamageTakenAbility(Ability):
    #Extended ability for fields on damage taken table
    def __init__(self, json):
        super(DamageTakenAbility,self).__init__(json)
        self.totalReduced = json["totalReduced"]if json.has_key("totalReduced") else 0

class BasicEntity(object):
    #Parent class for an entity in a fight on a table
    #Applies as Target for DamageDone and Healing tables
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.total = json["total"]
        self.type = json["type"]

class DamageTakenSource(BasicEntity):
    #SubClass for a source of damage taken on damage taken table
    def __init__(self, json):
        super(DamageTakenSource,self).__init__(json)
        self.totalReduced = json["totalReduced"] if json.has_key("totalReduced") else 0

class Pet(object):
    #parent class for a pet attached to a layers table entry
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.id = json["id"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.icon = json["icon"]
        self.total = json["total"]

class DamageDoneTableEntryPet(Pet):
    #Extended for extra damage-done view
    def __init__(self, json):
        super(DamageDoneTableEntryPet,self).__init__(json)
        self.totalReduced = json["totalReduced"]
        self.activeTime = json["activeTime"]

class DeathHistory(object):
    #Stores the pre death damage or healing
    def __init__(self, json):
        self.json = json
        self.total = json["total"]
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if json.has_key("activeTimeReduced") else 0
        self.abilities = list(map(Ability,json["abilities"]))
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.sources = list(map(BasicEntity,json["sources"]))

class Event(object):
    #Stores the pre death damage or healing
    def __init__(self, json):
        self.json = json
        self.timestamp = json["timestamp"]
        self.type = json["type"]
        self.sourceID = json["sourceID"] if json.has_key("sourceID") else -1
        self.source = EventSource(json["source"]) if json.has_key("source") else None
        self.sourceIsFriendly = json["sourceIsFriendly"]
        self.targetID = json["targetID"]
        self.targetIsFriendly = json["targetIsFriendly"]
        self.ability = DeathKillingBlow(json["ability"])
        self.hitType = json["hitType"]
        self.amount = json["amount"]
        self.overkill = json["overkill"] if json.has_key("overkill") else 0
        self.absorbed = json["absorbed"]
        self.tick = json["tick"] if json.has_key("tick") else False

class DeathKillingBlow(object):
    #represents an ability generally
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.abilityIcon = json["abilityIcon"]

class EventSource(object):
    #represents a source of death that has no ID
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.id = json["id"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.icon = json["icon"]

class AuraBand(object):
	#represents a band of time at which an aura was active
	def __init__(self, json):
		self.startTime = json["startTime"]
		self.endTime = json["endTime"]

class Zone(object):
	#represents zone on the zone list
	def __init__(self, json):
		self.id = json["id"]
		self.name = json["name"]
		self.frozen = json["frozen"] if json.has_key("frozen") else False
		self.encounters = list(map(Encounter, json["encounters"])) if json.has_key("encounters") else None
		self.brackets = list(map(Bracket, json["brackets"])) if json.has_key("brackets") else None

class Encounter(object):
	#represents a single possible encounter in a raid
	def __init__(self, json):
		self.id = json["id"]
		self.name = json["name"]

class Bracket(object):
	#represents a single bracket in a raid
	def __init__(self, json):
		self.id = json["id"]
		self.name = json["name"]

class _Class(object):
	#represents a single playable character class
	def __init__(self, json):
		self.id = json["id"]
		self.name = json["name"]
		self.specs = list(map(Spec, json["specs"])) if json.has_key("specs") else None


class Spec(object):
	#represents a single class specialization
	def __init__(self, json):
		self.id = json["id"]
		self.name = json["name"]