"""
TP4 — gRPC Metrics Streaming Client
=====================================
Demonstrates server-side streaming over gRPC (HTTP/2 binary transport).

The client sends one MetricsRequest and receives a stream of MetricUpdate
messages from the server — one per second for 10 seconds.

Observe in Wireshark:
  - A single TCP connection carries the entire 10-message stream
  - HTTP/2 DATA frames contain binary protobuf payloads (not plain text)
  - The gRPC framing layer sits on top of HTTP/2

Run: python client.py   (server must be running in another terminal)
"""

import grpc

import metrics_pb2
import metrics_pb2_grpc

# ──────────────────────────────────────────────────────────────────
# CONFIGURATION — Complete TODO 1
# ──────────────────────────────────────────────────────────────────

HOST = "localhost"

# TODO 1: Set the port number to match the server's PORT value.
#
#   The server uses the conventional gRPC port: 50051
#
PORT = ????


# ──────────────────────────────────────────────────────────────────
# gRPC CLIENT — Complete TODOs 2 and 3
# ──────────────────────────────────────────────────────────────────

def run():

    # TODO 2: Open an insecure gRPC channel to the server.
    #
    #   Use grpc.insecure_channel("host:port") to create the channel.
    #   The channel represents the underlying HTTP/2 connection to the server.
    #   Format the target address as the string:  f"{HOST}:{PORT}"
    #
    #   No TLS is used in this TP — this makes traffic visible in Wireshark.
    #
    channel = grpc.insecure_channel(????)

    stub = metrics_pb2_grpc.MetricsServiceStub(channel)

    # TODO 3: Build the request and start the streaming RPC.
    #
    #   Step A — Create a MetricsRequest with your client_id:
    #     request = metrics_pb2.MetricsRequest(client_id=????)
    #     Replace ???? with a short string identifying you (e.g. "student-1")
    #
    #   Step B — Call the streaming RPC on the stub:
    #     stream = stub.????(request)
    #     Replace ???? with the RPC method name from metrics.proto
    #
    request = metrics_pb2.MetricsRequest(client_id=????)
    stream  = stub.????(request)

    print(f"\n  gRPC client connected to {HOST}:{PORT}")
    print(f"  Wireshark filter: tcp.port == {PORT}")
    print(f"  Waiting for metric stream...\n")
    print(f"  {'Timestamp':<22}  {'Bandwidth':>12}  {'Latency':>12}  {'Loss':>6}")
    print(f"  {'-'*22}  {'-'*12}  {'-'*12}  {'-'*6}")

    # Iterate over the stream (provided — do not modify)
    count = 0
    for update in stream:
        count += 1
        print(f"  {update.timestamp:<22}  "
              f"{update.bandwidth_mb:>10.1f} MB/s  "
              f"{update.latency_ms:>10.1f} ms  "
              f"{update.packet_loss:>5}%")

    print(f"\n  Stream ended — received {count} metric update(s).")
    print(f"  In Wireshark: one TCP connection carried all {count} messages.")
    print(f"  Compare with TP1 where each chunk needed its own TCP connection.\n")

    channel.close()


if __name__ == "__main__":
    run()
