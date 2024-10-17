# UUID v9

## Fast, lightweight, zero-dependency Python implementation of UUID version 9

The v9 UUID supports both sequential (time-based) and non-sequential (random) UUIDs with an optional prefix of up to four bytes, an optional checksum, and sufficient randomness to avoid collisions. It uses the UNIX timestamp for sequential UUIDs and CRC-8 for checksums. A version digit can be added if desired, but is omitted by default.

To learn more about UUID v9, please visit the website: https://uuidv9.jhunt.dev

## Installation

Install UUID v9 from PyPI.

```bash
python3 -m pip install uuid-v9
```

## Usage

```python
from uuid_v9 import uuidv9, is_valid_uuidv9

ordered_id = uuidv9()
prefixed_ordered_id = uuidv9(prefix='a1b2c3d4')
unordered_id = uuidv9(timestamp=False)
prefixed_unordered_id = uuidv9(prefix='a1b2c3d4', timestamp=False)
ordered_id_with_checksum = uuidv9(checksum=True)
ordered_id_with_version = uuidv9(checksum=True, version=True)
ordered_id_with_compatibility = uuidv9(legacy=True)

const is_valid = validate_uuidv9(ordered_id)
const is_valid_with_checksum = validate_uuidv9(ordered_id_with_checksum, True)
const is_valid_with_version = validate_uuidv9(ordered_id_with_version, True, True)
const is_valid_with_compatibility = validate_uuidv9(ordered_id_with_compatibility, True, '1')
```

### Command Line Usage

```bash
python3 uuid_v9.py
python3 uuid_v9.py --prefix 'a1b2c3d4' # add a prefix
python3 uuid_v9.py --random # omit the timestamp
python3 uuid_v9.py --checksum # add a CRC-8 checksum
python3 uuid_v9.py --version # add a version 9 digit
python3 uuid_v9.py --legacy # legacy mode (see Backward Compatibility below)
```

## Backward Compatibility

Some UUID validators check for specific features of v1 or v4 UUIDs. This causes some valid v9 UUIDs to appear invalid. Three possible workarounds are:

1) Use the built-in validator (recommended)
2) Use compatibility mode*
3) Bypass the validator (not recommended)

_*Legacy mode adds version and variant digits to immitate v1 or v4 UUIDs depending on the presence of a timestamp._

## License

This project is licensed under the [MIT License](LICENSE).