#!/usr/bin/env python
#
# Copyright (c) 2012, Regents of the University of California
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
# Count ChIP-seq peaks
#
# by Fernando L. Garcia Bermudez & Yanina S. Bogliotti
#
# created on 2012-5-9
#

import os, sys, time, traceback, numpy as np


def main():

    # Check and parse arguments
    if len(sys.argv) < 2:
        print("Not enough arguments given. Need full path for the data file.")
        sys.exit()

    # Load dataset
    name      = os.path.splitext(sys.argv[1])[0]
    ext       = os.path.splitext(sys.argv[1])[1]
    datafile  = name + ext
    chr_names = list(np.loadtxt(datafile, delimiter=',', comments='#',      \
                                                    usecols=(0,), dtype=str))
    print('\nI: Loaded ChIP-seq peak data from ' + datafile)

    # Count number of peaks for each chromosome
    chr_peak_cnt = {}
    for chr_name in chr_names:
        if chr_name[0] not in ('c', 'G', '"') and not chr_peak_cnt.has_key(chr_name):
            chr_peak_cnt[chr_name] = chr_names.count(chr_name)

    # Save chromosome peak counts to a file
    dt_str          = time.strftime('%Y.%m.%d_%H.%M.%S', time.localtime())
    resultsfile = name + '_peak_cnt_' + dt_str + ext
    outfile = open(resultsfile,'w')
    outfile.write('chr,peak_cnt\n')
    outfile.close()
    np.savetxt(open(resultsfile , 'a'), np.array(chr_peak_cnt.items(), \
                                         dtype='|S10'), '%s', delimiter = ',')
    print('I: Saved chromosome peak counts to ' + resultsfile)

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
