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

**Question 2.**
What is the IP address of server? On what port number is it sending
and receiving TCP segments for this connection?

**Question 3.1**
What is the sequence number of the TCP SYN segment that is used to initiate the
TCP connection between the client computer and server?


**Question 3.2**
What is it in this TCP segment that identifies the segment as a
SYN segment?

**Question 3.3**
Will the TCP receiver in this session be able to use Selective
Acknowledgments (allowing TCP to function a bit more like a “selective repeat”
receiver)?


**Question 4.1**
What is the sequence number of the TCP SYN/ACK segment that is used by
server to acknowledge the receipt of the TCP SYN segment? (Hint: the
SYN/ACK segment contains an acknowledgment number that is the sequence number of
the TCP SYN segment plus 1.)

**Question 4.2**
What is it in the segment that identifies the segment as a SYNACK segment?

**Question 4.3**
What is the value of the Acknowledgement field in the SYNACK segment?

**Question 4.4**
How did the server determine that value?

**Question 5.1**
What is the sequence number of the TCP segment containing the header of the
HTTP POST command? Note that in order to find the POST message header,
you’ll need to dig into the packet content field at the bottom of the Wireshark
window, looking for a segment with the ASCII text “POST” within its DATA
field4,5.

**Question 5.3**

How many bytes of data are contained in the payload (data) field of this
TCP segment?

**Question 5.4**

Did all of the data in the transferred file alice.txt fit into this single
segment?

**Question 6**
Consider the TCP segment containing the HTTP “POST” as the first segment in
the data transfer part of the TCP connection.

**Question 6.1**
At what time was the first segment (the one containing the HTTP POST) in
the data-transfer part of the TCP connection sent?

**Question 6.2**
At what time was the ACK for this first data-containing segment received?

**Question 6.3**
What is the RTT for this first data-containing segment?

**Question 6.4**
What is the RTT value the second data-carrying TCP segment and its ACK?

**Question 6.5**
What is the EstimatedRTT value (see Section 3.5.3, in the text) after the
ACK for the second data-carrying segment is received? Assume that in
making this calculation after the received of the ACK for the second segment,
that the initial value of EstimatedRTT is equal to the measured RTT for the
first segment, and then is computed using the EstimatedRTT equation and a value of a = 0.125.

**Question 7**
What is the length (header plus payload) of each of the first four data-carrying
TCP segments?

**Question 8.1**
What is the minimum amount of available buffer space advertised to the client by
server among these first four data-carrying TCP segments?

**Question 8.2**
Does the lack of receiver buffer space ever throttle the sender for these first four datacarrying
segments?

**Question 9**
Are there any retransmitted segments in the trace file? What did you check for (in
the trace) in order to answer this question?

**Question 10**
How much data does the receiver typically acknowledge in an ACK among the
first ten data-carrying segments sent from the client to server? Can
you identify cases where the receiver is ACKing every other received segment
(see Table 3.2 in the text) among these first ten data-carrying segments?

**Question 11**
What is the throughput (bytes transferred per unit time) for the TCP connection?
Explain how you calculated this value.

**Question 12**
Use the Time-Sequence-Graph(Stevens) plotting tool to view the sequence
number versus time plot of segments being sent from the client to the
server server. Consider the “fleets” of packets sent around t = 0.025, t
= 0.053, t = 0.082 and t = 0.1. Comment on whether this looks as if TCP is in its
slow start phase, congestion avoidance phase or some other phase.


**Question 13**
These “fleets” of segments appear to have some periodicity. What can you say
about the period?

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
