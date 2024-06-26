import os
import re
from collections import defaultdict

# Directory containing the files
directory = './'

# Dictionary to hold the files grouped by their prefix
files_dict = defaultdict(list)

# Regex pattern to match the filenames
pattern = re.compile(r"(min_\d+)-.+\.json")

# Populate the dictionary with filenames grouped by prefix
for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        prefix = match.group(1)
        files_dict[prefix].append(filename)

# Rename files sequentially
for prefix, files in files_dict.items():
    # Sort files to ensure consistent renaming order
    files.sort()
    for i, filename in enumerate(files, start=1):
        new_name = f"{prefix}-{i}.json"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

print("Renaming complete.")
