#! /usr/bin/env python

from __future__ import print_function

import argparse
from cmath import inf
import os
import re

from pyulog.utils.euler import addEulerAngles

from pyulog import ULog
from hdf5storage import savemat

#pylint: disable=too-many-locals, invalid-name, consider-using-enumerate

def main():
    """Command line interface"""

    parser = argparse.ArgumentParser(description='Convert ULog to MAT')
    parser.add_argument('filename', metavar='file.ulg', help='ULog input file')

    parser.add_argument(
        '-m', '--messages', dest='messages',
        help=("Only consider given messages. Must be a comma-separated list of"
              " names, like 'sensor_combined,vehicle_gps_position'"))


    parser.add_argument('-o', '--output', dest='output', action='store',
                        help='Output directory (default is same as input file)',
                        metavar='DIR')
    parser.add_argument('-i', '--ignore', dest='ignore', action='store_true',
                        help='Ignore string parsing exceptions', default=False)

    args = parser.parse_args()

    if args.output and not os.path.isdir(args.output):
        print('Creating output directory {:}'.format(args.output))
        os.mkdir(args.output)

    convert_ulog2mat(args.filename, args.messages, args.output, args.ignore)


def convert_ulog2mat(ulog_file_name, messages, output, disable_str_exceptions=False):
    """
    Coverts and ULog file to a MATLAB file.

    :param ulog_file_name: The ULog filename to open and read
    :param messages: A list of message names
    :param output: Output file path

    :return: None
    """

    msg_filter = messages.split(',') if messages else None

    ulog = ULog(ulog_file_name, msg_filter, disable_str_exceptions)
    data = ulog.data_list

    output_file_prefix = ulog_file_name
    # strip '.ulg'
    if output_file_prefix.lower().endswith('.ulg'):
        output_file_prefix = output_file_prefix[:-4]

    # write to different output path?
    if output:
        base_name = os.path.basename(output_file_prefix)
        output_file_prefix = os.path.join(output, base_name)

    os.path.join(output_file_prefix, ".mat")

    matdata = {
        "data": {}
    }

    # Find the minimum timestamp for time shifting
    min_timestamp = inf

    for d in data:
        if d.name == 'parameter_update' or d.name == 'event':
            continue

        min_timestamp = min(min_timestamp, min(d.data['timestamp']))

    for d in data:
        fmt = '{0}_{1}'
        structname = fmt.format(d.name, d.multi_id)

        matdata['data'][structname] = {}

        for key, value in d.data.items():
            # Remove special characters
            newkey = re.sub('[^a-zA-Z0-9 \n\.]', '', key)
            matdata['data'][structname][newkey] = value

            # Add time-shifted data in seconds
            if newkey == 'timestamp':
                matdata['data'][structname]['timestamp_shifted_sec'] = (value - min_timestamp) / 1e6


    savemat(output_file_prefix, matdata)