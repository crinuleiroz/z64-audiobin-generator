# Zelda64 Audiobin Generator

## 🔧 How to Use
Drag and drop an Ocarina of Time or Majora's Mask ROM onto the script or use the following CLI command:
```
python <script name> <ROM file>
```
The script will read the ROM's header to detect the game, extract the audio binary files at the correct offsets, and write the audio binary index lists.

> [!NOTE]
> The output `.audiobin` file will be in the same folder as the script — it will not be in the same folder as the input ROM file.