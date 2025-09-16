#!/bin/bash
#
# WeatherStar 4000 Raspberry Pi Setup Script
# Configures a fresh Raspberry Pi to run WeatherStar 4000 on boot
#

echo "================================================"
echo "    WeatherStar 4000 Raspberry Pi Setup"
echo "    Perfect for CRT TVs (640x480 @ 4:3)"
echo "================================================"
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
echo "📦 Installing required packages..."
sudo apt-get install -y \
    python3-pip \
    python3-pygame \
    python3-pil \
    python3-requests \
    git \
    unzip \
    wget \
    python3-venv \
    xserver-xorg \
    xinit \
    x11-xserver-utils \
    chromium-browser

# Create weatherstar user if it doesn't exist
if ! id -u weatherstar >/dev/null 2>&1; then
    echo "👤 Creating weatherstar user..."
    sudo useradd -m -s /bin/bash weatherstar
    sudo usermod -aG video,audio weatherstar
fi

# Clone or update the repository
INSTALL_DIR="/home/weatherstar/WeatherStar4000"
if [ -d "$INSTALL_DIR" ]; then
    echo "📂 Updating existing installation..."
    cd "$INSTALL_DIR"
    sudo -u weatherstar git pull
else
    echo "📂 Cloning WeatherStar 4000..."
    sudo -u weatherstar git clone https://github.com/yourusername/Weather-Channel-G400-Python.git "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# Create virtual environment and install Python packages
echo "🐍 Setting up Python environment..."
sudo -u weatherstar python3 -m venv venv
sudo -u weatherstar venv/bin/pip install --upgrade pip
sudo -u weatherstar venv/bin/pip install pygame pillow requests

# Configure for CRT TV output (composite video)
echo "📺 Configuring for CRT TV output..."
sudo tee -a /boot/config.txt > /dev/null <<EOF

# WeatherStar 4000 CRT TV Configuration
# Disable HDMI, enable composite
hdmi_force_hotplug=0
hdmi_ignore_hotplug=1

# Set composite video mode
# For NTSC (USA/Canada):
sdtv_mode=0
sdtv_aspect=1

# For PAL (Europe):
# sdtv_mode=2
# sdtv_aspect=1

# Force 640x480 resolution
framebuffer_width=640
framebuffer_height=480

# Disable overscan for CRT
disable_overscan=0
overscan_left=20
overscan_right=20
overscan_top=10
overscan_bottom=10

# GPU memory split
gpu_mem=128

# Disable screen blanking
hdmi_blanking=0
EOF

# Create auto-start script
echo "🚀 Creating auto-start configuration..."
sudo tee /home/weatherstar/start_weatherstar.sh > /dev/null <<'EOF'
#!/bin/bash

# Wait for network
sleep 10

# Disable screen blanking
export DISPLAY=:0
xset s noblank
xset s off
xset -dpms

# Hide mouse cursor
unclutter -idle 0.5 -root &

# Change to WeatherStar directory
cd /home/weatherstar/WeatherStar4000

# Start WeatherStar 4000
/home/weatherstar/WeatherStar4000/venv/bin/python weatherstar4000.py

# If it crashes, restart after 5 seconds
sleep 5
exec "$0"
EOF

sudo chmod +x /home/weatherstar/start_weatherstar.sh
sudo chown weatherstar:weatherstar /home/weatherstar/start_weatherstar.sh

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/weatherstar.service > /dev/null <<EOF
[Unit]
Description=WeatherStar 4000 Weather Display
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=weatherstar
Group=weatherstar
WorkingDirectory=/home/weatherstar/WeatherStar4000
Environment="DISPLAY=:0"
ExecStart=/home/weatherstar/start_weatherstar.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create X11 auto-start for GUI
sudo tee /home/weatherstar/.xinitrc > /dev/null <<EOF
#!/bin/sh
exec /home/weatherstar/start_weatherstar.sh
EOF

sudo chown weatherstar:weatherstar /home/weatherstar/.xinitrc
sudo chmod +x /home/weatherstar/.xinitrc

# Configure auto-login for weatherstar user
echo "🔐 Configuring auto-login..."
sudo mkdir -p /etc/systemd/system/getty@tty1.service.d/
sudo tee /etc/systemd/system/getty@tty1.service.d/autologin.conf > /dev/null <<EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin weatherstar --noclear %I \$TERM
EOF

