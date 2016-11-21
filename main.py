#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import googlemaps
import random
import AdvancedHTMLParser
from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import quote

from helpers import write_name, write_zip_code, write_address, write_image, write_geolocation

parser = AdvancedHTMLParser.AdvancedHTMLParser()
parser.parseStr(urlopen("http://zoneby.net/catalog/iu_by/").read().decode("windows-1251", "replace"))
plain_prisons_text = parser.getElementsByClassName('doctext').getElementsByTagName('p')
prisons_by_regions = [x for x in plain_prisons_text[2:14] if not x.attributes]

parsed_prisons = []
for prisons_block in prisons_by_regions:
    prisons = prisons_block.innerHTML.split('<p')[0].split('&nbsp;<br />')
    for prison in prisons:
        try:
            prison_components = [x.strip() for x in prison.split('<br />') if x.strip()]
            name = prison_components[0]
            zip_code = prison_components[1].split(',')[0].strip()
            address = ','.join(prison_components[1].split(',')[1:])
            phones = []
            for phone_info in prison_components[2:]:
                phones.extend(phone_info.split('тел.')[-1].split(','))

            parsed_prisons.append({
                'name': name,
                'address': address,
                'zip_code': zip_code,
                'phones': phones
            })
        except IndexError:
            continue

gmaps = googlemaps.Client(key='AIzaSyAs5bmk9_Vs586Q8s2ExTVwz7_rcmzl7xY')

for prison in parsed_prisons[0:1]:
    scs_file = open(prison['name'] + '.scs', 'w')
    system_name = 'prison_' + str(random.getrandbits(30))
    write_name(scs_file, **{'system_name': system_name, 'name': prison['name']})
    write_zip_code(scs_file, **{'system_name': system_name, 'zip_code': prison['zip_code']})
    write_address(scs_file, **{'system_name': system_name, 'address': prison['address']})

    geocode_result = gmaps.geocode(prison['address'])
    if geocode_result:
        write_geolocation(scs_file, **{'system_name': system_name,
                                       'lat': geocode_result[0]['geometry']['location']['lat'],
                                       'lng': geocode_result[0]['geometry']['location']['lng']})

    request_url = 'http://35.161.57.139:8080/gpix/v1/gpix?keyword={0}&limit=1'.format(quote(prison['name']))
    request = Request(request_url)
    request.add_header('Authorization', 'QsiP2ZX7Ps')
    response = json.loads(urlopen(request).read().decode('utf-8'))
    image_url = response['data']['images'][0]['image_url']
    image_name = "{0}.{1}".format(prison['name'], image_url.split('.')[-1])
    urlretrieve(image_url, image_name)
    write_image(scs_file, **{'system_name': system_name, 'name': prison['name'], 'image_name': image_name})
