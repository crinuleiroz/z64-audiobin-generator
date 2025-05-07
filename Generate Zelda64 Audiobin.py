import os
import sys
import shutil
import tempfile
from typing import BinaryIO

# Last updated
LAST_UPDATED = '2025.05.06'

# Create ANSI formatting for terminal messages
# ANSI COLORS: https://talyian.github.io/ansicolors/
RESET  = "\x1b[0m"
BLUE   = "\x1b[38;5;14m"
PINK   = "\x1b[38;5;218m"
GREEN  = "\x1b[38;5;115m"
GREY   = "\x1b[38;5;8m"
YELLOW = "\x1b[33m"

OOT_BLUE = "\x1b[38;5;39m"
MM_PURPLE = "\x1b[38;5;141m"

ROM_FILE = sys.argv[1]
ROM_LENGTH = 67108864 # Decompressed ROM Size

# "Filename": (offset, size)
AUDIOBIN_OFFSETS: dict[str, dict[str, tuple[int, int]]] = {
    "oot": {
        "Audiobank":        (0x0000D390, 0x0001CA50),
        "Audiobank_index":  (0x00B896A0, 0x00000270),
        "Audiotable":       (0x00079470, 0x00460AD0),
        "Audiotable_index": (0x00B8A1C0, 0x00000080)
    },
    "mm": {
        "Audiobank":        (0x00020700, 0x000263F0),
        "Audiobank_index":  (0x00C776C0, 0x000002A0),
        "Audiotable":       (0x00097F70, 0x00548770),
        "Audiotable_index": (0x00C78380, 0x00000040)
    }
}

class SysMsg:
  @staticmethod
  def header():
    print(f'''\
{GREY}[▪]----------------------------------[▪]
 |   {RESET}{PINK}AUDIOBIN GENERATOR {GREY}v{LAST_UPDATED}   |
[▪]----------------------------------[▪]{RESET}
''')

  @staticmethod
  def complete():
    print(f'''\
{GREY}[▪]----------------------------------[▪]
 |     {RESET}{GREEN}Process is now completed      {GREY}|
[▪]----------------------------------[▪]{RESET}
''')
    os.system('pause')

  @staticmethod
  def compressed_rom():
    print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Error: ROM file is not decompressed!
''')
    os.system('pause')
    sys.exit(1)

  @staticmethod
  def read_rom_header():
    print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Reading ROM header:     {BLUE}"{ROM_FILE}"{RESET}''')

  @staticmethod
  def detected_game(game : str, color : str):
    print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Detected game:          {color}"{game}"{RESET}
''')

  @staticmethod
  def byteswapped_rom():
    print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Error: ROM file byte order is "Byteswapped", use {PINK}tool64{RESET} to change the byte order to "Big Endian"!
''')
    os.system('pause')
    sys.exit(1)

  @staticmethod
  def little_endian_rom():
    print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Error: ROM file byte order is "Little Endian", use {PINK}tool64{RESET} to change the byte order to "Big Endian"!
''')
    os.system('pause')
    sys.exit(1)

  @staticmethod
  def unknown_game():
    print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Error: Decompressed ROM has an unexpected ROM header!
''')
    os.system('pause')
    sys.exit(1)

  @staticmethod
  def processing_file(name: str):
    print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Extracting and writing: {BLUE}"{name}"{RESET}''')

  @staticmethod
  def creating_archive(file_dir : str, filename : str):
    print(f'''\

{GREY}[{PINK}>{GREY}]:{RESET} Creating archive:       {BLUE}"{file_dir}/{filename}.audiobin"{RESET}
''')

def extract_and_write_audiofile(rom: BinaryIO, offset : int, size: int, filename: str, tempfolder: str):
  rom.seek(offset)
  audio_data = rom.read(size)
  filepath = os.path.join(tempfolder, filename)
  with open(filepath, 'wb') as f:
    f.write(audio_data)

def generate_oot_audiobin(file_dir : str, tempfolder : str):
  with open(ROM_FILE, 'rb') as rom:
    for name, (offset, size) in AUDIOBIN_OFFSETS["oot"].items():
      SysMsg.processing_file(name)
      extract_and_write_audiofile(rom, offset, size, name, tempfolder)

  SysMsg.creating_archive(file_dir, "OOT")
  shutil.make_archive(f"{file_dir}/OOT", "zip", tempfolder)
  os.rename(f"{file_dir}/OOT.zip", f"{file_dir}/OOT.audiobin")

def generate_mm_audiobin(file_dir : str, tempfolder : str):
  with open(ROM_FILE, 'rb') as rom:
    for name, (offset, size) in AUDIOBIN_OFFSETS["mm"].items():
      SysMsg.processing_file(name)
      extract_and_write_audiofile(rom, offset, size, name, tempfolder)

  SysMsg.creating_archive(file_dir, "MM")
  shutil.make_archive(f"{file_dir}/MM", "zip", tempfolder)
  os.rename(f"{file_dir}/MM.zip", f"{file_dir}/MM.audiobin")

def main(game: str) -> None:
  file_dir = os.path.dirname(os.path.abspath(__file__))

  with tempfile.TemporaryDirectory(prefix="audiobin_generator_") as tempfolder:
    if game == "oot":
      generate_oot_audiobin(file_dir, tempfolder)

    if game == "mm":
      generate_mm_audiobin(file_dir, tempfolder)


if __name__ == "__main__":
  SysMsg.header()

  if os.path.getsize(ROM_FILE) != ROM_LENGTH:
    SysMsg.compressed_rom()

  SysMsg.read_rom_header()
  with open(ROM_FILE, 'rb') as rom:
    rom_header = rom.read(64)

    # OCARINA OF TIME BIG ENDIAN
    if b"THE LEGEND OF ZELDA \x00\x00\x00\x00\x00\x00\x00CZLE\x00" in rom_header:
      SysMsg.detected_game("Ocarina of Time", OOT_BLUE)
      game = "oot"

    # MAJORA'S MASK BIG ENDIAN
    elif b"ZELDA MAJORA'S MASK \x00\x00\x00\x00\x00\x00\x00NZSE\x00" in rom_header:
      SysMsg.detected_game("Majora's Mask", MM_PURPLE)
      game = "mm"

    # OCARINA OF TIME BYTESWAPPED
    elif b"HT EELEGDNO  FEZDL A\x00\x00\x00\x00\x00\x00C\x00L\x00E" in rom_header:
      SysMsg.detected_game("Ocarina of Time", OOT_BLUE)
      SysMsg.byteswapped_rom()

    # MAJORA'S MASK BYTESWAPPED
    elif b"EZDL AAMOJARS'M SA K\x00\x00\x00\x00\x00\x00N\x00SZ\x00E" in rom_header:
      SysMsg.detected_game("Majora's Mask", MM_PURPLE)
      SysMsg.byteswapped_rom()

    # OCARINA OF TIME LITTLE ENDIAN
    elif b"EHTEGELO DNEZ F ADL\x00\x00\x00\x00C\x00\x00\x00\x00ELZ" in rom_header:
      SysMsg.detected_game("Ocarina of Time", OOT_BLUE)
      SysMsg.little_endian_rom()

    # MAJORA'S MASK LITTLE ENDIAN
    elif b"DLEZAM AAROJM S' KSA\x00\x00\x00\x00N\x00\x00\x00\x00ESZ" in rom_header:
      SysMsg.detected_game("Majora's Mask", MM_PURPLE)
      SysMsg.little_endian_rom()

    # UNKNOWN GAME
    else:
      SysMsg.unknown_game()

  main(game)
  SysMsg.complete()