# Configure auto-start X on login
sudo tee -a /home/weatherstar/.bash_profile > /dev/null <<EOF

# Auto-start X and WeatherStar
if [ -z "\$DISPLAY" ] && [ "\$(tty)" = "/dev/tty1" ]; then
    exec startx
fi
EOF

# Create WiFi configuration helper
echo "📶 Creating WiFi configuration helper..."
sudo tee /home/weatherstar/setup_wifi.sh > /dev/null <<'EOF'
#!/bin/bash

echo "WeatherStar 4000 WiFi Setup"
echo "=========================="
echo ""

read -p "Enter WiFi network name (SSID): " SSID
read -s -p "Enter WiFi password: " PASSWORD
echo ""

# Save WiFi configuration
sudo tee /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null <<EOC
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="$SSID"
    psk="$PASSWORD"
    key_mgmt=WPA-PSK
}
EOC

echo "✅ WiFi configured for network: $SSID"
echo "Restarting network services..."
sudo systemctl restart networking
sudo systemctl restart wpa_supplicant

# Test connection
sleep 5
if ping -c 1 google.com &> /dev/null; then
    echo "✅ Internet connection successful!"
else
    echo "⚠️ Could not connect to internet. Please check your credentials."
fi
EOF

sudo chmod +x /home/weatherstar/setup_wifi.sh
sudo chown weatherstar:weatherstar /home/weatherstar/setup_wifi.sh

# Enable services
echo "✅ Enabling services..."
sudo systemctl daemon-reload
sudo systemctl enable weatherstar.service

# Create first-run configuration
echo "📝 Creating first-run configuration..."
sudo tee /home/weatherstar/WeatherStar4000/first_run.sh > /dev/null <<'EOF'
#!/bin/bash

echo "========================================="
echo "    WeatherStar 4000 First Run Setup"
echo "========================================="
echo ""
echo "Welcome! Let's configure your location."
echo ""

# Check for WiFi
if ! ping -c 1 google.com &> /dev/null; then
    echo "⚠️ No internet connection detected."
    echo "Please run: ~/setup_wifi.sh to configure WiFi"
    exit 1
fi

# Get location
read -p "Enter your ZIP code or city name: " LOCATION

# Save to settings
cat > ~/.weatherstar4000_settings.json <<EOC
{
  "location": {
    "auto_detect": false,
    "description": "$LOCATION"
  },
  "display": {
    "show_marine": false,
    "show_trends": true,
    "show_historical": true,
    "show_msn": true,
    "show_reddit": true,
    "show_local_news": true,
    "music_volume": 0.3
  }
}
EOC

echo "✅ Location set to: $LOCATION"
echo ""
echo "WeatherStar 4000 is now configured!"
echo "It will start automatically on next boot."
echo ""
echo "To change settings later, edit: ~/.weatherstar4000_settings.json"
echo "To reconfigure WiFi, run: ~/setup_wifi.sh"
echo ""
read -p "Press Enter to reboot now, or Ctrl+C to exit..."
sudo reboot
EOF

sudo chmod +x /home/weatherstar/WeatherStar4000/first_run.sh
sudo chown -R weatherstar:weatherstar /home/weatherstar/WeatherStar4000

# Final message
echo ""
echo "================================================"
echo "    ✅ WeatherStar 4000 Setup Complete!"
echo "================================================"
echo ""
echo "📺 CRT TV Setup:"
echo "   - Connect composite video cable to 3.5mm jack"
echo "   - Yellow = Video, Red = Right Audio, White = Left Audio"
echo ""
echo "📶 WiFi Setup:"
echo "   Run: ~/setup_wifi.sh"
echo ""
echo "🎯 First Run:"
echo "   Run: ~/WeatherStar4000/first_run.sh"
echo ""
echo "🔄 The system will:"
echo "   1. Auto-login as 'weatherstar' user"
echo "   2. Auto-start WeatherStar 4000"
echo "   3. Display at 640x480 for CRT TVs"
echo "   4. Restart if it crashes"
echo ""
echo "Reboot now to test? (y/n)"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo reboot
fi