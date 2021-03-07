import json
import sys
import glob
from pathlib import Path
import statistics
import numpy as np


def read_file_as_json(file_name):
    with open(file_name) as f:
        return json.loads(f.read())

def get_config_json(config_file_name):
    return read_file_as_json(config_file_name)

def get_test_out_dir(config_json):
    return Path(config_json["corpus_directory"])

def get_metadata_lazy(config_json):
    metadata_glob_str = str(get_test_out_dir(config_json) / "*.metadata.json")
    return glob.iglob(metadata_glob_str)


config_json = get_config_json(sys.argv[1])
generation_times = []
generation_times_with_timestamps = []
mean = -1.0
median = -1.0
stddev = -1.0
mintime = -1.0
maxtime = 1.0

for metadata_file_name in get_metadata_lazy(config_json):
    metadata_json = read_file_as_json(metadata_file_name)
    generation_times.append(metadata_json["time_to_produce"])
    generation_times_with_timestamps.append(
        {"time_to_produce": metadata_json["time_to_produce"],
         "timestamp": metadata_json["timestamp"]}
    )

generation_times_with_timestamps = sorted(generation_times_with_timestamps, key=lambda x: x['timestamp'], reverse=False)

generation_times = np.array(generation_times)
mean = np.mean(generation_times)
median = np.median(generation_times)
mintime = np.amin(generation_times)
maxtime = np.amax(generation_times)
stddev = np.std(generation_times) 

print(f'Num elems: {generation_times.size}')
print(f'Mean: {mean}')
print(f'Median: {median}')
print(f'Min: {mintime}')
print(f'Max: {maxtime}')
print(f'Stdev: {stddev}')

print(f'First and second times: {generation_times_with_timestamps[0]} {generation_times_with_timestamps[1]}')
