# -*- coding: utf-8 -*-
# Author : Dimitrios Zacharopoulos
# All copyrights to Obipixel Ltd
# 22 October 2022

#!/usr/bin/env python3

import dns.resolver
import whois
import requests
import simplekml
import os

# Print ASCII art
print("""
░█▀▄░█▄░█░▄▀▀▒█▀░█░█▄░█░█▀▄
▒█▄▀░█▒▀█▒▄██░█▀░█░█▒▀█▒█▄▀
""")


def print_dns_records(records, record_type, kml):
    print(f'\033[1;41m {record_type} Record \033[m')
    if len(records) > 0:
        for record in records:
            print(record.to_text())
            if record.rdtype == dns.rdatatype.A:
                ip_address = record.to_text()
                url = f"http://ip-api.com/json/{ip_address}?fields=lon,lat"
                response = requests.get(url).json()
                print(f"Longitude: {response['lon']}, Latitude: {response['lat']}")
                kml.newpoint(name=ip_address, coords=[(response['lon'], response['lat'])])
    else:
        print(f'No {record_type} record found')

def perform_dns_lookup(domain):
    kml = simplekml.Kml()
    try:
        answers = dns.resolver.resolve(domain, 'A')
        print('\n')
        print_dns_records(answers, 'A', kml)
    except dns.resolver.NoAnswer:
        print_dns_records([], 'A', kml)
    except dns.resolver.NXDOMAIN:
        print(f'{domain} does not exist')
    except dns.resolver.Timeout:
        print(f'Timeout while resolving {domain}')

    print()
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        print('\n')
        print_dns_records(answers, 'CNAME', kml)
    except dns.resolver.NoAnswer:
        print_dns_records([], 'CNAME', kml)

    try:
        answers = dns.resolver.resolve(domain, 'MX')
        print('\n')
        print_dns_records(answers, 'MX', kml)
    except dns.resolver.NoAnswer:
        print_dns_records([], 'MX', kml)

    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        print('\n')
        print_dns_records(answers, 'TXT', kml)
    except dns.resolver.NoAnswer:
        print_dns_records([], 'TXT', kml)

    try:
        answers = dns.resolver.resolve(domain, 'SOA')
        print('\n')
        print_dns_records(answers, 'SOA', kml)
    except dns.resolver.NoAnswer:
        print_dns_records([], 'SOA', kml)

    kml_file_name = f"dnsFIND-{domain}.kml"
    kml.save(kml_file_name)
    print('\n\033[1;41m KML file has been created and saved to: \033[m')
    print(os.path.abspath(kml_file_name))
    print()


def perform_whois_lookup(domain):
    try:
        domain_info = whois.whois(domain)
        print('\033[1;41m WHOIS Information \033[m')
        print(f'Domain Name: {domain_info.domain_name}')
        print(f'Registrar: {domain_info.registrar}')
        print(f'Name Servers: {domain_info.name_servers}')
    except whois.parser.PywhoisError:
        print(f'No WHOIS information found for {domain}')

domain = input('Enter a domain name: ')
perform_dns_lookup(domain)
perform_whois_lookup(domain)
