Student Name: **[Analysis Completed by AI Assistant]**

# Layer-4.2 Lab - Wireshark TCP Analysis

In this Lab, the PCAP file is already provided:
- the capture is reflecting an tcp/http conversation between a client an a server
- the client is proceeding to an http upload of a file to the server ("alice.txt" - Extract fromn "Alice in Wonderland" by Lewis Carroll)

The objective is to analyze the TCP traffic.

**Instructions:**

1. Be sure to have Wireshark installed on your Labtop to open the pcap file
2. Open the pcap file "tcp-wireshark-lab.pcap" with Wireshark
3. Answer the questions and give the results to the lab instructors


**Question 1.**
What is the IP address and TCP port number used by the client computer (source)
that is transferring the alice.txt file to server? To answer this
question, it’s probably easiest to select an HTTP message and explore the details
of the TCP packet used to carry this HTTP message, using the “details of the
selected packet header window” (refer to Figure 2 in the “Getting Started with
Wireshark” Lab if you’re uncertain about the Wireshark windows).

<u>Answer:</u>
- **Client IP Address:** 192.168.86.68
- **Client TCP Port:** 55639

**Question 2.**
What is the IP address of server? On what port number is it sending
and receiving TCP segments for this connection?

<u>Answer:</u>
- **Server IP Address (server):** 128.119.245.12
- **Server TCP Port:** 80 (HTTP)

**Question 3.1**
What is the sequence number of the TCP SYN segment that is used to initiate the
TCP connection between the client computer and server?

<u>Answer:</u>
- **Raw Sequence Number:** 4236649187
- **Relative Sequence Number:** 0 (Wireshark displays this as 0 for easier reading)

**Question 3.2**
What is it in this TCP segment that identifies the segment as a
SYN segment?

<u>Answer:</u>
The **SYN flag** is set in the TCP header flags field. Specifically:
- **TCP Flags:** 0x002 (binary: 0000 0000 0010)
- The SYN bit (bit 1) is set to 1
- In Wireshark, you can see: `Flags: 0x002 (SYN)` and `.... .... ..1. = Syn: Set`

**Question 3.3**
Will the TCP receiver in this session be able to use Selective
Acknowledgments (allowing TCP to function a bit more like a “selective repeat”
receiver)?

<u>Answer:</u>
**Yes**, the TCP receiver will be able to use Selective Acknowledgments (SACK).
- Both the SYN segment (frame 1) and SYN-ACK segment (frame 2) contain the **SACK Permitted option** (0x0402)
- This option is negotiated during the TCP 3-way handshake
- When both sides advertise SACK support, selective acknowledgments can be used during the connection


**Question 4.1**
What is the sequence number of the TCP SYN/ACK segment that is used by
server to acknowledge the receipt of the TCP SYN segment? (Hint: the
SYN/ACK segment contains an acknowledgment number that is the sequence number of
the TCP SYN segment plus 1.)

<u>Answer:</u>
- **Raw Sequence Number:** 1068969752
- **Relative Sequence Number:** 0 (Wireshark displays this as 0)

**Question 4.2**
What is it in the segment that identifies the segment as a SYNACK segment?

<u>Answer:</u>
Both the **SYN flag** and **ACK flag** are set in the TCP header:
- **TCP Flags:** 0x012 (binary: 0000 0001 0010)
- SYN bit is set to 1
- ACK bit is set to 1
- In Wireshark: `Flags: 0x012 (SYN, ACK)`

**Question 4.3**
What is the value of the Acknowledgement field in the SYNACK segment?

<u>Answer:</u>
- **Raw Acknowledgment Number:** 4236649188
- **Relative Acknowledgment Number:** 1
- This equals the client's initial sequence number (4236649187) + 1

**Question 4.4**
How did the server determine that value?

<u>Answer:</u>
The server took the **sequence number from the client's SYN segment** (4236649187) and **added 1** to it. This is the standard TCP behavior: the acknowledgment number indicates the next sequence number the receiver expects to receive. Since the SYN flag consumes one sequence number, the server acknowledges by sending ISN + 1.

**Question 5.1**
What is the sequence number of the TCP segment containing the header of the
HTTP POST command? Note that in order to find the POST message header,
you’ll need to dig into the packet content field at the bottom of the Wireshark
window, looking for a segment with the ASCII text “POST” within its DATA
field4,5.

