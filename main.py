import sys
import os

def parse_arguments():
    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist.")
        sys.exit(1)

    return input_file, output_file

if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    print(f"Converting {input_file} to {output_file}")
