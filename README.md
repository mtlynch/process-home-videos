# process-home-videos

[![CircleCI](https://circleci.com/gh/mtlynch/process-home-videos.svg?style=svg)](https://circleci.com/gh/mtlynch/process-home-videos)

## Overview

Python scripts for chopping up raw video files into clips and then publishing those clips to MediaGoblin.

## Requirements

* Python 3.7
* Docker
* ffmpeg
* virtualenv

## Installation

To run this project in a virtualenv, run the following

```bash
mkdir -p ./venv
virtualenv --python python3 ./venv
. venv/bin/activate
pip install --requirement requirements.txt
```

## csv\_to\_yaml

The `csv_to_yaml.py` script takes a CSV spreadsheet and converts it to a YAML file.

It exists because it's easier for the user to enter raw information into a spreadsheet, but it's easier for the applications to process rich data from a YAML that includes some postprocessing on the raw data.

### Example

```bash
app/csv_to_yaml.py \
  --config config.yaml \
  ~/metadata/scene-metadata.csv \
  > ~/metadata/scenes.yaml
```

## render\_scenes

Given raw video files, renders scenes by chopping out clips according to a scenes metadata file.

### Example

```bash
app/render_scenes.py \
  --metadata ~/metadata/scenes.yaml \
  --raw_videos_dir /mnt/videos-raw \
  --output_clips_dir /mnt/videos-processed/
```

## publish\_to\_mediagoblin

The `publish_to_mediagoblin` script uploads scenes to a MediaGoblin instance running in the specified Docker container.

* `--publish_history` is a flat text file of files that have previously been uploaded to this container (in case the publish process is interrupted and resumed)
* `--conatiner_name` is the name of the target Docker container running MediaGoblin.

### Example

```bash
app/publish_to_mediagoblin.py \
  /mnt/videos-processed   \
  --metadata ~/metadata/scenes.yaml \
  --publish_history ~/metadata/publish-history.txt \
  --container_name mediagoblin
```

## Contributing

A lot of this code is very quick 'n dirty, as I never intended it to be a long-term project. If you'd like to iterate on it, I'm happy to accept contributions, but I apologize for the quality of the code.

To install with dev tools:

```bash
mkdir -p ./venv
virtualenv --python python3 ./venv
. venv/bin/activate
pip install --requirement requirements.txt
pip install --requirement dev_requirements.txt
hooks/enable_hooks
```

To run quick tests:

```bash
./build
```

To run end-to-end tests:

```bash
./e2e/run-all-e2e-tests
```