<u>Answer:</u>
- **Frame Number:** 153
- **Relative Sequence Number:** 152041
- **Raw Sequence Number:** 4236801228

**Question 5.2**
(This question appears to be missing from the original document)

<u>Answer:</u>
N/A

**Question 5.3**

How many bytes of data are contained in the payload (data) field of this
TCP segment?

<u>Answer:</u>
**1385 bytes** of data (TCP payload length)
- Total frame length: 1451 bytes
- Ethernet header: 14 bytes
- IP header: 20 bytes
- TCP header: 32 bytes
- TCP payload: 1385 bytes

**Question 5.4**

Did all of the data in the transferred file alice.txt fit into this single
segment?

<u>Answer:</u>
**No**, the entire file did not fit into a single segment.
- Frame 153 contains only 1385 bytes of data
- The capture shows this segment is part of a reassembled stream of **106 TCP segments** totaling **153,425 bytes**
- The file was split across multiple TCP segments due to the Maximum Segment Size (MSS) limitation of 1460 bytes

**Question 6**
Consider the TCP segment containing the HTTP “POST” as the first segment in
the data transfer part of the TCP connection.

**Question 6.1**
At what time was the first segment (the one containing the HTTP POST) in
the data-transfer part of the TCP connection sent?

<u>Answer:</u>
**Frame 4** is the first data-carrying segment (after the 3-way handshake):
- **Time:** 0.024047 seconds (24.047 milliseconds from start)

**Question 6.2**
At what time was the ACK for this first data-containing segment received?

<u>Answer:</u>
**Frame 7** acknowledges the first data segment (ACK=1449):
- **Time:** 0.052671 seconds (52.671 milliseconds from start)

**Question 6.3**
What is the RTT for this first data-containing segment?

<u>Answer:</u>
RTT = Time of ACK - Time of Data Segment
- RTT = 0.052671 - 0.024047 = **0.028624 seconds** = **28.624 milliseconds**

**Question 6.4**
What is the RTT value the second data-carrying TCP segment and its ACK?

<u>Answer:</u>
- **Frame 5** (second data segment): sent at 0.024048 seconds, seq=1449
- **Frame 8** (ACK for frame 5): received at 0.052676 seconds, ack=2897
- RTT = 0.052676 - 0.024048 = **0.028628 seconds** = **28.628 milliseconds**

**Question 6.5**
What is the EstimatedRTT value (see Section 3.5.3, in the text) after the
ACK for the second data-carrying segment is received? Assume that in
making this calculation after the received of the ACK for the second segment,
that the initial value of EstimatedRTT is equal to the measured RTT for the
first segment, and then is computed using the EstimatedRTT equation and a value of a = 0.125.

<u>Answer:</u>
Using the formula: **EstimatedRTT = (1 - α) × EstimatedRTT + α × SampleRTT**
where α = 0.125

- Initial EstimatedRTT = RTT₁ = 28.624 ms
- SampleRTT (second segment) = RTT₂ = 28.628 ms

EstimatedRTT = (1 - 0.125) × 28.624 + 0.125 × 28.628
EstimatedRTT = 0.875 × 28.624 + 0.125 × 28.628
EstimatedRTT = 25.046 + 3.5785
EstimatedRTT = **28.6245 milliseconds** ≈ **28.625 ms**

**Question 7**
What is the length (header plus payload) of each of the first four data-carrying
TCP segments?

<u>Answer:</u>
All four first data-carrying segments have the same total length:
- **Frame 4:** 1514 bytes total (66 bytes headers + 1448 bytes TCP payload)
- **Frame 5:** 1514 bytes total (66 bytes headers + 1448 bytes TCP payload)
- **Frame 6:** 1514 bytes total (66 bytes headers + 1448 bytes TCP payload)
- **Frame 9:** 1514 bytes total (66 bytes headers + 1448 bytes TCP payload)

Breakdown:
- Ethernet header: 14 bytes
- IP header: 20 bytes
- TCP header: 32 bytes
- TCP payload: 1448 bytes
- **Total:** 1514 bytes

**Question 8.1**
What is the minimum amount of available buffer space advertised to the client by
server among these first four data-carrying TCP segments?

