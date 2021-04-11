from multiprocessing import Pool
import sys
import json

with open(sys.argv[1]) as f:
    placekeys = set([f["properties"]["placekey"] for f in json.load(f)["features"]])

filenames = sys.argv[2:]


def filter_file(fname):
    output = ""
    with open(fname) as f:
        for line in f:
            if line[:19] in placekeys:
                output += line
    return output


def main():
    # Print header of first file
    with open(filenames[0]) as f:
        sys.stdout.write(f.readline())

    # Process the files
    pool = Pool()
    for output in pool.imap(filter_file, filenames):
        sys.stdout.write(output)
    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
