"""pycraftlogs is an API wrapper for the WarcraftLogs API.

The WarcraftLogs API is still under construction but in its current state it
can do many useful things. This wrapper allows simpler interactions with the
API to occur within any python program.
"""
import requests
import sys
from pycraftlogsclasses import *

key = "yourAPIkey"

def wow_zones():
    """Request a listing of zones and return a list of Zone objects."""
    response = requests.get(
    "https://www.warcraftlogs.com:443/v1/zones?api_key=" + key)
    json_data = response.json()
    zones = list()
    for entry in json_data:
        zones.append(Zone(entry))
    return zones

def wow_classes():
    """Request a listing of playable classes and return a list of _Class objects."""
    response = requests.get(
    "https://www.warcraftlogs.com:443/v1/classes?api_key=" + key)
    json_data = response.json()
    classes = list()
    for entry in json_data:
        classes.append(Zone(entry))
    return classes
    return json_data

def wow_rankings_encounter(encounter_id, metric=None, size=None, 
                           difficulty=None, partition=None, 
                           class_id=None, spec=None, bracket=None, 
                           limit=None, guild=None, server=None, 
                           region=None, page=None, filter_str=None):
    """Request a set of matching rankings for a specific encounter. NOTE: Currently not stored in a class

    Keyword arguments:
    metric -- What metric to rank by. e.g. dps, hps etc.
    size -- Only valid in non-flex raids, must be omitted otherwise. Limit results to this exact size.
    difficulty -- Difficulty setting to query e.g. LFR to Mythic.
    partition -- What partition to query, if multiple exist.
    class_id -- Limit results to members of a certain class.
    spec -- Limit results to members of a certain spec (class must also be specified).
    bracket -- Bracket to query. See /zones response for info.
    limit -- Number of results to achieve. Default 200, max 5000.
    guild -- Limit results to given guild.
    server -- Specify which server to query. Requires server_region.
    region  -- Specify which server region to query.
    page -- What "page" of results to retrieve. page size is "limit"
    filter_str -- special filter string for experienced users

    Further details in WCL API docs
    """
    url = "https://www.warcraftlogs.com:443/v1/rankings/encounter/"+str(encounter_id)
    params = {"api_key":key,
              "metric":metric,
              "size":size,
              "difficulty":difficulty,
              "partition":partition,
              "class":class_id,
              "spec":spec,
              "bracket":bracket,
              "limit":limit,
              "guild":guild,
              "server":server,
              "region":region,
              "page":page,
              "filter":filter_str}
    response = requests.get(url, params=params)
    print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_rankings_character(character_name, server_name, server_region,
                           zone=None, encounter_id=None, metric=None,
                           bracket=None, partition=None):
    """Request a set of rankings for a specific character across all matching encounters. NOTE: Currently not stored in a class"""
    url = "https://www.warcraftlogs.com:443/v1/rankings/character/"+character_name+"/"+server_name+"/"+server_region
    params = {"api_key":key,
              "zone":zone,
              "encounter":encounter_id,
              "metric":metric,
              "bracket":bracket,
              "partition":partition}
    response = requests.get(url, params=params)
    print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_parses(character_name, server_name, server_region, zone=None,
               encounter_id=None, metric=None, bracket=None, 
               compare=None, partition=None):
    """Request a set of parses for a specific character across all matching encounters. NOTE: Currently not stored in a class"""
    url = "https://www.warcraftlogs.com:443/v1/parses/character/"+character_name+"/"+server_name+"/"+server_region
    params = {"api_key":key,
              "zone":zone,
              "encounter":encounter_id,
              "metric":metric,
              "bracket":bracket,
              "compare":compare,
              "partition":partition}
    response = requests.get(url, params=params)
    print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_reports_guild(guild_name, server_name, server_region,
                      start=None, end=None):
    url = "https://www.warcraftlogs.com:443/v1/reports/guild/"+guild_name+"/"+server_name+"/"+server_region
    params = {"api_key":key,
              "start":start,
              "end":end}
    response = requests.get(url, params=params)
    print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_reports_user(username, start=None, end=None):
    url = "https://www.warcraftlogs.com:443/v1/reports/user/"+username
    params = {"api_key":key,
              "start":start,
              "end":end}
    response = requests.get(url, params=params)
    print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data


