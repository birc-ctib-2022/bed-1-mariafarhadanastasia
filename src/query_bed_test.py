# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_

from query_bed import (BedLine, 
parse_line, 
print_line, 
Table, 
get_bed_table, 
is_overlapping, 
split_query_line, 
process_query)

def test_overlapping_lines():
    assert is_overlapping(0,100,4,5)
    assert not is_overlapping(0, 100, 99, 104)
    assert not is_overlapping(50, 100, 45, 51) 
    assert not is_overlapping(0,50,200,201)
    assert not is_overlapping(0,50,50,100)
    assert not is_overlapping(50,100,49,50)

def test_split_query_line():
    """
    Split_query_line should be able to split query lines on whitespace
    It should be able to handle any type of whitespace
    Should be able to handle any string representation of base 10 integers
    """
    assert split_query_line("chrom5 841 842") == ('chrom5', 841, 842)
    assert split_query_line("chrom5 84100 84_200") == ('chrom5', 84100, 84200)
    assert split_query_line("chrom5\n841\t842") == ('chrom5', 841, 842)
