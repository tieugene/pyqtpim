#!/usr/bin/env python3
"""
Split monolythic .ics into separate files (one VTODO per file).
Input: <infile.ics> <outdir>
Output: uniq keys and UID
"""
import os
import sys


def split(i_f, o_d: str):
    """Splitting itself
    :param i_f: Opened input file stream
    :param o_d: Output dir path

    1. store header (or skip it)
    2. read from BEGIN:VTODO to END:VTODO
    3. get UID
    4. save with header and footer
    """
    keys = dict()       # uniq keys
    buffer = list()     # tmp VTODO buffer
    keys_local = set()
    in_vtodo = False    # flag that inside VTODO => need fill buffer
    uid = None          # VTODO's UID
    header = list()     # common header
    header.append(i_f.readline())
    header.append(i_f.readline())
    header.append(i_f.readline())
    header.append('BEGIN:VTODO\n')
    footer = ('END:VTODO\n', 'END:VCALENDAR\n')
    for line in i_f:
        if line.startswith('BEGIN:VTODO'):
            in_vtodo = True
            continue
        elif line.startswith('END:VTODO'):
            with open(os.path.join(o_d, f"{uid}ics"), 'wt') as o_f:
                o_f.writelines(header)
                o_f.writelines(buffer)
                o_f.writelines(footer)
                # cleanup
                for k in keys_local:
                    keys[k] = uid
                keys_local.clear()
                buffer.clear()
                uid = None
                in_vtodo = False
        elif in_vtodo:
            buffer.append(line)
            if line.startswith('UID'):
                uid = line[4:]
            k = line.split(':', 1)[0]
            if k not in keys and k not in keys_local:
                keys_local.add(k)
        else:
            pass
    for k, v in keys.items():
        print(f"{k}\t{v}",)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <infile.ics> <outdir>")
    elif not os.path.isfile(sys.argv[1]):
        print(f"Error: {sys.argv[1]} is not file")
    elif not os.path.isdir(sys.argv[2]):
        print(f"Error: {sys.argv[2]} is not dir")
    else:
        with open(sys.argv[1], 'rt') as infile:
            split(infile, sys.argv[2])


if __name__ == '__main__':
    main()
