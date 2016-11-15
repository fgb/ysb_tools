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
# Filter RNA-seq data using ChIP-seq peaks
#
# by Fernando L. Garcia Bermudez & Yanina S. Bogliotti
#
# created on 2016-2-9
#

import sys, os, traceback, csv


def main():

    # check and parse arguments
    if len(sys.argv) < 4:
        print("Not enough arguments given. Need full paths for the RNA-seq data file, the ChIP-seq data file, and the CSV where you'd like to store the results.")
        sys.exit()

    rna_seq  = sys.argv[1]
    chip_seq = sys.argv[2]
    result   = sys.argv[3]

    # perform filtering
    d = {}
    r = {}

    with open( rna_seq, 'U' ) as dfile:
        dreader = csv.reader( dfile )
        for row in dreader:
            if not d.has_key( row[0] ):
                d[ row[0] ] = [ row[1] ]
            else:
                print( row[0] + ' is repeated!' )
                d[ row[0] ].append( row[1] )

    with open( chip_seq, 'U' ) as lfile, open( result, 'w') as ofile:
        lreader = csv.reader( lfile )
        owriter = csv.writer( ofile )
        for row in lreader:
            if row:
                if d.has_key( row[0] ):
                    r[ row[0] ] = d[ row[0] ]
                else:
                    r[ row[0] ] = ''

                owriter.writerow( [ row[0] ] + r[ row[0] ] )

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
