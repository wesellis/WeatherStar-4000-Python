#!/bin/bash

echo "Building WeatherStar 4000+ v2.1.0 for Raspberry Pi..."
echo ""

VERSION="v2.1.0"
RELEASE_NAME="WeatherStar4000-${VERSION}-RaspberryPi"
RELEASE_DIR="${RELEASE_NAME}"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf ${RELEASE_DIR}
rm -f ${RELEASE_NAME}.tar.gz

# Create release directory
echo "Creating release directory..."
mkdir -p ${RELEASE_DIR}

# Copy all necessary files
echo "Copying application files..."
cp weatherstar4000.py ${RELEASE_DIR}/
cp -r weatherstar_modules ${RELEASE_DIR}/
cp -r weatherstar_assets ${RELEASE_DIR}/
cp requirements.txt ${RELEASE_DIR}/
cp README.md ${RELEASE_DIR}/
cp LICENSE ${RELEASE_DIR}/
cp RELEASE_NOTES.md ${RELEASE_DIR}/
cp run_weatherstar.sh ${RELEASE_DIR}/
cp setup_raspberry_pi.sh ${RELEASE_DIR}/

# Create installation script
cat > ${RELEASE_DIR}/install.sh << 'EOF'
#!/bin/bash

echo "================================================"
echo "WeatherStar 4000+ v2.1.0 Installer for Raspberry Pi"
echo "================================================"
echo ""

# Update system
echo "Updating system packages..."
sudo apt-get update

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y python3 python3-pip python3-pygame python3-pil python3-requests git

# Install Python packages
echo "Installing Python packages..."
pip3 install --user -r requirements.txt

# Make run script executable
chmod +x run_weatherstar.sh
chmod +x setup_raspberry_pi.sh

# Create desktop shortcut
if [ -d "$HOME/Desktop" ]; then
    cat > "$HOME/Desktop/WeatherStar4000.desktop" << DESKTOP
[Desktop Entry]
Name=WeatherStar 4000+
Comment=Weather Channel Simulator
Exec=$PWD/run_weatherstar.sh
Terminal=false
Type=Application
Icon=$PWD/weatherstar_assets/app_icons/weatherstar.png
Categories=Education;Science;
DESKTOP
    chmod +x "$HOME/Desktop/WeatherStar4000.desktop"
    echo "Desktop shortcut created!"
fi

# Create systemd service (optional)
echo ""
echo "Would you like to run WeatherStar at boot? (y/n)"
read -r answer
if [ "$answer" = "y" ]; then
    sudo bash -c "cat > /etc/systemd/system/weatherstar.service << SERVICE
[Unit]
Description=WeatherStar 4000+
After=graphical.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PWD
ExecStart=/usr/bin/python3 $PWD/weatherstar4000.py
Restart=always

[Install]
WantedBy=default.target
SERVICE"
    sudo systemctl daemon-reload
    sudo systemctl enable weatherstar.service
    echo "WeatherStar will start automatically at boot!"
fi

echo ""
echo "================================================"
echo "Installation complete!"
echo ""
echo "To run WeatherStar 4000+:"
echo "  ./run_weatherstar.sh"
echo ""
echo "Or use the desktop shortcut if available"
echo "================================================"
EOF

chmod +x ${RELEASE_DIR}/install.sh

# Create README for Raspberry Pi
cat > ${RELEASE_DIR}/README_PI.md << 'EOF'
# WeatherStar 4000+ for Raspberry Pi

## Quick Installation

1. Extract the archive:
   ```bash
   tar -xzf WeatherStar4000-v2.1.0-RaspberryPi.tar.gz
   cd WeatherStar4000-v2.1.0-RaspberryPi
   ```

2. Run the installer:
   ```bash
   ./install.sh
   ```

3. Start WeatherStar:
   ```bash
   ./run_weatherstar.sh
   ```

## Tested On
- Raspberry Pi 3B+
- Raspberry Pi 4
- Raspberry Pi Zero 2 W

## Display Settings
- Supports both HDMI and composite output
- Best with 640x480 or 800x600 resolution
- Full screen mode available (F11 key)

## Performance Tips
- Disable unnecessary services for better performance
- Use a Class 10 SD card or better
- Ensure proper cooling for extended use

## Troubleshooting
- If audio doesn't work: `sudo raspi-config` > Advanced Options > Audio
- For composite output: Edit /boot/config.txt and set sdtv_mode
- Black screen: Check HDMI cable and power supply

For more information, see the main README.md file.
EOF

# Create the tarball
echo "Creating release archive..."
tar -czf ${RELEASE_NAME}.tar.gz ${RELEASE_DIR}

# Calculate checksum
echo "Calculating checksum..."
sha256sum ${RELEASE_NAME}.tar.gz > ${RELEASE_NAME}.tar.gz.sha256

echo ""
echo "================================================"
echo "Raspberry Pi release build complete!"
echo ""
echo "Files created:"
echo "  - ${RELEASE_NAME}.tar.gz"
echo "  - ${RELEASE_NAME}.tar.gz.sha256"
echo ""
echo "Upload these to GitHub Releases"
echo "================================================"