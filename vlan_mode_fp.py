#!/usr/bin/env python
#
# Copyright (C) 2015 Larksmith Forge LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

'''
This script parses the output of "show vlan brief" and converts the
vlans captured to mode FabricPath

It will convert all active VLANs to mode FabricPath.

It was designed for Nexus Leaf switches (5548) where all VLANs should be mode FP.

To invoke,

1. Copy the script into bootflash:
2. Invoke from exec using "python <scriptname>"

'''


from cli import *
import sys
import re

# Sample Output of the CLI : 

'''

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Eth1/1, Eth1/2, Eth1/3, Eth1/4
                                                Eth1/5, Eth1/6, Eth1/7, Eth1/8
                                                Eth1/9, Eth1/10, Eth1/11
                                                Eth1/12, Eth1/13, Eth1/14
                                                Eth1/15, Eth1/16, Eth1/17
                                                Eth1/18, Eth1/19, Eth1/20
                                                Eth1/21, Eth1/22, Eth1/23
                                                Eth1/24, Eth1/25, Eth1/26
                                                Eth1/27, Eth1/28, Eth1/29
                                                Eth1/30, Eth1/31, Eth1/32
                                                Eth1/33, Eth1/34, Eth1/35
                                                Eth1/36, Eth1/37, Eth1/38
                                                Eth1/39, Eth1/40, Eth1/41
                                                Eth1/42, Eth1/43, Eth1/44
                                                Eth1/45, Eth1/46, Eth1/47
                                                Eth1/48, Eth2/1, Eth2/2, Eth2/3
                                                Eth2/4, Eth2/5, Eth2/6, Eth2/7
                                                Eth2/8, Eth2/9, Eth2/10, Eth2/11
                                                Eth2/12
10   VLAN0010                         active    
11   VLAN0011                         active    
12   VLAN0012                         active    
13   VLAN0013                         active    

'''

cli("install feature-set fabricpath")
cli("feature-set fabricpath")

# Execute the command on the switch

raw_input = cli("show vlan brief | include act")

# Split the output into a list containing each line

all_raw_lines = raw_input.split('\n')

# print all_raw_lines

# The next section removes the header and any useless lines

all_device_lines = []
line_no = 0
for line in all_raw_lines:
    line_no += 1
    if line_no <= 0:
        pass
    else:
        all_device_lines.append(line)

# This removes the last line, which contain the footer - Total Entries
# displayed

for i in range(1):
    all_device_lines.pop();

# This section indexes the list and specifically calls out the vlan ID,
# and breaks up each value in the line by whitespace. 

for idx, line in enumerate(all_device_lines):
	thisline = re.split('\s+',line)
	vlan_id = thisline[0]
# We can now use the data to configure the description on the switch
	cli(' conf ' + ' ; vlan ' + vlan_id + ' ; mode fabricpath ')
#	print line

# cli("show vlan brief | include act")

cli("term length 0")
clip("show vlan | begin Vlan-mode")
cli("term length 50")