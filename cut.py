from multiprocessing import Pool
import sys
import json

with open(sys.argv[1]) as f:
    placekeys = set([f["properties"]["placekey"] for f in json.load(f)["features"]])

filenames = sys.argv[2:]

def filter_file(fname):
     date = "2021-" + "-".join(fname.split("/")[1:-2])
     output = ""
     # is_first = True
     with open(fname) as f:
        # if is_first:
        #     output += next(f)[:-1] + ',"date"\n'
        #     is_first = False
          for line in f:
               if line[:19] in placekeys:
                    output += line[:-1] + "," + date + "\n"
        # print("Completed", fname, file=sys.stderr)
     return output

def main():
     pool = Pool()
     for output in pool.imap(filter_file, filenames):
          sys.stdout.write(output)
     pool.close()
     pool.join()

if __name__ == '__main__':
     main()
