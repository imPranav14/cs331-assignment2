#!/usr/bin/env python3

"""
Custom Mininet Topology for the assignment:
 - 4 switches: S1, S2, S3, S4
 - 7 hosts: H1, H2, H3, H4, H5, H6, H7
"""

from mininet.topo import Topo
from mininet.link import TCLink

class AssignmentTopo(Topo):
    def build(self):
        # Create switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Create hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')

        # Connect hosts to S1
        self.addLink(h1, s1)
        self.addLink(h2, s1)

        # Connect host H3 to S2
        self.addLink(h3, s2)

        # Connect hosts H4, H5 to S3
        self.addLink(h4, s3)
        self.addLink(h5, s3)

        # Connect hosts H6, H7 to S4
        self.addLink(h6, s4)
        self.addLink(h7, s4)

        # Connect the switches in a chain: S1 -> S2 -> S3 -> S4
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)

# This dictionary allows you to run the topology with:
#   sudo mn --custom assignment_topo.py --topo assignment
topos = {
    'assignment': (lambda: AssignmentTopo())
}
