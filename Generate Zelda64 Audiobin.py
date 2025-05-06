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

def extract_and_write_audiofile(rom: BinaryIO, offset : int, size: int, filename: str, tempfolder: str):
  rom.seek(offset)
  audio_data = rom.read(size)
  filepath = os.path.join(tempfolder, filename)
  with open(filepath, 'wb') as f:
    f.write(audio_data)

def generate_oot_audiobin(file_dir : str, tempfolder : str):
  with open(ROM_FILE, 'rb') as rom:
    for name, (offset, size) in AUDIOBIN_OFFSETS["oot"].items():
      print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Extracting and writing: {BLUE}"{name}"{RESET}''')
      extract_and_write_audiofile(rom, offset, size, name, tempfolder)

  print(f'''\

{GREY}[{PINK}>{GREY}]:{RESET} Creating archive:       {BLUE}"{file_dir}/OOT.audiobin"{RESET}
''')
  shutil.make_archive(f"{file_dir}/OOT", "zip", tempfolder)
  os.rename(f"{file_dir}/OOT.zip", f"{file_dir}/OOT.audiobin")

def generate_mm_audiobin(file_dir : str, tempfolder : str):
  with open(ROM_FILE, 'rb') as rom:
    for name, (offset, size) in AUDIOBIN_OFFSETS["mm"].items():
      print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Extracting and writing: {BLUE}"{name}"{RESET}''')
      extract_and_write_audiofile(rom, offset, size, name, tempfolder)

  print(f'''\

{GREY}[{PINK}>{GREY}]:{RESET} Creating archive:       {BLUE}"{file_dir}/MM.audiobin"{RESET}
''')
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
  print(f'''\
{GREY}[▪]----------------------------------[▪]
 |   {RESET}{PINK}AUDIOBIN GENERATOR {GREY}v{LAST_UPDATED}   |
[▪]----------------------------------[▪]{RESET}
''')
  if os.path.getsize(ROM_FILE) != ROM_LENGTH:
    print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Error: ROM file is not decompressed!
''')
    os.system('pause')
    sys.exit(1)

  print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Reading ROM header:     {BLUE}"{ROM_FILE}"{RESET}''')
  with open(ROM_FILE, 'rb') as rom:
    rom_header = rom.read(64)

    if b"THE LEGEND OF ZELDA \x00\x00\x00\x00\x00\x00\x00CZLE\x00" in rom_header:
      print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Detected game:          {OOT_BLUE}"Ocarina of Time"{RESET}
''')
      game = "oot"
    elif b"ZELDA MAJORA'S MASK \x00\x00\x00\x00\x00\x00\x00NZSE\x00" in rom_header:
      print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Detected game:          {MM_PURPLE}"Majora's Mask"{RESET}
''')
      game = "mm"
    else:
      print(f'''\
{GREY}[{PINK}>{GREY}]:{RESET} Error: Decompressed ROM has an unexpected ROM header!
''')
      os.system('pause')
      sys.exit(1)

  main(game)
  print(f'''\
{GREY}[▪]----------------------------------[▪]
 |     {RESET}{GREEN}Process is now completed      {GREY}|
[▪]----------------------------------[▪]{RESET}
''')
  os.system('pause')
