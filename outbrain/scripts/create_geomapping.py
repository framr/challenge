#!/usr/bin/env python

import sys


def dump_mapping(mapping, geoname, outfilename):

    with open(outfilename, "w") as outfile:
        outfile.write("%s,%s_fid\n" % geoname)

        for key, fid in mapping.iteritems():
            outfile.write("%s,%s\n" % (key, str(fid)))


if __name__ == "__main__":

    infilename = sys.argv[1]
    outfilename = sys.argv[2]

    mapping_country = {}
    mapping_state = {}
    mapping_dma = {}
    with open(infilename) as infile:
        header = infile.readline().strip().split(",")

        country_fid = 0
        state_fid = 0
        dma_fid = 0

        for line in infile:
            geolocation, shows, clicks = line.strip().split(",")
            splitted = geolocation.split(">")
            if len(splitted) >= 1:
                country = splitted[0]
                if country not in mapping_country:
                    mapping_country[country] = country_fid
                    country_fid += 1

            if len(splitted) >= 2:
                state = splitted[1]
                if state not in mapping_state:
                    mapping_state[state] = state_fid
                    state_fid += 1

            if len(splitted) >= 3:
                dma = splitted[2]
                if dma not in mapping_dma:
                    mapping_dma[dma] = dma_fid
                    dma_fid += 1



        dump_mapping(mapping_country, "geo_country", outfilename + "_country")
        dump_mapping(mapping_state, "geo_state", outfilename + "_state")
        dump_mapping(mapping_dma, "geo_dma", outfilename + "_dma")





