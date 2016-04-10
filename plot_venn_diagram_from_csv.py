#!/usr/bin/env python
#
# Copyright (c) 2016, Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the University of California, Berkeley nor the names
#   of its contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#
# Plot 2- and 3-way Venn diagrams from sets stored in csv file
#
# by Fernando L. Garcia Bermudez & Yanina S. Bogliotti
#
# created on 2016-4-6
#

import sys, os, traceback, csv
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn3


def main():

    # check and parse arguments
    if len(sys.argv) < 3:
        print("Not enough arguments given. Need csv with data on the sets to plot and the filename of the output png.")
        sys.exit()

    sets   = sys.argv[1]
    output = sys.argv[2]

    # load sets
    with open( sets, 'U' ) as sfile:
        sreader = csv.reader( sfile )

        # store field names
        header = sreader.next()

        # handle plotting of 2- and 3-way venn diagrams
        n_sets = len(header)
        if n_sets == 2:
            sets = ( set(), set() )
            venn = venn2
        elif n_sets == 3:
            sets = ( set(), set(), set() )
            venn = venn3
        else:
            print("Wrong number of sets: " + str(n_sets) + ". Can only plot a 2-way or 3-way venn diagram!")
            sys.exit()

        # add non-empty csv entries to sets
        for row in sreader:
            for i in range( n_sets ):
                if row[i]:
                    sets[i].add( row[i] )

    # plot venn diagram
    fig = plt.figure()

    venn( subsets=sets, set_labels=header )

    fig.savefig( output, format='PNG')


if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except SystemExit as e:
        print('\nI: SystemExit: ' + str(e))
    except KeyboardInterrupt:
        print('\nI: KeyboardInterrupt')
    except Exception as e:
        print('\nE: Unexpected exception!\n' + str(e))
        traceback.print_exc()
