dfrom mininet.topo import Topo
from mininet.link import TCLink

class AssignmentTopoD(Topo):
    def __init__(self, loss=0):
        Topo.__init__(self)
        # Create switches
        s1, s2, s3, s4 = [self.addSwitch(f's{i}') for i in range(1,5)]
        
        # Create hosts
        hosts = [self.addHost(f'h{i}') for i in range(1,8)]
        
        # Connect hosts to switches
        self.addLink(hosts[0], s1)  # H1
        self.addLink(hosts[1], s1)  # H2
        self.addLink(hosts[2], s2)  # H3
        self.addLink(hosts[3], s3)  # H4
        self.addLink(hosts[4], s3)  # H5
        self.addLink(hosts[5], s4)  # H6
        self.addLink(hosts[6], s4)  # H7

        # Configure switch links with loss
        self.addLink(s1, s2, cls=TCLink, bw=100)        # S1-S2: 100Mbps
        self.addLink(s2, s3, cls=TCLink, bw=50, loss=loss)  # S2-S3: 50Mbps + loss
        self.addLink(s3, s4, cls=TCLink, bw=100)        # S3-S4: 100Mbps

topos = {'assignment_d': (lambda loss=0: AssignmentTopoD(loss))}
