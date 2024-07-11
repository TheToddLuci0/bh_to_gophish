#!/usr/bin/env python3
import requests
import argparse
from requests.auth import HTTPBasicAuth
import csv


CSV_HEADER = ['First Name', 'Last Name', 'Email', 'Position']
NEO_QUERY = "MATCH (u:User {{email:\"{email}\"}}) RETURN u.displayname, u.email, u.title"


def do_query(args, query, data_format=None):

    data_format = [data_format, "row"][data_format == None]
    data = {
        "statements" : [
            {
                "statement" : query,
                "resultDataContents" : [ data_format ]
            }
        ]
    }
    headers = {'Content-type': 'application/json', 'Accept': 'application/json; charset=UTF-8'}
    auth = HTTPBasicAuth(args.username, args.password)

    r = requests.post(args.url, auth=auth, headers=headers, json=data)

    if r.status_code == 401:
        print("Authentication error: the supplied credentials are incorrect for the Neo4j database, specify new credentials with --username & --password")
        exit()
    elif r.status_code >= 300:
        print("Failed to retrieve data. Server returned status code: {}".format(r.status_code))
        exit()
    else:
        return r.json()['results'][0]['data']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', required=True, help="Output filename")
    ap.add_argument('-u', required=True, help="Input list of emails")
    ap.add_argument('--url', default='http://127.0.0.1:7474/db/neo4j/tx/commit', help="Neo4j endpint URL")
    ap.add_argument('--username', default="neo4j", help="Neo4j username")
    ap.add_argument('--password', default='bloodhound', help='Neo4j password')
    
    args = ap.parse_args()
    with open(args.u, 'r') as f:
        emails = f.readlines()
    with open(args.o , 'w') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        for e in emails:
            q = NEO_QUERY.format(email=e.strip())
            r = do_query(args, q)
            if len(r) == 0:
                writer.writerow({
                    'First Name': e.strip().split('@')[0],
                    'Last Name': None,
                    'Email': e.strip(),
                    'Position': None
                })
                continue
            first = r[0]['row'][0].split()[0]
            last = r[0]['row'][0].split()[-1]
            writer.writerow({
                'First Name': first,
                'Last Name': last,
                'Email': r[0]['row'][1],
                'Position': r[0]['row'][2]
            })
    





if __name__=='__main__':
    main()