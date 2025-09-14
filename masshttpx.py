import argparse

def parse_masscan_line(line):
    """
    Parse satu baris dari output Masscan dan convert ke URL http/https.
    """
    if "Host:" in line and "Ports:" in line:
        try:
            parts = line.strip().split()
            ip = parts[3]
            port = parts[7].split('/')[0]

            if port == "443":
                return f"https://{ip}"
            else:
                return f"http://{ip}"
        except IndexError:
            return None
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

    print(f"[+] Converted {len(urls)} hosts to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Convert Masscan output to httpx input list")
    parser.add_argument("-i", "--input", required=True, help="Masscan output file")
    parser.add_argument("-o", "--output", default="targets.txt", help="Output file for httpx (default: targets.txt)")

    args = parser.parse_args()
    convert_masscan_to_httpx(args.input, args.output)

if __name__ == "__main__":
    main()
