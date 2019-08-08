#!/usr/bin/env python3
import subprocess
import json

output = subprocess.check_output(["sudo", "pvpn", "--status"])
output = output or ""
output = output.decode('utf8').split("\n")

with open('.config/argos/countries.json', 'r') as c:
    available_countries = json.loads(c.read())


def get_country_by_code(code):
    return next(cntry for cntry in available_countries if cntry["code"] == code.upper())


for o in output:
    if '[ProtonVPN Status]: Not Running' == o:
        print("| iconName=network-error")
        break
    elif 'Exit Country' in o:
        country_code = o.split(': ')[1].strip()
        if country_code:
            country = get_country_by_code(country_code)
            if country:
                print("| image='%s'" % country['image'])
                break

print("| iconName=network-error")
