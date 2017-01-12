#!/usr/bin env python

import sys

if __name__ == "__main__":

    with open(sys.argv[1]) as infile:
        with open(sys.argv[2], "w") as outfile:
            header = infile.readline()
            outfile.write(header)
            for line in infile:
                splitted = line.strip().split(",")
                res = []
                for col_value in splitted:
                    if not col_value:
                        res.append("-1")
                    else:
                        res.append(col_value)

                outfile.write("%s\n" % ",".join(res))
