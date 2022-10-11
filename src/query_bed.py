"""Tool for cleaning up a BED file."""

import argparse  # we use this module for option parsing. See main for details.

from typing import TextIO, Tuple
import sys
from bed import (
    BedLine, parse_line, print_line
)
from query import Table

def get_bed_table(infile: TextIO) -> Table:
    """
    Get and insert the bed file into a 'Table'.
    """
    # Open and insert every line in BED file into 'bed_table' table.
    bed_table = Table()
    for line in infile:
        bed_table.add_line(parse_line(line))
    return bed_table

def is_overlapping(query_lower: int, query_upper: int, feature_start: int, feature_end: int) -> bool:
    """
    This function wants to check whether the feature in our BED file is within the query range or not.
    >> query_lower - [feature_start:feature_end] - query_upper
    > query_lower: Start index of query.
    > query_upper: Last index of query.
    > feature_start: Start index of a feature
    > feature_end: Last index of a feature

    >>> is_overlapping(0, 100, 2, 3)
    True
    >>> is_overlapping(0, 5, 2, 6)
    False
    """
    if query_lower <= feature_start and query_upper >= feature_end:
        return True 
    else:
        return False

def split_query_line(line: str) -> Tuple[str, int, int]:
    """
    Split a line that have chromosome, query start index, and query
    last index information.
    
    >>> split_query_line("chrom5  841     900")
    ('chrom5', 841, 900)

    >>> split_query_line("xx  0     1")
    ('xx', 0, 1)
    """
    chrom, start, end = line.split()
    return chrom, int(start), int(end)

def print_overlap(bedlines: Table, query_lower: int, query_upper: int, output: TextIO) -> None:
    """
    Print every BedLine to outfile or stdout that overlaps with given range of query.
    BedLines only contains all BedLine with certain "chrom"
    """
    for i in range(0, len(bedlines)):
        feature_start = bedlines[i].chrom_start
        feature_end = bedlines[i].chrom_end
        if is_overlapping(query_lower, query_upper, feature_start, feature_end):
            print_line(bedlines[i], output)
    return None

def process_query(fbed: TextIO, fquery: TextIO, fout:TextIO) -> None:
    """Function to process all files: bed, query, and outfile (if any)."""
    bed_table = get_bed_table(fbed)

    for line in fquery:
        chrom, query_start, query_end = split_query_line(line)
        bedlines = bed_table.get_chrom(chrom) # bedlines contains all BedLine with certain "chrom"
        print_overlap(bedlines, query_start, query_end, fout)
    return None

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
    
    # Call process_query() function
    process_query(args.bed, args.query, args.outfile)

if __name__ == '__main__':
    main()
