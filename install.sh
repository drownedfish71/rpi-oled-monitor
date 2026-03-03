#!/bin/bash

# 樹莓派 OLED 監控器安裝腳本
echo "=================================="
echo "樹莓派 OLED 監控器安裝腳本"
echo "=================================="

# 檢查是否為樹莓派
if [ ! -f /etc/rpi-issue ]; then
    echo "⚠️ 警告：這似乎不是樹莓派系統"
    read -p "是否繼續？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 更新系統
echo "📦 更新系統套件..."
sudo apt update
sudo apt upgrade -y

# 安裝必要套件
echo "📦 安裝 I2C 工具和 Python 開發套件..."
sudo apt install -y python3-pip python3-venv i2c-tools python3-pil python3-numpy

# 啟用 I2C
echo "🔌 啟用 I2C 介面..."
sudo raspi-config nonint do_i2c 0

# 檢查 I2C 裝置
echo "🔍 檢查 I2C 裝置..."
if command -v i2cdetect &> /dev/null; then
    echo "I2C 掃描結果："
    sudo i2cdetect -y 1
else
    echo "⚠️ i2c-tools 未安裝"
fi

# 建立虛擬環境
echo "🐍 建立 Python 虛擬環境..."
python3 -m venv venv
source venv/bin/activate

# 安裝 Python 套件
echo "📦 安裝 Python 套件..."
pip install --upgrade pip
pip install psutil pillow Adafruit_SSD1306

# 建立 requirements.txt
cat > requirements.txt << EOF
psutil==5.9.0
pillow==9.5.0
Adafruit_SSD1306==1.6.2
EOF

# 測試執行
echo "🧪 測試 OLED 顯示（5秒後自動結束）..."
timeout 5 python monitor.py

echo ""
echo "=================================="
echo "✅ 安裝完成！"
echo "=================================="
echo ""
echo "👉 手動執行：python monitor.py"
echo "👉 開機自動執行：sudo systemctl enable oled.service"
echo ""