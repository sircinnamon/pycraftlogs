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

report = wow_get_report(recent_report_code, key=key)
print(wow_get_report(recent_report_code, key=key).title + " "+str(report.start) + "-"+str(report.end)+" "+str(report.end-report.start))
fights = generate_fight_list(recent_report_code, key=key)
for f in fights:
	#print(f.name)
	x = 0

table = wow_report_tables("healing", recent_report_code, end=11718355, key=key, sourceid=117)
#print(table[0].json)
print("\nHEAL")
for t in table:
	print(t.name+" "+str(t.total))

print("\nDPS")
table = wow_report_tables("damage-done", recent_report_code, end=11718355, key=key, sourceid=117)
for t in table:
	print(t.name+" "+str(t.total))

print("\nTANK")
table = wow_report_tables("damage-taken", recent_report_code, end=11718355, key=key, sourceid=117)
for t in table:
	print(t.name+" "+str(t.total))