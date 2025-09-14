import argparse
import re

def parse_masscan_line(line):
    """
    Parse line format seperti:
    Timestamp: 1757843832   Host: 23.61.80.242 ()   Ports: 443/open/tcp//https//
    """
    match = re.search(r'Host:\s+([\d.]+)\s+\(\)\s+Ports:\s+(\d+)/open/tcp', line)
    if match:
        ip = match.group(1)
        port = match.group(2)

        if port == "443":
            return f"https://{ip}"
        elif port == "80":
            return f"http://{ip}"
        else:
            return f"http://{ip}:{port}"
    return None

def convert_masscan_to_httpx(input_file, output_file):
    urls = []

    with open(input_file, "r") as infile:
        for line in infile:
            url = parse_masscan_line(line)
            if url:
                urls.append(url)

    with open(output_file, "w") as outfile:
        for url in urls:
            outfile.write(url + "\n")

    print(f"[+] Converted {len(urls)} targets to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert Masscan output to httpx input list")
    parser.add_argument("-i", "--input", required=True, help="Masscan output file")
    parser.add_argument("-o", "--output", default="targets.txt", help="Output file for httpx (default: targets.txt)")

    args = parser.parse_args()
    convert_masscan_to_httpx(args.input, args.output)

if __name__ == "__main__":
    main()
