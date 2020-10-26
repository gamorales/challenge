import json
import csv
import yaml
from dataclasses import dataclass, field


@dataclass
class Parsing(object):

    @staticmethod
    def save(self, filename, filetype):
        with open(f"{filename}.{filetype}", "w") as outfile:
            if filetype == "json":
                outfile.write("[\n")
                for _ in lookup_data:
                    json.dump(eval(_), outfile, indent=4, sort_keys=True)
                    outfile.write(",")
                outfile.write("]")
            elif filetype == "yaml":
                for _ in lookup_data:
                    yaml.dump(eval(_), outfile)
            elif filetype == "csv":
                writer = csv.DictWriter(outfile, fieldnames=eval(lookup_data[0]).keys())
                writer.writeheader()
                for index in lookup_data:
                    writer.writerow(eval(index))

