from pycraftlogs import *
import sys

key=sys.argv[1]
print(key)
pycraftlogs.update_key(key)
print(pycraftlogs.default_key)
lst = pycraftlogs.generate_guild_report_list("Vitium","Korgath","US", key=key)
for l in lst:
    print(l.title + " ("+l.id+")")
recent_report_code = lst[len(lst)-1].id

table = wow_report_tables("debuffs", recent_report_code, end=4058391, key=key)
print("DEBUFFS")
for entry in table:
    print(entry.name + " -> " + str(entry.totalUses))
    print("    "+str(entry.totalUptime) + " over "+ str(len(entry.bands)))

json_rankings = wow_rankings_encounter(1866, metric="hps", server="Korgath", region="US", guild="Vitium", key=key)
print(json_rankings["rankings"][1]["name"])
print(wow_get_report(recent_report_code, key=key).title,)