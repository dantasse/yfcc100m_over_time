#!/usr/bin/env python

# Input: a yfcc100m file. Output: a csv with date, number geotagged, number
# non-geotagged.

import argparse, csv, collections, datetime
parser = argparse.ArgumentParser()
parser.add_argument('--infile', default='yfcc100m_dataset_1k.tsv')
parser.add_argument('--outfile', default='yfcc_per_day.csv')
args = parser.parse_args()

geotagged = collections.Counter() # date -> count
nongeotagged = collections.Counter() # date -> count

outwriter = csv.writer(open(args.outfile, 'w'))

# longest_line=0
# counter = 0
# for line in open(args.infile):
#     counter +=1
#     if counter % 1000000 == 0:
#         print counter
#     if len(line) > longest_line:
#         longest_line = len(line)
# 
# print "Found longest line, it is: %s" % str(longest_line)
longest_line = 197990 # Found this when I ran it once before.
counter = 0
reader = csv.reader(open(args.infile), delimiter='\t')
csv.field_size_limit(longest_line)
for line in reader:
    counter += 1
    print counter
    if counter % (1000*1000) == 0:
        print "This many photos processed: %s" % str(counter)

    try:
        date = datetime.datetime.strptime(line[5][0:10], '%Y-%m-%d').date()
    except:
        print "skipping row because failed to parse date: " + str(line[5])
        continue
    lon = line[12]
    lat = line[13]
    if lon and lat:
        # print date, lon, lat, "geo"
        geotagged[date] += 1
    else:
        # print date, "nongeo"
        nongeotagged[date] += 1

current_date = datetime.date(2004,1,1)
while current_date <= datetime.date(2016,1,1):
    outwriter.writerow([str(current_date), geotagged[current_date], nongeotagged[current_date]])
    current_date += datetime.timedelta(1)
