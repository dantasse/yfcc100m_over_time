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

counter = 0
for line in csv.reader(open(args.infile), delimiter='\t'):
    counter += 1
    if counter % (1000*1000) == 0:
        print "This many photos processed: %s" % str(counter)

    try:
        date = datetime.datetime.strptime(line[5][0:10], '%Y-%m-%d').date()
    except:
        print "skipping row because failed to parse date: " + str(line)
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
