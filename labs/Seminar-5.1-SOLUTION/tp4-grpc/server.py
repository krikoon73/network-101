"""
TP4 — gRPC Metrics Streaming Server — SOLUTION
================================================
FOR INSTRUCTOR USE ONLY
"""

import grpc
import time
import random
import datetime
from concurrent import futures

import metrics_pb2
import metrics_pb2_grpc

# ── TODO 1 SOLUTION ──────────────────────────────────────────────
PORT = 50051
# 50051 is the conventional gRPC development port.

STREAM_COUNT = 10


class MetricsServicer(metrics_pb2_grpc.MetricsServiceServicer):

    def StreamMetrics(self, request, context):
        print(f"  [gRPC] New client connected: client_id='{request.client_id}'")

        for i in range(STREAM_COUNT):

            # ── TODO 2 SOLUTION ──────────────────────────────────
            update = metrics_pb2.MetricUpdate(
                timestamp    = datetime.datetime.now().isoformat(timespec="seconds"),
                bandwidth_mb = round(random.uniform(10.0, 100.0), 2),
                latency_ms   = round(random.uniform(1.0, 50.0), 2),
                packet_loss  = random.randint(0, 5),
            )

            # ── TODO 3 SOLUTION ──────────────────────────────────
            yield update

            print(f"  [update {i+1:>2}/{STREAM_COUNT}] "
                  f"bw={update.bandwidth_mb:.1f} MB/s  "
                  f"lat={update.latency_ms:.1f} ms  "
                  f"loss={update.packet_loss}%")

            time.sleep(1)

        print(f"  [gRPC] Stream complete for '{request.client_id}'\n")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))

    # ── TODO 4 SOLUTION ──────────────────────────────────────────
    metrics_pb2_grpc.add_MetricsServiceServicer_to_server(MetricsServicer(), server)

    server.add_insecure_port(f"[::]:{PORT}")
    server.start()

    print(f"\n  gRPC Metrics server started")
    print(f"  Listening on: grpc://localhost:{PORT}  (insecure / no TLS)")
    print(f"  Wireshark filter: tcp.port == {PORT}")
    print(f"\n  In a second terminal, run:  python client.py")
    print(f"  The server will stream {STREAM_COUNT} metric updates, one per second.\n")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
