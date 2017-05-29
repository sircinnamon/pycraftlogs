class Report(object):
    """Represents a report uploaded to WCL."""
    def __init__(self, json):
        self.json = json
        self.id = json["id"]
        self.title = json["title"]
        self.owner = json["owner"]
        self.start = json["start"]
        self.end = json["end"]
        self.zone = json["zone"]

class Fight(object):
    """Represents a logged fight."""
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
    """Represents a logged trash fight."""
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
    """Represents an entity which participated in fight events."""
    def __init__(self, json, code):
        self.json = json
        self.code = code
        self.name = json["name"]
        self.id = json["id"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.fights = FightAttendance(json["fights"])

class FightParticipantPet(FightParticipant):
    """Represents an pet entity which participated in fight events."""
    def __init__(self, json, code):
        super(FightParticipantPet,self).__init__(json, code)
        self.petOwner = json["petOwner"]

class FightAttendance(object):
    """Represents an attendance list for fights a single player participated in."""
    def __init__(self, json):
        #json is a list of dictionaries, with possible ids, isntances and groups
        self.json = json
        self.attendedFights = []
        for x in json:
            self.attendedFights.append(x["id"])
    def get_instances(self, fightId):
        """Retrieve how many instances of the parent were present in the fight specified."""
        for x in json:
            if x["id"] == fightId:
                if "instances" in x:
                    return x["instances"]
                else:
                    return 1
        return 0
    def get_groups(self, fightId):
        """Retrieve how many groups of the parent were present in the fight specified."""
        #Not actually sure what this means.
        for x in json:
            if x["id"] == fightId:
                if "groups" in x:
                    return x["groups"]
                else:
                    return 1
        return 0
    def attended(self, fightId):
        """Return true if parent was present for at least one attempt of given fight."""
        return (self.attendedFights.count(fightId)>0)

#Table views: "damage-done", "damage-taken", "healing", 
#"casts", "summons", "buffs", "debuffs", "deaths", 
#"survivability", "resources", "resource-gains"

class TableEntry(object):
    """Represents an entity's information on a standard data table."""
    #Superclass for standard table entries
    #damage-done, damage-taken, healing, casts, summons, deaths
    def __init__(self, json, code, totalTime):
        self.json = json
        self.code = code
        self.name = json["name"]
        self.id = json["id"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.itemLevel = json["itemLevel"] if "itemLevel" in json else None #Hati screws this up too
        self.icon = json["icon"]
        self.gear = list(map(Gear, json["gear"])) if "gear" in json else None #Hati comes up as a non pet but has no gear or talents
        self.talents = list(map(Talent, json["talents"])) if "talents" in json else None # ...relatable
        self.totalTime = totalTime

class DamageDoneTableEntry(TableEntry):
    """Represents an entity's information on a damage-done data table."""
    def __init__(self, json, code, totalTime):
        super(DamageDoneTableEntry,self).__init__(json, code, totalTime)
        self.total = json["total"]
        self.totalReduced = json["totalReduced"] if "totalReduced" in json else 0
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if "activeTimeReduced" in json else 0
        self.abilities = list(map(Ability,json["abilities"]))
        #exclude? May always be empty on this table
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.targets = list(map(BasicEntity,json["targets"]))
        self.pets = list(map(DamageDoneTableEntryPet, json["pets"])) if "pets" in json else None

class DamageTakenTableEntry(TableEntry):
    """Represents an entity's information on a damage-taken data table."""
    def __init__(self, json, code, totalTime):
        super(DamageTakenTableEntry,self).__init__(json, code, totalTime)
        self.total = json["total"]
        self.totalReduced = json["totalReduced"] if "totalReduced" in json else 0
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if "activeTimeReduced" in json else 0
        self.abilities = list(map(DamageTakenAbility,json["abilities"]))
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.sources = list(map(DamageTakenSource,json["sources"]))

class HealingTableEntry(TableEntry):
    """Represents an entity's information on a healing data table."""
    def __init__(self, json, code, totalTime):
        super(HealingTableEntry,self).__init__(json, code, totalTime)
        self.total = json["total"]
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if "activeTimeReduced" in json else 0
        self.overheal = json["overheal"]
        self.abilities = list(map(DamageTakenAbility,json["abilities"]))
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.targets = list(map(BasicEntity,json["targets"]))

class CastsTableEntry(TableEntry):
    """Represents an entity's information on a casts data table."""
    def __init__(self, json, code, totalTime):
        super(CastsTableEntry,self).__init__(json, code, totalTime)
        self.total = json["total"]
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if "activeTimeReduced" in json else 0
        self.abilities = list(map(DamageTakenAbility,json["abilities"]))
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.targets = list(map(BasicEntity,json["targets"]))

class SummonsTableEntry(TableEntry):
    """Represents an entity's information on a summons data table."""
    def __init__(self, json, code, totalTime):
        super(SummonsTableEntry,self).__init__(json, code, totalTime)
        self.total = json["total"]
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if "activeTimeReduced" in json else 0
        self.abilities = list(map(DamageTakenAbility,json["abilities"]))
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.targets = list(map(BasicEntity,json["targets"]))

class DeathsTableEntry(object):
    """Represents an entity's information on a deaths data table."""
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
        self.killingBlow = DeathKillingBlow(json["killingBlow"]) if "killingBlow" in json else None

class AuraTableEntry(object):
    """Represents an entity's information on a aura data table."""
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
    """Represents a single piece of equipment."""
    def __init__(self, json):
        self.json = json
        self.id = json["id"]
        self.slot = json["slot"]
        self.itemLevel = json["itemLevel"]
        self.quality = json["quality"]
        self.icon = json["icon"]
        self.name = json["name"] if "name" in json else None
        self.gems = list(map(Gem, json["gems"])) if "gems" in json else None
        self.bonusIDs = json["bonusIDs"] if "bonusIDs" in json else None
        self.permanentEnchant = json["permanentEnchant"] if "permanentEnchant" in json else None
        self.permanentEnchantName = json["permanentEnchantName"] if "permanentEnchantName" in json else None

class Gem(object):
    """Represents a socketed gem on a piece of equipment."""
    def __init__(self, json):
        self.json = json
        self.id = json["id"]
        self.itemLevel = json["itemLevel"]
        self.icon = json["icon"]

class Talent(object):
    """Represents a players current selected talent."""
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.abilityIcon = json["abilityIcon"]

class Ability(object):
    """Parent class representing an ability."""
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.total = json["total"]
        self.type = json["type"]

class DamageTakenAbility(Ability):
    """Extended ability for field on damage taken table"""
    def __init__(self, json):
        super(DamageTakenAbility,self).__init__(json)
        self.totalReduced = json["totalReduced"]if "totalReduced" in json else 0

class BasicEntity(object):
    """Parent class for an entity in a fight on a table."""
    #Applies as Target for DamageDone and Healing tables
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.total = json["total"]
        self.type = json["type"]

class DamageTakenSource(BasicEntity):
    """SubClass for a source of damage taken on damage taken table."""
    def __init__(self, json):
        super(DamageTakenSource,self).__init__(json)
        self.totalReduced = json["totalReduced"] if "totalReduced" in json else 0

class Pet(object):
    """Parent class for a pet attached to a players table entry."""
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.id = json["id"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.icon = json["icon"]
        self.total = json["total"]

class DamageDoneTableEntryPet(Pet):
    """Extended Pet for damage-done view fields."""
    def __init__(self, json):
        super(DamageDoneTableEntryPet,self).__init__(json)
        self.totalReduced = json["totalReduced"]
        self.activeTime = json["activeTime"]

class DeathHistory(object):
    """Represents the abilities targeted by preceeding death."""
    def __init__(self, json):
        self.json = json
        self.total = json["total"]
        self.activeTime = json["activeTime"]
        self.activeTimeReduced = json["activeTimeReduced"] if "activeTimeReduced" in json else 0
        self.abilities = list(map(Ability,json["abilities"]))
        self.damageAbilities = list(map(Ability,json["damageAbilities"]))
        self.sources = list(map(BasicEntity,json["sources"]))

class Event(object):
    """Represents one event in a log. May be an ability cast, auto-attack, etc."""
    def __init__(self, json):
        self.json = json
        self.timestamp = json["timestamp"]
        self.type = json["type"]
        self.sourceID = json["sourceID"] if "sourceID" in json else -1
        self.source = EventSource(json["source"]) if "source" in json else None
        self.sourceIsFriendly = json["sourceIsFriendly"]
        self.targetID = json["targetID"]
        self.targetIsFriendly = json["targetIsFriendly"]
        self.ability = DeathKillingBlow(json["ability"])
        self.hitType = json["hitType"]
        self.amount = json["amount"]
        self.overkill = json["overkill"] if "overkill" in json else 0
        self.absorbed = json["absorbed"]
        self.tick = json["tick"] if "tick" in json else False

class DeathKillingBlow(object):
    """Represents the ability or event which cause death."""
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.abilityIcon = json["abilityIcon"]

class EventSource(object):
    """Represents a source of event that has no relational ID."""
    def __init__(self, json):
        self.json = json
        self.name = json["name"]
        self.id = json["id"]
        self.guid = json["guid"]
        self.type = json["type"]
        self.icon = json["icon"]

class AuraBand(object):
    """represents a band of time at which an aura was active"""
    def __init__(self, json):
        self.startTime = json["startTime"]
        self.endTime = json["endTime"]

class Zone(object):
    """Represents one zone on the zone list of the API."""
    def __init__(self, json):
        self.id = json["id"]
        self.name = json["name"]
        self.frozen = json["frozen"] if "frozen" in json else False
        self.encounters = list(map(Encounter, json["encounters"])) if "encounters" in json else None
        self.brackets = list(map(Bracket, json["brackets"])) if "brackets" in json else None

class Encounter(object):
    """Represents a single possible encounter in a raid."""
    def __init__(self, json):
        self.id = json["id"]
        self.name = json["name"]

class Bracket(object):
    """Represents a single bracket of a raid. (Usually an ilvl range.)"""
    def __init__(self, json):
        self.id = json["id"]
        self.name = json["name"]

class _Class(object):
    """Represents a single playable character class"""
    def __init__(self, json):
        self.id = json["id"]
        self.name = json["name"]
        self.specs = list(map(Spec, json["specs"])) if "specs" in json else None

class Spec(object):
    """Represents a single class specialization."""
    def __init__(self, json):
        self.id = json["id"]
        self.name = json["name"]
