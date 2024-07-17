# hashtrack

A simple tool to track the hash of files in case you need to verify them later.

## Installation

```bash
git clone https://github.com/fkcptlst/hashtrack.git
cd hashtrack
pip install .
```

## Usage

```bash
Usage: hashtrack [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  cache   Cache commands
  check   Check if entries in cache is modified (whether the file is...
  config  Configuration commands
  init    Initialize HashTrack cache
  update  Scan for new/modified/removed files and update the cache.
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
```