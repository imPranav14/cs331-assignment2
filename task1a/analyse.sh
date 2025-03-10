#!/bin/bash
for pcap in h7_*.pcap; do
  echo "=== Analyzing $pcap ==="
  
  # Throughput
  echo -n "Throughput (Mbps): "
  tshark -r "$pcap" -Y "tcp.dstport==5201" -T fields -e frame.time_relative -e frame.len \
    | awk 'BEGIN {sum=0} {sum+=$2*8} END {printf "%.2f\n", sum/15/1e6}'

  # Goodput (application-layer data)
  echo -n "Goodput (Mbps): "
  tshark -r "$pcap" -Y "tcp.dstport==5201 && tcp.len>0 && !tcp.analysis.retransmission" -T fields -e tcp.len \
    | awk 'BEGIN {sum=0} {sum+=$1*8} END {printf "%.2f\n", sum/15/1e6}'

  # Packet Loss Rate
  total=$(tshark -r "$pcap" -Y "tcp.dstport==5201" | wc -l)
  lost=$(tshark -r "$pcap" -Y "tcp.analysis.lost_segment" | wc -l)
  echo "Packet Loss Rate: $lost/$total ($(echo "scale=2; $lost*100/($total+1)" | bc)%)"

  # Maximum Window Size
  echo -n "Max Window Size: "
  tshark -r "$pcap" -Y "tcp.dstport==5201" -T fields -e tcp.window_size \
    | sort -n | tail -1 | awk '{print $1 " bytes"}'

  echo "---------------------------------"
done
