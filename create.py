import sys
import os
import json
import csv
import difflib
import subprocess
import random

# Countries GeoJSON file
COUNTRIES_FILE = 'data/countries/countries.geojson'
COUNTRY_NAME_FIELD = 'name_long'

# Members CSV file
MEMBERS_FILE = 'data/un_members/un_members.csv'
MEMBER_NAME_FIELD = 'member_state'
YEAR_FIELD = 'year_of_admission'

# Output GeoJSON file
OUTPUT_FILE = 'output/un_members.geojson'
COMMIT_PREFIX = 'New UN members'

try:
    subprocess.check_output(['git', 'status'])
except subprocess.CalledProcessError:
    print 'Initialize a git repo please'
    sys.exit(1)

with open(COUNTRIES_FILE, 'r') as f:
    countries = json.loads(f.read())

country_names = [c['properties'][COUNTRY_NAME_FIELD]
                 for c in countries['features']]

members = []
with open(MEMBERS_FILE, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        members.append(row)

members = sorted(members,
                 key=lambda k: (k[YEAR_FIELD], k[MEMBER_NAME_FIELD].lower()))


def get_country(name):

    def get_country_feature(name):
        for country in countries['features']:
            if country['properties'][COUNTRY_NAME_FIELD] == name:
                return country

    if name in country_names:
        match = [name]
        country_names.remove(name)
        return get_country_feature(name)
    else:
        match = difflib.get_close_matches(name, country_names, 1, 0.6)
        if match:
            return get_country_feature(match[0])
    print 'Could not find a match for ', name
    return


def add_fill_colour_and_year(countries, year):

    color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))

    for country in countries:
        country['properties']['joined'] = year
        country['properties']['fill'] = color


def commit_year(year, countries_joined):
    output_file = OUTPUT_FILE
    if not os.path.exists(output_file):
        current_countries = {
            'type': 'FeatureCollection',
            'features': []
        }
    else:
        with open(output_file, 'r') as f:
            current_countries = json.loads(f.read())

    add_fill_colour_and_year(countries_joined, year)

    current_countries['features'].extend(countries_joined)

    with open(output_file, 'w') as f:
        f.write(json.dumps(current_countries))

    subprocess.call(['git', 'add', output_file])

    commit_message = '{0} {1}\n\n{2}'.format(
        COMMIT_PREFIX,
        year,
        ', '.join([c['properties'][COUNTRY_NAME_FIELD]
                   for c in countries_joined])
    )
    subprocess.call(['git', 'commit', '-m', commit_message])

year = members[0][YEAR_FIELD]
countries_joined = []

for member in members:
    country = get_country(member[MEMBER_NAME_FIELD])
    if not country:
        continue

    if member[YEAR_FIELD] != year:
        commit_year(year, countries_joined)

        countries_joined = []
        year = member[YEAR_FIELD]

    countries_joined.append(country)
commit_year(year, countries_joined)
