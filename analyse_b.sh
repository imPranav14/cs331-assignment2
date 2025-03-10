#!/bin/bash
declare -A HOST_IPS=(
    ['h1']='10.0.0.1'
    ['h3']='10.0.0.3' 
    ['h4']='10.0.0.4'
)

analyze_pcap() {
    local pcap=$1
    local cong=$2
    
    echo -e "\n===== Analysis for $cong ====="
    
    if [ ! -f "$pcap" ]; then
        echo "ERROR: $pcap not found!"
        return 1
    fi
    
    for host in h1 h3 h4; do
        ip=${HOST_IPS[$host]}
        echo -e "\nFlow: $host -> h7 ($ip)"
        
        # Throughput calculation
        echo -n "Avg Throughput (Mbps): "
        tshark -r "$pcap" -Y "ip.src==$ip && tcp.dstport==5201" -T fields -e frame.time_relative -e frame.len 2>/dev/null \
            | awk 'BEGIN {sum=0; start=0} 
                   {if(NR==1) start=$1; sum+=$2*8; duration=$1-start} 
                   END {if(duration>0) printf "%.2f\n", sum/(duration*1e6); else print "0"}'

        # Goodput calculation
        echo -n "Goodput (Mbps): "
        tshark -r "$pcap" -Y "ip.src==$ip && tcp.dstport==5201 && tcp.len>0 && !tcp.analysis.retransmission" -T fields -e tcp.len 2>/dev/null \
            | awk '{sum+=$1*8} END {printf "%.2f\n", sum/1e6}'

        # Packet loss
        total=$(tshark -r "$pcap" -Y "ip.src==$ip && tcp.dstport==5201" 2>/dev/null | wc -l)
        lost=$(tshark -r "$pcap" -Y "ip.src==$ip && tcp.analysis.lost_segment" 2>/dev/null | wc -l)
        echo "Packet Loss: $lost/$total ($(echo "scale=2; $lost*100/($total+1)" | bc)%)"

        # Window size
        echo -n "Max Window: "
        tshark -r "$pcap" -Y "ip.src==$ip && tcp.dstport==5201" -T fields -e tcp.window_size 2>/dev/null \
            | sort -n | tail -1 | awk '{print $1 " bytes"}'
    done
}

for cong in cubic westwood scalable; do
    analyze_pcap "h7_${cong}.pcap" "$cong"
done