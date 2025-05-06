# Zelda64 Audiobin Generator

## 🔧 How to Use
Drag and drop a decompressed Ocarina of Time or Majora's Mask ROM onto the script or use the following CLI command:
```
python <script name> <ROM file>
```
The script will check the size of the ROM to ensure it is decompressed, then it will read the ROM's header to detect the game and extract the audio binary files at the correct offsets.

> [!NOTE]
> The output `.audiobin` file will be in the same folder as the script — it will not be in the same folder as the input ROM file.
