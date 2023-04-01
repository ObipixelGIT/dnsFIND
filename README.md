# dnsFIND
dnsFIND performs DNS and WHOIS lookups for a given domain name. It then uses the dns.resolver and whois Python libraries to retrieve DNS and WHOIS information, respectively, and the requests and simplekml libraries to retrieve the location of IP addresses and generate a KML file with the locations of IP addresses found in DNS A records.


## How this script works?

- Performs DNS and WHOIS lookups for a given domain name.
- It uses the dns.resolver module to query DNS records for the domain, and the whois module to retrieve WHOIS information for the domain.
- It also uses the requests module to query the IP address location using the IP-API service, and the simplekml module to generate a KML file with the location of the IP addresses found in the DNS A records.
- When the script is executed, it prompts the user to enter a domain name, and then calls the perform_dns_lookup and perform_whois_lookup functions to retrieve and print the DNS and WHOIS information for the domain, respectively.
- The DNS information includes A, CNAME, MX, TXT, and SOA records, and for each A record found, the IP address location is also retrieved and added to a KML file.
- The KML file is saved in the same directory as the script, and its name includes the domain name.
- You can then Import the KML file from your system into Google Earth (https://earth.google.com).
- Once in Google Earth, click the 3 lines menu, choose Projects, then import a KML from your system and open the kml you created. You can get the location of the KML from your output on the screen. Screenshots have been provided of an example domain: domain.com
- The script uses ANSI escape sequences to print colored output to the console.

## Preparation

- dns.resolver: This library provides DNS resolution functionality.
- whois: This library provides WHOIS lookup functionality.
- requests: This library provides HTTP requests functionality.
- simplekml: This library provides KML file generation functionality.

To install these libraries, you can run the following command in your terminal:
```bash
pip3 install dns whois requests simplekml
```

## Permissions

Ensure you give the script permissions to execute. Do the following from the terminal:
```bash
sudo chmod +x dnsFIND.py
```

## Usage
```bash
sudo python3 dnsFIND.py
```

## Sample script
```
#!/usr/bin/env python3

import dns.resolver
import whois
import requests
import simplekml
import os

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
```

## Sample output
```bash
sudo python3 dnsFIND.py

░█▀▄░█▄░█░▄▀▀▒█▀░█░█▄░█░█▀▄
▒█▄▀░█▒▀█▒▄██░█▀░█░█▒▀█▒█▄▀

Enter a domain name: domain.com


 A Record
18.221.195.49
Longitude: -83.1141, Latitude: 40.0992

 CNAME Record
No CNAME record found


 MX Record
10 mx.domain.com.


 TXT Record
"google-site-verification=zlpN6bg9OaBJVw4Lv4-1fZ2wHekVqEnEGBXwuonNpBM"
"v=spf1 ip4:38.113.1.0/24 ip4:38.113.20.0/24 ip4:12.45.243.128/26 ip4:65.254.224.0/19 include:_spf.google.com include:_spf.qualtrics.com -all"
"google-site-verification=1aIdxE8tG_8BUCMClWep8Z33AIxgsL91plweqqCuNZU"
"google-site-verification=M2Ehy1mb_Yh-Z57igzRDXPY35c5nNsYmI_l3B6D9zZs"


 SOA Record
ns-2022.awsdns-60.co.uk. awsdns-hostmaster.amazon.com. 2017090501 7200 900 1209600 86400

 KML file has been created and saved to:
/Users/dimitrioszacharopoulos/PycharmProjects/Security/dnsFIND-domain.com.kml

 WHOIS Information
Domain Name: DOMAIN.COM
Registrar: Domain.com, LLC
Name Servers: ['NS-1250.AWSDNS-28.ORG', 'NS-166.AWSDNS-20.COM', 'NS-2022.AWSDNS-60.CO.UK', 'NS-683.AWSDNS-21.NET', 'ns-166.awsdns-20.com', 'ns-683.awsdns-21.net', 'ns-1250.awsdns-28.org', 'ns-2022.awsdns-60.co.uk']
```

## Disclaimer
"The scripts in this repository are intended for authorized security testing and/or educational purposes only. Unauthorized access to computer systems or networks is illegal. These scripts are provided "AS IS," without warranty of any kind. The authors of these scripts shall not be held liable for any damages arising from the use of this code. Use of these scripts for any malicious or illegal activities is strictly prohibited. The authors of these scripts assume no liability for any misuse of these scripts by third parties. By using these scripts, you agree to these terms and conditions."

## License Information

This library is released under the [Creative Commons ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/). You are welcome to use this library for commercial purposes. For attribution, we ask that when you begin to use our code, you email us with a link to the product being created and/or sold. We want bragging rights that we helped (in a very small part) to create your 9th world wonder. We would like the opportunity to feature your work on our homepage.
