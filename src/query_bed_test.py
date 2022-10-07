# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_


from io import StringIO
import pytest
import sys

from query_bed import (BedLine, 
parse_line, 
get_bed_table, 
is_overlapping, process_query, 
split_query_line)

def test_works_with_different_bedlines():
    """
    The function should work with different string representations of int in base 10
    And it should work with different white spaces
    """
    expected = BedLine('chr1', 20100, 20101, 'foo')
    assert parse_line('chr1 20_100 20_101 foo') == expected
    assert parse_line('chr1 20100     20101         foo') == expected
    assert parse_line('chr1 20100\t20101\nfoo') == expected

def test_error_if_wrong_line():
    """
    And ValueError should be raised with a line with to many or to few columns is parsed
    And AssertionError should be raised if the interval is not a single nucleotide
    """
    line_with_less_columns = 'chr1 20100 20101'
    line_with_more_columns = 'chr1 20100 20101 foo 10'
    line_with_interval_not_SNP = 'chr1 20100 20201 foo'
    with pytest.raises(ValueError):
        parse_line(line_with_less_columns)
    with pytest.raises(ValueError):
        parse_line(line_with_more_columns)
    with pytest.raises(AssertionError):
        parse_line(line_with_interval_not_SNP) 

def test_correct_tables():
    """
    Tests whether the correct table is made parsing BED-files to get_bed_table
    """
    bed = StringIO("chrom1 201 202 foo\nchrom1 304 305 bar\nchrom1 20100 20101 bas\nchrom7 207 208 qux\nchrom20 506 507 qax")
    bedtable = get_bed_table(bed)
    assert bedtable.get_chrom("chrom1") == [BedLine("chrom1", 201, 202, "foo"), BedLine("chrom1", 304, 305, "bar"), BedLine("chrom1", 20100, 20101, "bas")]
    assert bedtable.get_chrom("chrom7") == [BedLine("chrom7", 207, 208, "qux")]
    assert bedtable.get_chrom("chrom20") == [BedLine("chrom20", 506, 507, "qax")]

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

def test_find_overlaps_between_bed_and_query(capsys):
    """
    When looking into a BEDfile and a query-file the features in the BED-file overlapping
    with the features i the query-file should be printed
    """

    process_query(StringIO("chrom1 201 202 Feature01\n chrom1 203 204 Feature02"), StringIO("chrom1 1 400"), sys.stdout)
    out, err = capsys.readouterr()
    assert out == "chrom1\t201\t202\tFeature01\nchrom1\t203\t204\tFeature02\n"
    assert err == ''

    process_query(StringIO("chrom1 201 202 Feature01\n chrom1 203 204 Feature02\nchrom8 404 405 Feature03"), StringIO("chrom1 1 400\nchrom8 400 450"), sys.stdout)
    out, err = capsys.readouterr()
    assert out == "chrom1\t201\t202\tFeature01\nchrom1\t203\t204\tFeature02\nchrom8\t404\t405\tFeature03\n"
    assert err == ''

def test_no_overlaps_between_bed_and_query(capsys):
   """
   If no overlaps exist '' is printed but no error
   """
   process_query(StringIO("chrom1 201 202 Feature01\n chrom1 203 204 Feature02"), StringIO("chrom1 1 10"), sys.stdout)
   out, err = capsys.readouterr()
   assert out == ''
   assert err == ''

    
