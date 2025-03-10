#!/bin/bash

analyze() {
    pcap=$1
    echo "===== Analysis for ${pcap/_c.pcap/} ====="
    
    # Throughput over time
    echo -e "\nThroughput (Mbps per second):"
    tshark -r $pcap -q -z io,stat,1,"tcp.dstport==5201" | grep -A 20 "5201"
    
    # Goodput calculation
    goodput=$(tshark -r $pcap -Y "tcp.len>0 && !tcp.analysis.retransmission" -T fields -e tcp.len | awk '{sum+=$1} END {print sum*8/1e6}')
    echo -e "\nGoodput: ${goodput:-0} Mbps"
    
    # Packet loss rate
    total=$(tshark -r $pcap -Y "tcp.dstport==5201" | wc -l)
    lost=$(tshark -r $pcap -Y "tcp.analysis.lost_segment" | wc -l)
    echo "Packet Loss: $lost/$total ($(echo "scale=2; $lost*100/($total+1)" | bc)%)"
    
    # Max window size
    echo -n "Max Window: "
    tshark -r $pcap -T fields -e tcp.window_size | sort -n | tail -1
}

analyze condition1_c.pcap
analyze condition2a_c.pcap 
analyze condition2b_c.pcap
analyze condition2c_c.pcap