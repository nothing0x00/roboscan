import requests
import argparse
import wget
import re, sys
import time
from termcolor import colored


print(colored('''


########   #######  ########   #######   ######   ######     ###    ##    ##
##     ## ##     ## ##     ## ##     ## ##    ## ##    ##   ## ##   ###   ##
##     ## ##     ## ##     ## ##     ## ##       ##        ##   ##  ####  ##
########  ##     ## ########  ##     ##  ######  ##       ##     ## ## ## ##
##   ##   ##     ## ##     ## ##     ##       ## ##       ######### ##  ####
##    ##  ##     ## ##     ## ##     ## ##    ## ##    ## ##     ## ##   ###
##     ##  #######  ########   #######   ######   ######  ##     ## ##    ##


Automated Scanning of Sites for robots.txt Entries and Directory Brute Forcer
''','red'))
# Add folder creation functionality and project naming
parser = argparse.ArgumentParser(description = "A Simple Script to Bruteforce Web Directories Based on robots.txt Files")

parser.add_argument('-t', '--target', help = "Input domain name", dest = 'target')
parser.add_argument('-d', '--dictionary', help = "Directory Brute Force", dest = 'dictionary')


args = parser.parse_args()

class Reprinter:
    def __init__(self):
        self.text = ''

    def moveup(self, lines):
        for _ in range(lines):
            sys.stdout.write("\x1b[A")

    def reprint(self, text):
        # Clear previous text by overwritig non-spaces with spaces
        self.moveup(self.text.count("\n"))
        sys.stdout.write(re.sub(r"[^\s]", " ", self.text))

        # Print new text
        lines = min(self.text.count("\n"), text.count("\n"))
        self.moveup(lines)
        sys.stdout.write(text)
        self.text = text

reprinter = Reprinter()


def robots():
    site = str(args.target) + '/robots.txt'
    scan = requests.get(site, timeout = 5)

    if scan.status_code == 200:
        print(colored('[*] robots.txt file found', 'yellow'))
        print(colored('Downloading robots.txt file', 'yellow'))
        wget.download(site)
        print('\n')

        bots = open('robots.txt', 'r')
        data = bots.readlines()
        bots.close()
        for line in data:
            if ':' in line:
                form, bots_prov = line.split(":", 1)
                bots_new = bots_prov.replace(" ", "")
                #print bots_new
                repo = open('repo.txt', 'a')
                repo.write(bots_new)

        infile = open('repo.txt').readlines()
        print('\n')
        print(colored('[+] Checking info from robots.txt file...', 'yellow'))
        for line in infile:
               query = args.target + line

               try:
                   request = requests.get(query, timeout = .5)
                   output = query
                   reprinter.reprint(output)
                   target_list = open('targets.txt', 'a')
                   if request.status_code == 200:
                       print("[+]Target Found: %s" % query + '\n')
                       target_list.write(query)

               except requests.exceptions.RequestException as e:
                    pass





    if scan.status_code != 200:
        print(colored('[!] Error downloading robots.txt', 'red'))
        pass


    print(colored("\n[+] Robots.txt scan Complete!", 'yellow'))

def brute():
    print(colored("\n[*]Directory Brute Forcing Beginning...", 'yellow'))
    print("Loading Dictionary: %s \n" % args.dictionary)
    lists = open(args.dictionary).readlines()
    for line in lists:
        query = args.target + "/" + line
        try:
            request = requests.get(query, timeout = .5)
            output = query
            reprinter.reprint(query)

            target_list = open('targets.txt', 'a')

            if request.status_code == 200:
                print("[+]Target Found: %s" % query)
                target_list.write(query)
                files = open('extensions.txt').readlines()

                for line in lists:

                    for ext in files:

                        file_query = query + "/" + line + ext
                        request2 = requests.get(file_query, timeout = .5)
                        output2 = file_query
                        reprinter.reprint(file_query)
                        target_list2 = open('targets.txt', 'a')

                        if request2.status_code == 200:
                            print("[+]Target Found: %s" % file_query)
                            target_list2.write(file_query)

        except requests.exceptions.RequestException as e:
            print(colored("Error Error Error!", 'red'))
            pass

    print(colored("[+]Directoty Brute Forcing Complete", 'yellow'))




robots()
if args.dictionary:
    brute()
print(colored('[*] Scan Complete', 'yellow'))
print(colored('[*] See targets.txt for results', 'yellow'))
