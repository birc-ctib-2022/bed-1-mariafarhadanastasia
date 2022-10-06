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
    > query_lower:
    > query_upper:
    > feature_start:
    > feature_end:

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
    >>> split_query_line("chrom5  841     842")
    ('chrom5', 841, 842)
    """
    chrom, start, end = line.split()
    return chrom, int(start), int(end)


def process_query(fbed: TextIO, fquery: TextIO, fout:TextIO) -> None:
    """
    """
    bed_table = get_bed_table(fbed)

    for line in fquery:
        chrom, query_start, query_end = split_query_line(line)
        bedline = bed_table.get_chrom(chrom)

        for i in range(0, len(bedline)):
                if is_overlapping(query_start, query_end, bedline[i].chrom_start, bedline[i].chrom_end):
                    print_line(bedline[i], fout)
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
