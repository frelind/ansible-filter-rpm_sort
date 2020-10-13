#!/usr/libexec/platform-python -tt
# -*- coding: utf-8 -*-

# rpmdev-sort -- sort rpms from standard input
#
# Copyright (c) 2010 Dan Horak
#               2010-2013 Ville Skyttä
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import re
import sys

import rpm


def usage():
    print("""
rpmdev-sort # with no arguments, processes standard input

Sort the package list given on standard input, one per line.
Empty and commented out lines are ignored, comment character is #.
Supported formats:
    Name-Version-Release
    Epoch:Name-Version-Release
    Name-Epoch:Version-Release
""")

EPOCH_RE = re.compile(r"^(\d+):")


def parse_nevr(s):
    ss = s.split('-')
    while (len(ss) < 3):
        ss.append("")
    r = ss.pop()
    v = ss.pop()
    e = ""

    m = EPOCH_RE.search(v)
    if m:  # N-E:V-R
        e = m.group(1)
        v = v[len(m.group(0)):]
    else:
        m = EPOCH_RE.search(ss[0])
        if m:  # E:N-V-R
            e = m.group(1)
            ss[0] = ss[0][len(m.group(0)):]

    return ("-".join(ss), e, v, r)


class NevrLine(object):
    line = None
    n = None
    e = None
    v = None
    r = None

    def __init__(self, line):
        self.line = line
        self.n, self.e, self.v, self.r = parse_nevr(line)

    def __cmp__(self, other):
        if self.n > other.n:
            return 1
        elif self.n < other.n:
            return -1
        return rpm.labelCompare((self.e, self.v, self.r),
                                (other.e, other.v, other.r))

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __repr__(self):
        return self.line


class FilterModule(object):
    def filters(self):
        return {'rpm_sort': self.rpm_sort}

    def rpm_sort(self, pkg_list):
        if isinstance(pkg_list, str):
            pkg_list = pkg_list.splitlines()

        lines = []
        for line in pkg_list:
            if len(line) == 0:
                break
            line = line.strip()
            if len(line) and not line.startswith("#"):
                lines.append(NevrLine(line))
        lines.sort()
        return lines
