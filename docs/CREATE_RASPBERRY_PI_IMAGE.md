# Creating a Raspberry Pi Image for WeatherStar 4000

## Option 1: Quick Setup (Using Existing Pi OS)

1. **Download Raspberry Pi OS Lite**
   ```bash
   # Download from: https://www.raspberrypi.com/software/operating-systems/
   # Choose: Raspberry Pi OS Lite (32-bit)
   ```

2. **Flash to SD Card**
   - Use Raspberry Pi Imager or Balena Etcher
   - Flash the OS to your SD card (8GB minimum)

3. **Enable SSH and WiFi (Optional)**
   - After flashing, mount the boot partition
   - Create `ssh` file (empty) to enable SSH
   - Create `wpa_supplicant.conf` with your WiFi details:
   ```
   country=US
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1

   network={
       ssid="YOUR_WIFI_NAME"
       psk="YOUR_WIFI_PASSWORD"
   }
   ```

4. **Boot and Run Setup**
   ```bash
   # SSH into your Pi (or use keyboard/monitor)
   ssh pi@raspberrypi.local
   # Default password: raspberry

   # Download and run setup
   wget https://raw.githubusercontent.com/yourusername/Weather-Channel-G400-Python/main/setup_raspberry_pi.sh
   chmod +x setup_raspberry_pi.sh
   ./setup_raspberry_pi.sh
   ```

## Option 2: Pre-Built Image (For Distribution)

### Creating the Master Image

1. **Start with Fresh Raspberry Pi OS Lite**
2. **Run the setup script**
3. **Configure everything**
4. **Clean up for distribution:**

```bash
# Remove personal data
rm -rf ~/.bash_history
rm -rf ~/.weatherstar4000_settings.json
rm -rf /home/weatherstar/.bash_history
sudo rm -rf /var/log/*
sudo rm -rf /tmp/*

# Clear WiFi passwords
sudo cp /dev/null /etc/wpa_supplicant/wpa_supplicant.conf

# Regenerate SSH keys on first boot
sudo rm -f /etc/ssh/ssh_host_*
sudo tee /etc/rc.local > /dev/null <<'EOF'
#!/bin/sh -e
# Regenerate SSH keys if missing
if [ ! -f /etc/ssh/ssh_host_rsa_key ]; then
    ssh-keygen -A
fi
exit 0
EOF
sudo chmod +x /etc/rc.local

# Shutdown
sudo shutdown -h now
```

### Creating the Image File

1. **On Another Linux Computer:**

```bash
# Insert SD card and find device (e.g., /dev/sdb)
sudo fdisk -l

# Create image (replace /dev/sdb with your SD card device)
sudo dd if=/dev/sdb of=weatherstar4000_v1.0.img bs=4M status=progress

# Compress the image
zip weatherstar4000_v1.0.zip weatherstar4000_v1.0.img

# Or use gzip
gzip -9 weatherstar4000_v1.0.img
```

2. **Shrink the Image (Optional):**

```bash
# Install PiShrink
wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
chmod +x pishrink.sh

# Shrink the image
sudo ./pishrink.sh weatherstar4000_v1.0.img

# This will resize the image to minimum size
```

## First Boot Instructions for End Users

### For Pre-Built Image Users:

1. **Flash the Image**
   - Download `weatherstar4000_v1.0.img.gz`
   - Use Raspberry Pi Imager or Balena Etcher
   - Flash to SD card (8GB minimum)

2. **Connect Your CRT TV**
   - Use 3.5mm to RCA cable
   - Yellow = Video
   - White = Left Audio
   - Red = Right Audio

3. **First Boot Setup**
   - Power on the Pi
   - Wait 2-3 minutes for first boot
   - Connect keyboard if needed

4. **Configure WiFi (if needed)**
   ```bash
   ~/setup_wifi.sh
   ```

5. **Configure Location**
   ```bash
   ~/WeatherStar4000/first_run.sh
   ```

6. **Enjoy!**
   - System will auto-start WeatherStar 4000
   - Press S for settings
   - Press Space to pause rotation

## Image Contents

The pre-built image includes:
- Raspberry Pi OS Lite (minimal)
- WeatherStar 4000 fully installed
- All Python dependencies
- Auto-start on boot configured
- CRT TV settings pre-configured
- 75+ music tracks included
- All weather icons and backgrounds

## System Requirements

- **Raspberry Pi**: 3B+, 4, or Zero 2W
- **SD Card**: 8GB minimum (16GB recommended)
- **Display**: CRT TV with composite input (or HDMI)
- **Internet**: WiFi or Ethernet for weather data

## Default Settings

- Resolution: 640x480 @ 60Hz
- Composite output: NTSC (change to PAL in /boot/config.txt)
- Audio: Enabled with background music
- Auto-start: Enabled
- User: weatherstar (auto-login)

## Troubleshooting

### No Display on CRT
- Check /boot/config.txt for correct sdtv_mode
- NTSC = 0, PAL = 2
- Ensure HDMI is disabled

### No Weather Data
- Check internet connection
- Run: `ping google.com`
- Configure WiFi: `~/setup_wifi.sh`

### Music Too Loud/Quiet
- Press M to mute/unmute
- Edit ~/.weatherstar4000_settings.json
- Change "music_volume" value (0.0 to 1.0)

## Creating Your Own Distribution

Feel free to create your own customized image with:
- Your location pre-configured
- Custom news sources enabled
- Different music selection
- Modified display rotation

Just follow the master image creation steps above!

---

## Download Links

Once created, the image will be available at:
- GitHub Releases page
- Direct download: ~500MB compressed
- Uncompressed size: ~2GB
- Works on all Pi models with 1GB+ RAM