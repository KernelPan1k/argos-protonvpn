#!/usr/bin/env python3

import json

import requests

with open('.config/argos/countries.json', 'r') as c:
    available_countries = json.loads(c.read())
    available_code = [c['code'].upper() for c in available_countries]


def get_country_by_code(code):
    return next(cntry for cntry in available_countries if cntry["code"] == code.upper())


protonServerReq = requests.get("https://api.protonmail.ch/vpn/logicals")
protonVPNData = json.loads(protonServerReq.text)
browseServer = {}

print("VPN\n---")

for item in protonVPNData['LogicalServers'][::-1]:
    if ("1" in str(item['Features']) or "CH" in item['ExitCountry']) \
            and item['ExitCountry'] in available_code \
            and (str((item['Tier'])) == "1" or str((item['Tier'])) == "2" or str((item['Tier'])) == "3"):
        browserCountry = browseServer.get(item["ExitCountry"].encode("utf-8"), [])
        browserCountry.append((item["ExitCountry"], item['Name'], item['Score']))
        browseServer[item["ExitCountry"].encode("utf-8")] = browserCountry

for k, v in browseServer.items():
    browseServer[k] = sorted(v, key=lambda x: x[2])[:2]

print("Logout | useMarkup=false bash='sudo pvpn -d' terminal=false")
print("Fast secure core | useMarkup=false bash='sudo pvpn -d && sudo pvpn -sc' terminal=false")
print("Servers list")

for v in browseServer.values():
    if len(v):
        for s in v:
            country = get_country_by_code(s[0])
            if country:
                print("--%s | useMarkup=false bash='sudo pvpn -d && sudo pvpn -c %s udp' terminal=false image='%s'" % (
                    country['name'], s[1], country['image']))
