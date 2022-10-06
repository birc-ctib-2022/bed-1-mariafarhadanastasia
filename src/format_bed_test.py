# This directory will be checked with pytest. It will examine
# all files that start with test_*.py and run all functions with
# names that start with test_

from format_bed import (BedLine ,print_line, parse_line)

import pytest
import sys

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

def test_bedlines_are_printed(capsys):
    """
    Tests whether the lines printed are correct bedlines
    """

    bedline = BedLine(chrom="chr1", chrom_start=20100, chrom_end=20101, name="foo")
    print_line(bedline,sys.stdout)
    out, err = capsys.readouterr()
    assert out == "chr1\t20100\t20101\tfoo\n"
    assert err ==''

    print_line(parse_line('chr1 20100 20101 foo'),sys.stdout)
    out, err = capsys.readouterr()
    assert out == "chr1\t20100\t20101\tfoo\n"
    assert err ==''
