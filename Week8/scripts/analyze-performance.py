import json
import os
import statistics
import sys

def analyze_results(report_path):
    if not os.path.exists(report_path):
        print(f"Error: Report file {report_path} not found.")
        return

    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("\n" + "="*50)
    print("      OPERATIONAL MONITORING & PERFORMANCE REPORT")
    print("="*50)

    executions = data.get('run', {}).get('executions', [])
    
    total_requests = 0
    total_failed = 0
    all_latencies = []

    request_stats = {}

    for exec_item in executions:
        request_name = exec_item.get('item', {}).get('name', 'Unknown')
        response = exec_item.get('response', {})
        
        if not response:
            continue

        total_requests += 1
        latency = response.get('responseTime', 0)
        all_latencies.append(latency)

        # Check for failures in assertions
        assertions = exec_item.get('assertions', [])
        failed_assertions = [a for a in assertions if 'error' in a]
        
        is_failed = len(failed_assertions) > 0 or response.get('code', 0) >= 400
        if is_failed:
            total_failed += 1

        if request_name not in request_stats:
            request_stats[request_name] = []
        request_stats[request_name].append(latency)

    if not all_latencies:
        print("No data found in report.")
        return

    # Overall Stats
    avg_latency = statistics.mean(all_latencies)
    p50 = statistics.median(all_latencies)
    all_latencies.sort()
    n = len(all_latencies)
    p95 = all_latencies[int(n * 0.95)] if n > 0 else 0
    p99 = all_latencies[int(n * 0.99)] if n > 0 else 0
    
    error_rate = (total_failed / total_requests) * 100 if total_requests > 0 else 0
    availability = 100 - error_rate

    print(f"{'Metric':<20} | {'Value':<15}")
    print("-" * 38)
    print(f"{'Availability':<20} | {availability:>14.2f}%")
    print(f"{'Error Rate':<20} | {error_rate:>14.2f}%")
    print(f"{'Avg Latency':<20} | {avg_latency:>12.2f} ms")
    print(f"{'p50 Latency':<20} | {p50:>12.2f} ms")
    print(f"{'p95 Latency':<20} | {p95:>12.2f} ms")
    print(f"{'p99 Latency':<20} | {p99:>12.2f} ms")
    
    print("\nSLA CHECK:")
    sla_passed = True
    if p95 > 500:
        print("[FAIL] p95 latency is > 500ms")
        sla_passed = False
    if availability < 99.9:
        print("[WARN] Availability is below 99.9%")
    
    if sla_passed:
        print("[PASS] All SLA targets met.")

    print("="*50 + "\n")

if __name__ == "__main__":
    report_file = sys.argv[1] if len(sys.argv) > 1 else "reports/newman-results.json"
    analyze_results(report_file)