def wow_report_fights(code, translate=None):
    url = "https://www.warcraftlogs.com:443/v1/report/fights/"+code
    params = {"api_key":key,
              "translate":translate}
    response = requests.get(url, params=params)
    print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_report_events(code, start=None, end=None, actorid=None,
                      actorinstance=None, actorclass=None, cutoff=None,
                      encounter=None, wipes=None, difficulty=None,
                      filter_str=None, translate=None):
    url = "https://www.warcraftlogs.com:443/v1/report/events/"+code
    params = {"api_key":key,
              "start":start, 
              "end":end, 
              "actorid":actorid, 
              "actorinstance":actorinstance, 
              "actorclass":actorclass, 
              "cutoff":cutoff, 
              "encounter":encounter, 
              "wipes":wipes, 
              "difficulty":difficulty, 
              "filter":filter_str,
              "translate":translate}
    response = requests.get(url, params=params)
    print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_report_tables(view, code, start=None, end=None, hostility=None, 
                      by=None, sourceid=None, sourceinstance=None, 
                      sourceclass=None, targetid=None, 
                      targetinstance=None, targetclass=None, 
                      abilityid=None, options=None, cutoff=None, 
                      encounter=None, wipes=None, difficulty=None, 
                      filter_str=None, translate=None):
    url = "https://www.warcraftlogs.com:443/v1/report/tables/"+view+"/"+str(code)
    params = {"api_key":key,
              "start":start, 
              "end":end, 
              "hostility":hostility, 
              "by":by, 
              "sourceid":sourceid, 
              "sourceinstance":sourceinstance, 
              "sourceclass":sourceclass, 
              "targetid":targetid, 
              "targetinstance":targetinstance, 
              "targetclass":targetclass, 
              "abilityid":abilityid, 
              "options":options, 
              "cutoff":cutoff, 
              "encounter":encounter, 
              "wipes":wipes, 
              "difficulty":difficulty, 
              "filter":filter_str,
              "translate":translate}
    response = requests.get(url, params=params)
    print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return parse_json_to_table(json_data, view, code)

def parse_json_to_table(json_data, view, code):
    if(view == "damage-done"):
        table = list()
        for entry in json_data["entries"]:
            table.append(DamageDoneTableEntry(entry, code, json_data["totalTime"]))
        return table
    elif(view == "damage-taken"):
        table = list()
        for entry in json_data["entries"]:
            table.append(DamageTakenTableEntry(entry, code, json_data["totalTime"]))
        return table
    elif(view == "healing"):
        table = list()
        for entry in json_data["entries"]:
            table.append(HealingTableEntry(entry, code, json_data["totalTime"]))
        return table
    elif(view == "casts"):
        table = list()
        for entry in json_data["entries"]:
            table.append(CastsTableEntry(entry, code, json_data["totalTime"]))
        return table
    elif(view == "summons"):
        table = list()
        for entry in json_data["entries"]:
            table.append(SummonsTableEntry(entry, code, json_data["totalTime"]))
        return table
    elif(view == "deaths"):
        table = list()
        for entry in json_data["entries"]:
            table.append(DeathsTableEntry(entry, code))
        return table
    elif(view == "buffs" or view == "debuffs"):
        table = list()
        for entry in json_data["auras"]:
            table.append(AuraTableEntry(entry, code, json_data["useTargets"], json_data["totalTime"], json_data["startTime"], json_data["endTime"]))
        return table
    else:
        return json_data

def generateReportList(json):
    reports = []
    for report in json:
        reports.append(Report(report))
    return reports

def generateUserReportList(username, start=None, end=None):
    return generateReportList(wow_reports_user(username, start=start, end=end))

def generateGuildReportList(guild_name, server_name, server_region, start=None, end=None):
    return generateReportList(wow_reports_guild(guild_name, server_name, server_region, start=start, end=end))


def generateFightList(report_code):
    json = wow_report_fights(report_code)
    allFriendlies = []
    allEnemies = []
    allFriendlyPets = []
    allEnemyPets = []
    fightList = []
    for friendly in json["friendlies"]:
        allFriendlies.append(FightParticipant(friendly, report_code))
    for enemy in json["enemies"]:
        allEnemies.append(FightParticipant(enemy, report_code))
    for friendlypet in json["friendlyPets"]:
        allFriendlyPets.append(FightParticipant(friendlypet, report_code))
    for enemypet in json["enemyPets"]:
        allEnemyPets.append(FightParticipant(enemypet, report_code))
    for fight in json["fights"]:
        friendlies = []
        enemies = []
        friendlypets = []
        enemypets = []
        phases = []
        for friendly in allFriendlies:
            if(friendly.fights.attended(fight["id"])):
                friendlies.append(friendly)
        for enemy in allEnemies:
            if(enemy.fights.attended(fight["id"])):
                enemies.append(enemy)
        for friendlypet in allFriendlyPets:
            if(friendlypet.fights.attended(fight["id"])):
                friendlypets.append(friendlypet)
        for enemypet in allEnemyPets:
            if(enemypet.fights.attended(fight["id"])):
                enemypets.append(enemypet)
        for boss in json["phases"]:
            if(boss["boss"] == fight["boss"]):
                phases = boss["phases"]
        if(fight["boss"]==0):
            fightList.append(TrashFight(fight, report_code, friendlies, enemies, friendlypets, enemypets, phases))    
        else:
            fightList.append(Fight(fight, report_code, friendlies, enemies, friendlypets, enemypets, phases))
    return fightList

key=sys.argv[1]
lst = generateGuildReportList("Vitium","Korgath","US",start=1490241142311)
for l in lst:
    print l.title + " ("+l.id+")"
recent_report_code = lst[len(lst)-1].id

table = wow_report_tables("debuffs", recent_report_code, end=4058391)
print("DEBUFFS")
for entry in table:
    print(entry.name + " -> " + str(entry.totalUses))
    print("    "+str(entry.totalUptime) + " over "+ str(len(entry.bands)))

json_rankings = wow_rankings_encounter(1866, metric="hps", server="Korgath", region="US", guild="Vitium")
print(json_rankings["rankings"][1]["name"])