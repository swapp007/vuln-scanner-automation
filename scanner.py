import nmap
import yaml
import datetime
import os

with open("config.yaml") as f:
    config = yaml.safe_load(f)

TARGETS = config["targets"]
SCAN_TYPE = config["scan_type"]
REPORT_FORMAT = config["report_format"]

scanner = nmap.PortScanner()

def run_scan(target):
    print(f"Scanning {target} ...")
    scanner.scan(target, arguments=SCAN_TYPE)
    return scanner[target]

def generate_report(results):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    report_file = f"reports/scan_report_{timestamp}.{REPORT_FORMAT}"

    os.makedirs("reports", exist_ok=True)

    with open(report_file, "w") as f:
        if REPORT_FORMAT == "html":
            f.write("<html><body><h2>Vulnerability Scan Report</h2>")
            for host, data in results.items():
                f.write(f"<h3>{host}</h3><pre>{data}</pre>")
            f.write("</body></html>")
        else:
            for host, data in results.items():
                f.write(f"Host: {host}\n{data}\n\n")

    print(f"Report generated: {report_file}")

def main():
    results = {}

    for target in TARGETS:
        try:
            results[target] = run_scan(target)
        except Exception as e:
            results[target] = f"Scan failed: {str(e)}"

    generate_report(results)

if __name__ == "__main__":
    main()
