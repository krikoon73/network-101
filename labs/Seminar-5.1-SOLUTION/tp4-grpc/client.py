"""
TP4 — gRPC Metrics Streaming Client — SOLUTION
================================================
FOR INSTRUCTOR USE ONLY
"""

import grpc

import metrics_pb2
import metrics_pb2_grpc

HOST = "localhost"

# ── TODO 1 SOLUTION ──────────────────────────────────────────────
PORT = 50051


def run():
    # ── TODO 2 SOLUTION ──────────────────────────────────────────
    channel = grpc.insecure_channel(f"{HOST}:{PORT}")

    stub = metrics_pb2_grpc.MetricsServiceStub(channel)

    # ── TODO 3 SOLUTION ──────────────────────────────────────────
    request = metrics_pb2.MetricsRequest(client_id="student-1")
    stream  = stub.StreamMetrics(request)

    print(f"\n  gRPC client connected to {HOST}:{PORT}")
    print(f"  Wireshark filter: tcp.port == {PORT}")
    print(f"  Waiting for metric stream...\n")
    print(f"  {'Timestamp':<22}  {'Bandwidth':>12}  {'Latency':>12}  {'Loss':>6}")
    print(f"  {'-'*22}  {'-'*12}  {'-'*12}  {'-'*6}")

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
