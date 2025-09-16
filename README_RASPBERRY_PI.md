# WeatherStar 4000 - Raspberry Pi Setup Guide

## Recommended Hardware

### Best Performance
- **Raspberry Pi 4 Model B (2GB or 4GB RAM)**
  - Smooth 60 FPS performance
  - Can handle all animations and transitions
  - Supports dual displays if needed

### Good Performance
- **Raspberry Pi 3B+**
  - 30-45 FPS performance
  - All features work well
  - May have slight delays during transitions

### Minimum Viable
- **Raspberry Pi Zero 2 W**
  - 15-30 FPS performance
  - Compact and low power
  - Best for static display mode

## Installation on Raspberry Pi

### 1. Install Raspberry Pi OS
```bash
# Use Raspberry Pi OS Lite (32-bit) for best performance
# Or Raspberry Pi OS with Desktop if you want GUI
```

### 2. Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### 3. Install Dependencies
```bash
# Python and pip
sudo apt install python3 python3-pip git -y

# SDL dependencies for pygame
sudo apt install python3-pygame -y

# Alternative pygame installation if needed
pip3 install pygame requests

# For better performance on Pi
sudo apt install libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 -y
```

### 4. Clone Repository
```bash
cd ~
git clone https://github.com/wesellis/WeatherStar-4000-Python.git
cd WeatherStar-4000-Python
```

### 5. Install Python Requirements
```bash
pip3 install -r requirements.txt
```

### 6. Run WeatherStar 4000
```bash
python3 run_weatherstar.py
```

## Performance Optimization for Raspberry Pi

### Enable GPU Acceleration
Edit `/boot/config.txt`:
```
gpu_mem=128
dtoverlay=vc4-fkms-v3d
```

### Reduce Resolution (if needed)
```bash
# For Pi Zero or older models, reduce to 480p
export SDL_VIDEODRIVER=fbcon
export SDL_FBDEV=/dev/fb0
```

### Auto-start on Boot

Create service file:
```bash
sudo nano /etc/systemd/system/weatherstar.service
```

Add:
```ini
[Unit]
Description=WeatherStar 4000
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/WeatherStar-4000-Python
ExecStart=/usr/bin/python3 /home/pi/WeatherStar-4000-Python/run_weatherstar.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable weatherstar.service
sudo systemctl start weatherstar.service
```

## Display Options

### HDMI Output
- Works out of the box
- Best quality at 640x480 or 1024x768

### Composite Video (RCA)
- For authentic CRT TV experience
- Edit `/boot/config.txt`:
```
sdtv_mode=0  # NTSC
hdmi_ignore_hotplug=1
```

### Small TFT/LCD Displays
- Adafruit PiTFT works great
- Waveshare displays supported
- May need to adjust resolution

## Memory Usage

- Base: ~150MB RAM
- With music: ~200MB RAM
- With all features: ~250MB RAM

## Tips for Best Performance

1. **Disable unnecessary services:**
```bash
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon
```

2. **Use wired ethernet** instead of WiFi for reliability

3. **Set static IP** for faster boot:
```bash
sudo nano /etc/dhcpcd.conf
# Add:
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8
```

4. **Overclock (Pi 3/4 only):**
```bash
# Edit /boot/config.txt
over_voltage=2
arm_freq=1750  # Pi 4
gpu_freq=500
```

## Troubleshooting

### Black Screen
- Check HDMI cable
- Try: `export DISPLAY=:0`

### Slow Performance
- Reduce music volume or disable
- Check CPU temp: `vcgencmd measure_temp`
- Add heatsinks/fan if over 70°C

### No Audio
```bash
# Force HDMI audio
sudo amixer cset numid=3 2
# Or for 3.5mm jack
sudo amixer cset numid=3 1
```

## Power Requirements

- Pi 4: 3A USB-C power supply
- Pi 3B+: 2.5A micro-USB power supply
- Pi Zero 2 W: 1.5A micro-USB power supply

Always use official Raspberry Pi power supplies for stability!