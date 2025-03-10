#!/bin/bash

analyze() {
    pcap=$1
    echo "===== Analysis: ${pcap/_d.pcap/} ====="
    
    # Throughput
    echo -n "Avg Throughput (Mbps): "
    tshark -r $pcap -Y "tcp.dstport==5201" -T fields -e frame.time_relative -e frame.len 2>/dev/null \
        | awk 'BEGIN {sum=0; start=0} 
               {if(NR==1) start=$1; sum+=$2*8; duration=$1-start} 
               END {printf "%.2f\n", sum/((duration>0?duration:1)*1e6)}'

    # Goodput
    echo -n "Goodput (Mbps): "
    tshark -r $pcap -Y "tcp.len>0 && !tcp.analysis.retransmission" -T fields -e tcp.len 2>/dev/null \
        | awk '{sum+=$1*8} END {printf "%.2f\n", sum/1e6}'

    # Packet Loss
    total=$(tshark -r $pcap -Y "tcp.dstport==5201" 2>/dev/null | wc -l)
    lost=$(tshark -r $pcap -Y "tcp.analysis.lost_segment" 2>/dev/null | wc -l)
    echo "Packet Loss Rate: $(echo "scale=2; $lost*100/($total+1)" | bc)%"

    # Window Size
    echo -n "Max Window: "
    tshark -r $pcap -T fields -e tcp.window_size 2>/dev/null | sort -n | tail -1
}

for loss in 1 5; do
    for cond in condition1 condition2a condition2b condition2c; do
        analyze "${cond}_loss${loss}_d.pcap"
    done
done