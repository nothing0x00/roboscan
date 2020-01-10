
# RoboScan
### Automated Scanning of Sites for robots.txt Entries and Directory Brute Forcer


Roboscan is a simple python script to download a robots.txt file from a target site,
 scrape the file for possible directories, scan the site for these directories,
and then run a fuzzing attack on the target site using a specified dictionary. It is useful in situations in which a robots.txt file contains a variety of entries that need to be checked for validity.

### Installation and Use

To get roboscan running just do the following:

`git clone `

`pip3 install requirements.txt`

`python3 roboscan.py [-h][-t target][-d dictionary]`

### Note: This is an older codebase that is in a process of rewrite with new functionality added...Coming soon
