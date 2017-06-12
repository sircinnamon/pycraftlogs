"""pycraftlogs is an API wrapper for the WarcraftLogs API.

The WarcraftLogs API is still under construction but in its current state it
can do many useful things. This wrapper allows simpler interactions with the
API to occur within any python program.
"""
import requests
import sys
from .pycraftlogsclasses import *

default_key = "yourAPIkey"
baseURL = "https://www.warcraftlogs.com:443/v1/"

def wow_zones(key=default_key):
    """Request a listing of zones and return a list of Zone objects."""
    response = requests.get(baseURL + "zones?api_key=" + key)
    json_data = response.json()
    zones = list()
    for entry in json_data:
        zones.append(Zone(entry))
    return zones

def wow_classes(key=default_key):
    """Request a listing of playable classes and return a list of _Class objects."""
    response = requests.get(baseURL + "classes?api_key=" + key)
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
                           region=None, page=None, filter_str=None,key=default_key):
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
    key -- The public API key to use.

    Further details in WCL API docs
    """
    url = baseURL + "rankings/encounter/" + str(encounter_id)
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
              "filter":filter_str
              }
    response = requests.get(url, params=params)
    #print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_rankings_character(character_name, server_name, server_region,
                           zone=None, encounter_id=None, metric=None,
                           bracket=None, partition=None, key=default_key):
    """Request a set of rankings for a specific character across all matching encounters. NOTE: Currently not stored in a class

    Keyword arguments:
    zone -- Limit results to a specific zone (raid).
    encounter_id -- Limit results to specific encounter.
    metric -- What metric to rank by. e.g. dps, hps etc.
    bracket -- Bracket to query. See /zones response for info.
    partition -- What partition to query, if multiple exist.
    key -- The public API key to use.

    Further details in WCL API docs
    """
    url = baseURL + "rankings/character/"+character_name+"/"+server_name+"/"+server_region
    params = {"api_key":key,
              "zone":zone,
              "encounter":encounter_id,
              "metric":metric,
              "bracket":bracket,
              "partition":partition}
    response = requests.get(url, params=params)
    #print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_parses(character_name, server_name, server_region, zone=None,
               encounter_id=None, metric=None, bracket=None, 
               compare=None, partition=None, key=default_key):
    """Request a set of parses for a specific character across all matching encounters. NOTE: Currently not stored in a class

    Keyword arguments:
    zone -- Limit results to a specific zone (raid).
    encounter_id -- Limit results to specific encounter.
    metric -- What metric to rank by. e.g. dps, hps etc.
    bracket -- Bracket to query. See /zones response for info.
    compare -- Defines whether to compare vs rankings or statistics. 0 or 1 respectively.
    partition -- What partition to query, if multiple exist.
    key -- The public API key to use.

    Further details in WCL API docs
    """
    url = baseURL + "parses/character/"+character_name+"/"+server_name+"/"+server_region
    params = {"api_key":key,
              "zone":zone,
              "encounter":encounter_id,
              "metric":metric,
              "bracket":bracket,
              "compare":compare,
              "partition":partition}
    response = requests.get(url, params=params)
    #print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_reports_guild(guild_name, server_name, server_region,
                      start=None, end=None, key=default_key):
    """Request a set of uploaded reports for a specified guild.

    Keyword arguments:
    start -- UNIX start time to contain search
    end -- UNIX end time to contain search
    key -- The public API key to use.
    """
    url = baseURL + "reports/guild/"+guild_name+"/"+server_name+"/"+server_region
    params = {"api_key":key,
              "start":start,
              "end":end}
    response = requests.get(url, params=params)
    #print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_reports_user(username, start=None, end=None, key=default_key):
    """Request a set of reports uploaded by a certain WCL user.

    Keyword arguments:
    start -- UNIX start time to contain search
    end -- UNIX end time to contain search
    key -- The public API key to use.
    """
    url = baseURL+"reports/user/"+username
    params = {"api_key":key,
              "start":start,
              "end":end}
    response = requests.get(url, params=params)
    #print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_get_report(code, translate=None, key=default_key):
    """Create a report object from a given report ID

    Keyword arguments:
    translate -- Flag to determine if results should be translated to host lang.
    key -- The public API key to use.
    """
    url = baseURL + "report/fights/"+code
    params = {"api_key":key,
              "translate":translate}
    response = requests.get(url, params=params)
    print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    json_data["id"]=code
    del json_data["fights"]
    del json_data["lang"]
    del json_data["friendlies"]
    del json_data["enemies"]
    del json_data["friendlyPets"]
    del json_data["enemyPets"]
    del json_data["phases"]
    return Report(json_data)

def wow_report_fights(code, translate=None, key=default_key):
    """Request a list of fights contained in a report.

    Keyword arguments:
    translate -- Flag to determine if results should be translated to host lang.
    key -- The public API key to use.
    """
    url = baseURL + "report/fights/"+code
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
                      filter_str=None, translate=None, key=default_key):
    """Request a list of events contained in a report.

    Keyword arguments:
    start -- UNIX offset from beginning of report to start list.
    end -- UNIX offset from beginning to end list.
    actorid -- Only return events with target or source being actor specified (or their pets).
    actorinstance -- Only return events where source or target is in specified instance.
    actorclass -- Only return events whose source or target is of the specified class.
    cutoff -- Number of deaths at which events should not be included.
    encounter -- Only return events that ocurred during the specified encounter.
    wipes -- Only view events from wiped encounters.
    difficulty -- Only view events occurring in specified difficulty.
    filter_str -- Filter string for advanced users.
    translate -- Flag to determine if results should be translated to host lang.
    key -- The public API key to use.
    """
    url = baseURL + "report/events/"+code
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
    #print(response.url + " " + str(response.status_code))
    response.raise_for_status()
    json_data = response.json()
    return json_data

def wow_report_tables(view, code, start=None, end=None, hostility=None, 
                      by=None, sourceid=None, sourceinstance=None, 
                      sourceclass=None, targetid=None, 
                      targetinstance=None, targetclass=None, 
                      abilityid=None, options=None, cutoff=None, 
                      encounter=None, wipes=None, difficulty=None, 
                      filter_str=None, translate=None, key=default_key):
    """Request a table of data from a specific report.

    View is the type of data the table displays, which may change the specific
    format of the returned data. Supports damage-done, damage-taken etc.

    Keyword arguments:
    start -- UNIX offset from beginning of report to start list of included events.
    end -- UNIX offset from beginning to end list of included events.
    hostility -- Flag determines whether data is collected for friendlies or enemies.
    by -- indicate how to group table entries. e.g. by source, by target, by ability etc.
    sourceid -- Only collect data where source is this id.
    sourceinstance -- Only collect data where source instance is this id.
    sourceclass -- Only collect data where source class is this id.
    targetid -- Only collect data where target is this id.
    targetinstance -- Only collect data where target instance is this id.
    targetclass -- Only collect data where target class is this id.
    abilityid -- only collect data where the ability matches this id.
    options -- Special include/exclude options. 
    cutoff -- Number of deaths at which events should not be included.
    encounter -- Only return events that ocurred during the specified encounter.
    wipes -- Only view events from wiped encounters.
    difficulty -- Only view events occurring in specified difficulty.
    filter_str -- Filter string for advanced users.
    translate -- Flag to determine if results should be translated to host lang.
    key -- The public API key to use.

    See WCL API docs for more info
    """
    url = baseURL+"report/tables/"+view+"/"+str(code)
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
    return parse_json_to_table(json_data, view, code, bysource=(params["sourceid"] is not None))

def parse_json_to_table(json_data, view, code, bysource=False):
    """Given json table data, construct an object containing the data"""
    if(view == "damage-done"):
        table = list()
        if(bysource):
            for entry in json_data["entries"]:
                table.append(DamageDoneBySourceTableEntry(entry, code, json_data["totalTime"]))
        else:
            for entry in json_data["entries"]:
                table.append(DamageDoneTableEntry(entry, code, json_data["totalTime"]))
        return table
    elif(view == "damage-taken"):
        table = list()
        if(bysource):
            for entry in json_data["entries"]:
                table.append(DamageTakenBySourceTableEntry(entry, code, json_data["totalTime"]))
        else:
            for entry in json_data["entries"]:
                table.append(DamageTakenTableEntry(entry, code, json_data["totalTime"]))
        return table
    elif(view == "healing"):
        table = list()
        if(bysource):
            for entry in json_data["entries"]:
                table.append(HealingBySourceTableEntry(entry, code, json_data["totalTime"]))
        else:
            for entry in json_data["entries"]:
                table.append(HealingTableEntry(entry, code, json_data["totalTime"]))
        return table
    elif(view == "casts"):
        table = list()
        if(bysource):
            for entry in json_data["entries"]:
                table.append(CastsBySourceTableEntry(entry, code, json_data["totalTime"]))
        else:
            for entry in json_data["entries"]:
                table.append(CastsTableEntry(entry, code, json_data["totalTime"]))
        return table
    elif(view == "summons"):
        table = list()
        if(bysource):
            for entry in json_data["entries"]:
                table.append(SummonsBySourceTableEntry(entry, code, json_data["totalTime"]))
        else:
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

def generate_report_list(json):
    """Given a json listing of reports, create report objects and place in a list."""
    reports = []
    for report in json:
        reports.append(Report(report))
    return reports

def generate_user_report_list(username, start=None, end=None, key=default_key):
    """Return a list of reports uploaded by the given WCL user."""
    return generate_report_list(wow_reports_user(username, start=start, end=end, key=key))

def generate_guild_report_list(guild_name, server_name, server_region, start=None, end=None, key=default_key):
    """Return a list of reports matched to given guild."""
    return generate_report_list(wow_reports_guild(guild_name, server_name, server_region, start=start, end=end, key=key))


def generate_fight_list(report_code, key=default_key, no_trash=False):
    """Return a list of fight objects contained in a given report."""
    json = wow_report_fights(report_code, key=key)
    allFriendlies = [FightParticipant(x, report_code) for x in json["friendlies"]] if len(json["friendlies"])>0 else list()
    allEnemies = [FightParticipant(x, report_code) for x in json["enemies"]] if len(json["enemies"])>0 else list()
    allFriendlyPets = [FightParticipant(x, report_code) for x in json["friendlyPets"]] if len(json["friendlyPets"])>0 else list()
    allEnemyPets = [FightParticipant(x, report_code) for x in json["enemyPets"]] if len(json["enemyPets"])>0 else list()
    fightList = []
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
        if("phases" in json):
            for boss in json["phases"]:
                if(boss["boss"] == fight["boss"]):
                    phases = boss["phases"]
        if(fight["boss"]==0):
            if(no_trash):
                #skip adding this
                pass
            else:
                fightList.append(TrashFight(fight, report_code, friendlies, enemies, friendlypets, enemypets, phases))    
        else:
            fightList.append(Fight(fight, report_code, friendlies, enemies, friendlypets, enemypets, phases))
    return fightList

def generate_player_attendance_list(report_code, key=default_key):
    """Return a list of players and attended fights contained in a given report."""
    json = wow_report_fights(report_code, key=key)
    allFriendlies = list(map(FightParticipant, json["friendlies"], report_code)) if len(json["friendlies"])>0 else list()
    return allFriendlies

def update_key(new_API_key):
    default_key=new_API_key
    return True