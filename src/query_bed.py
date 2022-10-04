"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

import sys
from bed import (
    BedLine, parse_line, print_line
)
from query import Table


def main() -> None:
    """Run the program."""
    # Setting up the option parsing using the argparse module
    argparser = argparse.ArgumentParser(
        description="Extract regions from a BED file")
    argparser.add_argument('bed', type=argparse.FileType('r'))
    argparser.add_argument('query', type=argparse.FileType('r'))

    # 'outfile' is either provided as a file name or we use stdout
    argparser.add_argument('-o', '--outfile',  # use an option to specify this
                           metavar='output',  # name used in help text
                           type=argparse.FileType('w'),  # file for writing
                           default=sys.stdout)

    # Parse options and put them in the table args
    args = argparser.parse_args()

    # With all the options handled, we just need to do the real work
    # FIXME: put your code here

    # Define and open output_file. 
    # We will print our query inside this file. 
    with open(args.outfile.name) as output_file:

        # Open and insert every line in BED file into 'bed_table' table.
        with open(args.bed.name) as file:
            bed_table = Table() # Create a Table object.
            line = file.readline() # Read one line in the BED file.
            while line: # Run this loop while we still have a line to read in BED file.
                bed_table.add_line(parse_line(line)) # Add the line to our 'bed_table' object.
                line = file.readline() # Read the next line.

        # Open the file we want to query.
        with open(args.query.name) as file:
            line = file.readline() # Read one line in the query file.
            while line: # Run this loop while we still have a line to read in query file.
                chrom, start, end = line.split() # Get chrom, chrom_start, chrom_end in query file.
                # Get every line in 'bed_table' that have the same chromosome 
                # in the line of query we currently read
                bedline = bed_table.get_chrom(chrom)
                # Check every line in 'bed_table' that overlaps with our query.
                # Then print the overlapping line to our output_file using print_line().
                for i in range(0,len(bedline)):
                    if bedline[i].chrom_start >= int(start) and bedline[i].chrom_end <= int(end):
                        print_line(bedline[i], output_file)
                line = file.readline() # Read the next line.

if __name__ == '__main__':
    main()
