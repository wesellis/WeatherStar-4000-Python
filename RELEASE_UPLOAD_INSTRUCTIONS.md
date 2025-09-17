# GitHub Release Upload Instructions

## Release Assets Ready for Upload

### 1. Raspberry Pi Package
- **File**: `WeatherStar4000-v2.1.0-RaspberryPi.tar.gz` (287MB)
- **Checksum**: `WeatherStar4000-v2.1.0-RaspberryPi.tar.gz.sha256`
- **Contains**: Full application with installer script
- **For**: Raspberry Pi 3B+, 4, Zero 2 W

### 2. Windows Executable
- **Note**: Requires Windows machine with Python & PyInstaller to build
- **Script Ready**: `build_windows.bat`
- Run on Windows to create `WeatherStar4000-v2.1.0-Windows.zip`

## Upload Steps

1. Go to: https://github.com/wesellis/WeatherStar-4000-Python/releases/edit/v2.1.0

2. In "Attach binaries" section, drag and drop:
   - `WeatherStar4000-v2.1.0-RaspberryPi.tar.gz`
   - `WeatherStar4000-v2.1.0-RaspberryPi.tar.gz.sha256`

3. Update release description with download instructions:

```markdown
## Downloads

### For Raspberry Pi
Download: `WeatherStar4000-v2.1.0-RaspberryPi.tar.gz`

```bash
# Extract and install
tar -xzf WeatherStar4000-v2.1.0-RaspberryPi.tar.gz
cd WeatherStar4000-v2.1.0-RaspberryPi
./install.sh
```

### For Windows
Building from source recommended. Use `build_windows.bat` with Python 3.8+ and PyInstaller.

### For Linux/Mac
Clone and run directly with Python:
```bash
git clone https://github.com/wesellis/WeatherStar-4000-Python.git
cd WeatherStar-4000-Python
pip install -r requirements.txt
python3 weatherstar4000.py
```
```

4. Save/Update the release

## File Sizes Note
GitHub has a 2GB file size limit for release assets. Our Raspberry Pi package (287MB) is well within limits.