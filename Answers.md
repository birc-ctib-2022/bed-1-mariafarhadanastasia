# Questions for bed-1
## How does the method for extracting features work? 
In our case: 
- First the features in the BED-file is processed. The BED-file is split o any kind of white space and put into the format of BedLines (chromosome, chrom_start, chrom_end, name) which is put into a table which contains all the BedLines whith their chromosome as key
- When the BedTable is made it is time to process the query file. For each line in query it is split into chromosome, start and end. 
- For each line in the query-file the BedFiles i the BedTable with the same chromosome as the line in the query-file is assed. For each BedLine on the same chromosome it is investigated if there is a overlap between the line in the query-file and the BedLine. If there is an ovarlap the BedLine is printed as "chrom\tchrom_start\t_chrom_end\tname" to the output
- The end result is a file (or printed to standard-out) with all the features in the BED-file which had an overlap with lines in the query-file

## The complexity of the algorithm
The complexity of the algortihm, as a function of the size of the two input files.
The get a list of chromosomes from a `query.Table` runs in constant time, but it does, take longer to run through all the lines in it. 

There is one function that is called in the main function: `process_query()`. The following is the preview of the function.

    /F
    def process_query(fbed: TextIO, fquery: TextIO, fout:TextIO) -> None:
        """Function to process all files: bed, query, and outfile (if any)."""
        bed_table = get_bed_table(fbed) # O(n)

        # We go through every line in query file
        for line in fquery: # O(m)
            chrom, query_start, query_end = split_query_line(line) # O(1)
            bedlines = bed_table.get_chrom(chrom) # bedlines contains all BedLine with certain "chrom". O(n)
            print_overlap(bedlines, query_start, query_end, fout) # O(n)
        return None
The `get_bed_table()` function runs through all lines in the BED file with length `n`, so its `O(n)`. 

Then we go through every line in query file, let's say with length `m`. There are three functions called inside the loop:
1. `split_query_line()` has `O(1)` complexity since it only split the query line into 3 variable.
2. `get_chrom()` function runs through every line in `bed_table` so it is `O(n)`.
3. Lastly, `print_overlap()`  run through every line in `bedlines` and the worst case complexity is `O(n)`.

To sum up, we got `O(n) + O(m * (1+n+n))` complexity. Or in other word, `O(m*n)`.

## Handle SNP's vs. larger regions
Did you at any point, exploit that our features are on single nucleotides and not larger regions?
If you did, what would it take to handle general regions?

- In the tests we tested for AssertionError when features in BED-files where larger than 1 nucleotide, but this error where our own desicion in the way the program was made. 
- If we were to handle general regions we would have to consider what an overlap is: if the entire feature from the BED-file should be in the region from the query-file or if it is enough that there is a overlap in one end. 

/F
