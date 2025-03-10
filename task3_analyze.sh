#!/bin/bash

analyze() {
    pcap=$1
    config=$2
    echo -e "\n===== Analysis: $config ====="
    
    # Validate pcap file
    if [ ! -f "$pcap" ]; then
        echo "ERROR: File $pcap not found!"
        return 1
    fi

    # Get capture duration
    duration=$(capinfos "$pcap" | grep 'Capture duration' | awk '{print $3}')
    if (( $(echo "$duration < 100" | bc -l) )); then
        echo "WARNING: Short capture duration ($duration seconds)"
    fi

    # Throughput calculation
    throughput=$(tshark -r "$pcap" -Y "tcp.dstport==5201 && tcp.len>0" -T fields -e frame.time_relative -e frame.len 2>/dev/null |
        awk -v dur="$duration" 'BEGIN {sum=0} 
            {sum += $2*8} 
            END {if (dur > 0) printf "%.8f", sum/(dur*1e6); else print "0"}')

    # Goodput calculation
    goodput=$(tshark -r "$pcap" -Y "tcp.len>0 && !tcp.analysis.retransmission" -T fields -e tcp.len 2>/dev/null |
        awk 'BEGIN {sum=0} {sum += $1*8} END {printf "%.8f", sum/1e6}')

    # Packet loss
    total_packets=$(tshark -r "$pcap" -Y "tcp.dstport==5201 && tcp.len>0" 2>/dev/null | wc -l)
    lost_packets=$(tshark -r "$pcap" -Y "tcp.analysis.retransmission" 2>/dev/null | wc -l)
    loss_rate=$(echo "scale=4; $lost_packets*100/($total_packets+1)" | bc -l)

    # Max TCP payload size (data only)
    max_payload=$(tshark -r "$pcap" -Y "tcp.dstport==5201 && tcp.len>0" -T fields -e tcp.len 2>/dev/null | sort -n | tail -1)
    max_payload=${max_payload:-0}

    # Max frame size (for reference)
    max_frame=$(tshark -r "$pcap" -Y "tcp.dstport==5201 && tcp.len>0" -T fields -e frame.len 2>/dev/null | sort -n | tail -1)
    max_frame=${max_frame:-0}

    echo "Throughput: ${throughput:-0} Mbps"
    echo "Goodput: ${goodput:-0} Mbps"
    echo "Packet Loss Rate: ${loss_rate:-0}%"
    echo "Max TCP Payload: ${max_payload} bytes"
    echo "Max Frame Size: ${max_frame} bytes"
}

analyze test3_1.pcap "Nagle ON, Delayed-ACK ON"
analyze test3_2.pcap "Nagle ON, Delayed-ACK OFF"
analyze test3_3.pcap "Nagle OFF, Delayed-ACK ON"
analyze test3_4.pcap "Nagle OFF, Delayed-ACK OFF"