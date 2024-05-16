# We are going to be running the "blastdbcmd" program from inside
# python, so we need to import this library
import subprocess

# We also need to import the "random" library so that
# we can choose slices at random
import random

# The "line_length" in blastdbcmd doesn't work *shrug*
import textwrap

# This is the name of the blast database
DBNAME = "panTro7"

# This is the name of the query file that
# we're going to save all our little query slices to
QUERYFILE = "query.fa"

# How many slices do you want to choose from each chromosome?
SLICES = 10

# How big do you want the slice to be?
SLICESIZE = 300

################################################################################

def get_entries():

	# We're going to call "blastdbcmd" to give us a list
	# of all the chromosomes/sequences in the database, as
	# well as their lengths.
	cmd = "blastdbcmd -db {0} -entry all -outfmt \"%i %l\"".format(DBNAME)
	output = subprocess.getoutput(cmd)
	lines = output.splitlines()

	# If you want to see the output, just remove the "#" from the next line
	#print(output)

	# For some silly reason, the output has a blank line at the ends
	# Let's remove it
	lines.pop()

	# Make a dictionary with the chromosome name and the lengths
	e = {}
	for line in lines:
		(chrom, length) = line.split()
		e[chrom] = int(length)

	# Return the entries as a dictionary
	return e

################################################################################

entries = get_entries()
print("There are {0} entries in the {1} database".format(len(entries), DBNAME))

# Open the output query file for writing
qf = open(QUERYFILE, "w")

for chrom in entries.keys():
	sz = entries[chrom]

	print("Getting {0} sequence(s) from {1}".format(SLICES, chrom))

	for counter in range(SLICES):

		# Choose a starting point at random somewhere in the chromosome
		qstart = random.randrange(sz - SLICESIZE)
		qend = qstart + SLICESIZE - 1
		qseqid = "{0}:{1}:{2}".format(chrom, qstart, qend)

		# Get the sequence out of the database
		cmd = "blastdbcmd -db {0} -entry \"{1}\" -range {2}-{3} -outfmt \"%s\"".format(DBNAME, chrom, qstart, qend)
		output = subprocess.getoutput(cmd)
		lines = textwrap.wrap(output, 60)

		# Print the sequence out to the query file
		print(">{0}".format(qseqid), file=qf)
		print("\n".join(lines), file=qf)

print("Sequences written to {0}".format(QUERYFILE))
qf.close()