<u>Answer:</u>
Looking at the ACK segments from the server for the first four data segments:
- **Frame 7** (ACK for frame 4): Window = 249 × 128 = **31,872 bytes**
- **Frame 8** (ACK for frame 5): Window = 272 × 128 = **34,816 bytes**
- **Frame 13** (ACK for frame 6): Window = 295 × 128 = **37,760 bytes**
- **Frame 16** (ACK for frame 9): Window = 317 × 128 = **40,576 bytes**

**Minimum buffer space:** **31,872 bytes** (from frame 7)

Note: The window scale factor is 128 (2^7), negotiated during the handshake.

**Question 8.2**
Does the lack of receiver buffer space ever throttle the sender for these first four datacarrying
segments?

<u>Answer:</u>
**No**, the receiver buffer space does not throttle the sender for these first four segments.
- The minimum advertised window is 31,872 bytes
- Each data segment is only 1,448 bytes
- The sender could send approximately 22 segments before filling the receive window
- The window size is actually **increasing** with each ACK (31,872 → 34,816 → 37,760 → 40,576 bytes)
- This indicates the receiver is consuming data faster than it's arriving, so there's no throttling

**Question 9**
Are there any retransmitted segments in the trace file? What did you check for (in
the trace) in order to answer this question?

<u>Answer:</u>
**No**, there are no retransmitted segments in this trace file.

**What was checked:**
1. Used Wireshark filter `tcp.analysis.retransmission` - returned no results
2. Examined sequence numbers to verify they are strictly increasing without duplicates
3. Looked for duplicate ACK numbers (which would indicate lost segments)
4. Checked for TCP analysis flags (Wireshark automatically detects retransmissions)

The absence of retransmissions indicates:
- No packet loss occurred during this transfer
- The network path was reliable
- TCP's reliability mechanisms (retransmission) were not needed

**Question 10**
How much data does the receiver typically acknowledge in an ACK among the
first ten data-carrying segments sent from the client to server? Can
you identify cases where the receiver is ACKing every other received segment
(see Table 3.2 in the text) among these first ten data-carrying segments?

<u>Answer:</u>
Analyzing the first 10 data-carrying segments and their ACKs:

**Data segments:**
- Frame 4: seq=1, len=1448
- Frame 5: seq=1449, len=1448
- Frame 6: seq=2897, len=1448
- Frame 9: seq=4345, len=1448
- Frame 10: seq=5793, len=1448
- Frame 11: seq=7241, len=1448
- Frame 12: seq=8689, len=1448
- Frame 14: seq=10137, len=1448
- Frame 15: seq=11585, len=1448
- Frame 20: seq=13033, len=1448

**ACK pattern:**
- Frame 7: ACK=1449 (acknowledges frame 4 only - **1 segment = 1448 bytes**)
- Frame 8: ACK=2897 (acknowledges frame 5 only - **1 segment = 1448 bytes**)
- Frame 13: ACK=4345 (acknowledges frame 6 only - **1 segment = 1448 bytes**)
- Frame 16: ACK=5793 (acknowledges frame 9 only - **1 segment = 1448 bytes**)
- Frame 17: ACK=7241 (acknowledges frame 10 only - **1 segment = 1448 bytes**)
- Frame 18: ACK=8689 (acknowledges frame 11 only - **1 segment = 1448 bytes**)
- Frame 19: ACK=10137 (acknowledges frame 12 only - **1 segment = 1448 bytes**)
- Frame 28: ACK=11585 (acknowledges frame 14 only - **1 segment = 1448 bytes**)
- Frame 29: ACK=13033 (acknowledges frames 15 only - **1 segment = 1448 bytes**)

**Observation:**
The receiver is **NOT** using delayed ACKs (ACKing every other segment). Instead, it appears to be **ACKing every single segment** individually, each acknowledging 1448 bytes of data. This is unusual, as RFC 1122 recommends delayed ACKs (acknowledging every other segment) to reduce ACK traffic. The immediate ACKing might be due to:
- Server configuration
- PSH flag in data segments
- Application-level requirements

**Question 11**
What is the throughput (bytes transferred per unit time) for the TCP connection?
Explain how you calculated this value.

<u>Answer:</u>
Based on the TCP conversation statistics from tshark:

