import os
import random


def get_modification_time(file_path):
    """Get the modification time of a file."""
    return os.path.getmtime(file_path)


def set_modification_time(file_path, mod_time):
    """Set the modification time of a file."""
    os.utime(file_path, (mod_time, mod_time))


def corrupt_file(file_path, corruption_rate=0.01):
    """Corrupt a file by modifying a specified percentage of its bytes."""
    # Get the original modification time
    original_mod_time = get_modification_time(file_path)

    # Read the file
    with open(file_path, 'rb') as f:
        data = bytearray(f.read())

    # Corrupt the file data
    num_bytes = len(data)
    num_corruptions = int(num_bytes * corruption_rate)

    for _ in range(num_corruptions):
        index = random.randint(0, num_bytes - 1)
        original_byte = data[index]
        corrupt_byte = random.randint(0, 255)
        while corrupt_byte == original_byte:
            corrupt_byte = random.randint(0, 255)
        data[index] = corrupt_byte

    # Write the corrupted data back to the file
    target_file_path = f"corrupted.{file_path}"
    with open(target_file_path, 'wb') as f:
        f.write(data)

    # Restore the original modification time
    set_modification_time(target_file_path, original_mod_time)

    print(f"File corrupted and modification time restored: {target_file_path}")


# Usage
corrupt_file("src.bin", corruption_rate=0.5)