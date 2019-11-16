# process-home-videos

[![CircleCI](https://circleci.com/gh/mtlynch/process-home-videos.svg?style=svg)](https://circleci.com/gh/mtlynch/process-home-videos)

## Overview

Python scripts for chopping up raw video files into clips and then publishing those clips to MediaGoblin.

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

### Example

```bash
app/publish_to_mediagoblin.py \
  /mnt/videos-processed   \
  --metadata ~/metadata/scenes.yaml \
  --publish_history ~/metadata/publish-history.txt \
  --container_name mediagoblin
```
