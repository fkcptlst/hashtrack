# hashtrack

A simple tool to track the hash of files in case you need to verify them later.

## Installation

### Install from PyPI

```bash
pip install hashtrack
```

### Install from Source

```bash
git clone https://github.com/fkcptlst/hashtrack.git
cd hashtrack
pip install -e .
```

## Usage

```bash
hashtrack --help
```

## Example

```bash
hashtrack init  # Initialize the cache
hashtrack update  # Update the cache
# do some work or modify files
hashtrack check  # Check the checksum of the files in the cache
```

## Configuration

Under `.hashtrack` directory, there is a `config.yml` file that you can modify to suit your needs.

```yaml
extensions:  # ".ext"
  - ".ckpt"
  - ".pth"
  - ".pt"
  - ".h5"
  - ".onnx"
  - ".safetensors"
  - ".pkl"
  - ".npy"

search_dirs:  # list[str]
  - "."

# if current time - modification_time > min_update_interval, then file is considered to be updated
watch:
  min_update_interval: 60  # seconds
  sleep_interval: 5  # seconds
```