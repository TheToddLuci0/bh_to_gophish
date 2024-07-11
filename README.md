# Generate GoPhish targets from Bloodhound
So, you've got bloodhound pulled, and you want to generate a list of phish targets.
No more copy-paste, python to the rescue!

This simple script generates a CSV target file compatible with GoPhish from a list of email addresses you want to target.

### Useage

```
$ python3 bh_to_gohpish.py -h                                                    
usage: bh_to_gohpish.py [-h] -o O -u U [--url URL] [--username USERNAME] [--password PASSWORD]

options:
  -h, --help           show this help message and exit
  -o O                 Output filename
  -u U                 Input list of emails
  --url URL            Neo4j endpint URL
  --username USERNAME  Neo4j username
  --password PASSWORD  Neo4j password
```

Example:
```bash
./bh_to_gophish.py -u se_target_emails.txt -o gophish_targets.csv
```