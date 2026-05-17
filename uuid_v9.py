import re
import random
import time

uuid_regex = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)

def calc_checksum(hex_string:str):
    data = [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]
    polynomial = 0x07
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
    return format(crc & 0xFF, '02x')

def verify_checksum(uuid:str):
    clean_uuid = uuid.replace('-', '')[0:30]
    checksum = calc_checksum(clean_uuid)
    return checksum == uuid[34:36]

def validate_uuidv9(uuid:str, checksum=False, version=0):
    return (isinstance(uuid, str) 
        and uuid_regex.match(uuid)
        and (not checksum or verify_checksum(uuid))
        and (not version or (
            uuid[14:15] == str(version)
            and uuid[19] in '89abAB'
        )))

def random_bytes(count:int):
    return ''.join(random.choice('0123456789abcdef') for _ in range(count))

def random_char(chars:str):
    random_index = random.randint(0, len(chars) - 1)
    return chars[random_index]

base16_regex = re.compile(r'^[0-9a-fA-F]+$')

def is_base16(str:str):
    return bool(base16_regex.match(str))

def validate_prefix(prefix:str):
    if not isinstance(prefix, str):
        raise ValueError('Prefix must be a string')
    if len(prefix) > 8:
        raise ValueError('Prefix must be no more than 8 characters')
    if not is_base16(prefix):
        raise ValueError('Prefix must be only hexadecimal characters')

def validate_suffix(suffix:str):
    if not isinstance(suffix, str):
        raise ValueError('Suffix must be a string')
    if len(suffix) > 4:
        raise ValueError('Suffix must be no more than 4 characters')
    if not is_base16(suffix):
        raise ValueError('Suffix must be only hexadecimal characters')

def add_dashes(str:str):
    return f'{str[:8]}-{str[8:12]}-{str[12:16]}-{str[16:20]}-{str[20:]}'

def uuidv9(prefix='', timestamp=True, checksum=False, version=False, legacy=False, suffix=''):
    if prefix:
        validate_prefix(prefix)
        prefix = prefix.lower()
    if suffix:
        validate_suffix(suffix)
        suffix = suffix.lower()
    center = format(int(time.time_ns() / 1000000), 'x') if timestamp is True else format(timestamp, 'x') if isinstance(timestamp, int) else ''
    random = random_bytes(32 - len(prefix or '') - len(suffix or '') - len(center) - (2 if checksum else 0) - (2 if (legacy or version) else 0)) # (2 if legacy else 1 if version else 0)
    joined = (prefix or '') + center + random + (suffix or '')
    if legacy:
        joined = joined[:12] + ('1' if timestamp else '4') + joined[12:15] + random_char('89ab') + joined[15:]
    elif version:
        joined = joined[:12] + '9' + joined[12:15] + random_char('89ab') + joined[15:] # joined[12:]
    if checksum:
        joined += calc_checksum(joined)
    return add_dashes(joined)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate and validate UUID v9.")
    parser.add_argument("--prefix", dest="prefix", default="", help="Include a prefix")
    parser.add_argument("--suffix", dest="suffix", default="", help="Include a suffix")
    parser.add_argument("--timestamp", dest="timestamp", help="Customize the timestamp")
    parser.add_argument("--random", dest="random", action="store_true", help="Exclude timestamp")
    parser.add_argument("--checksum", dest="checksum", action="store_true", help="Include checksum")
    parser.add_argument("--version", dest="version", action="store_true", help="Include version")
    parser.add_argument("--legacy", dest="legacy", action="store_true", help="Legacy mode (v1/v4)")
    args = parser.parse_args()
    print(uuidv9(prefix=args.prefix, suffix=args.suffix, timestamp=int(args.timestamp) if args.timestamp else not args.random, checksum=args.checksum, version=args.version, legacy=args.legacy))