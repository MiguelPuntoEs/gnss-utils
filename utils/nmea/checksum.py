# record has the following format: GNGGA,220002.00,4724.5238070,N,00937.1060504,E,4,15,0.8,476.195,M,,,0.87,0000
def compute_NMEA_checksum(record: str) -> str:
  checksum = 0
  for el in record:
      checksum ^= ord(el)
  return f'{checksum:02X}'

# Returns True if checksum is correct
def check_NMEA_checksum(record: str) -> bool:
  record_split = record.split('*')
  clean_record = record_split[0][1:]
  received_checksum = record_split[1]

  return compute_NMEA_checksum(clean_record) == received_checksum