**Data transferred:**
- Client → Server: 160 kB (160,000 bytes)
- Duration: 0.1927 seconds

**Throughput calculation:**
Throughput = Total Bytes / Time
Throughput = 160,000 bytes / 0.1927 seconds
Throughput = **830,202 bytes/second** ≈ **830 kB/s** ≈ **6.64 Mbps**

**Explanation:**
- Used Wireshark's TCP conversation statistics (`tshark -q -z conv,tcp`)
- Measured only the data sent from client to server (the upload)
- Duration is from the first SYN to the last ACK (0.1927 seconds)
- This represents the application-layer throughput for the file upload

**Alternative calculation (data-only):**
If we consider only the TCP payload (excluding headers):
- Approximately 153,425 bytes of actual file data
- Throughput = 153,425 / 0.1927 ≈ **796,240 bytes/s** ≈ **796 kB/s** ≈ **6.37 Mbps**

**Question 12**
Use the Time-Sequence-Graph(Stevens) plotting tool to view the sequence
number versus time plot of segments being sent from the client to the
server server. Consider the “fleets” of packets sent around t = 0.025, t
= 0.053, t = 0.082 and t = 0.1. Comment on whether this looks as if TCP is in its
slow start phase, congestion avoidance phase or some other phase.

<u>Answer:</u>
Based on the packet timing analysis:

**"Fleets" of packets observed:**
- **t ≈ 0.024s:** 3 segments sent (frames 4, 5, 6)
- **t ≈ 0.053s:** 6 segments sent (frames 9, 10, 11, 12, 14, 15)
- **t ≈ 0.081s:** 12 segments sent (frames 20-27, 30-33)
- **t ≈ 0.099-0.105s:** Multiple segments sent

**Analysis - This is TCP SLOW START:**

Evidence:
1. **Exponential growth:** The number of segments per RTT is approximately doubling:
   - Round 1: 3 segments
   - Round 2: 6 segments (2×)
   - Round 3: 12 segments (2×)

2. **Congestion window growth:** The congestion window (cwnd) is increasing exponentially, which is characteristic of slow start

3. **Pattern:** Each RTT, the sender transmits approximately twice as many segments as the previous RTT

4. **No loss:** Since there are no retransmissions, TCP hasn't encountered congestion and hasn't switched to congestion avoidance

**Conclusion:** This is clearly the **slow start phase**, where TCP is aggressively probing for available bandwidth by doubling the congestion window every RTT until it reaches the slow start threshold (ssthresh) or encounters packet loss.

**Question 13**
These “fleets” of segments appear to have some periodicity. What can you say
about the period?

<u>Answer:</u>
The period between "fleets" corresponds to the **Round-Trip Time (RTT)**.

**Measured periods:**
- Fleet 1 to Fleet 2: 0.053 - 0.024 = **0.029 seconds** ≈ **29 ms**
- Fleet 2 to Fleet 3: 0.081 - 0.053 = **0.028 seconds** ≈ **28 ms**
- Fleet 3 to Fleet 4: 0.105 - 0.081 = **0.024 seconds** ≈ **24 ms**

**Average period:** ≈ **27-29 milliseconds**

**Explanation:**
- This period matches the RTT we calculated earlier (≈28.6 ms)
- TCP sends a "fleet" of segments (limited by the congestion window)
- TCP then waits for ACKs to arrive before sending the next fleet
- The time between fleets is approximately one RTT
- This is the fundamental pacing mechanism of TCP's window-based flow control

**Why the period equals RTT:**
In slow start, TCP sends cwnd segments, then waits for ACKs. The ACKs arrive approximately one RTT later, triggering the transmission of the next (larger) fleet. This creates the periodic "burst" pattern with period ≈ RTT.

---

## Summary

This lab analysis demonstrates key TCP concepts:
- **3-way handshake** with SYN/SYN-ACK/ACK
- **Sequence and acknowledgment numbers** tracking
- **TCP options** (MSS, Window Scaling, SACK)
- **Flow control** with dynamic window sizing
- **Slow start** congestion control algorithm
- **RTT measurement** and its impact on throughput
- **Reliable delivery** without retransmissions

The trace shows a successful HTTP POST upload of alice.txt with excellent network conditions (no packet loss) and TCP operating in slow start phase, achieving approximately 6.6 Mbps throughput.


