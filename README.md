# 樹莓派 OLED 即時系統監控器

<div align="center">
  <img src="https://img.shields.io/badge/Raspberry%20Pi-Zero%202W-red" alt="Raspberry Pi Zero 2W">
  <img src="https://img.shields.io/badge/Display-SSD1306%20128x64-blue" alt="SSD1306">
  <img src="https://img.shields.io/badge/Language-Python%203-green" alt="Python 3">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</div>

<p align="center">
  <img src="IMG_5143.png" width="400" alt="OLED 實際顯示畫面">
</p>

## 📖 專案介紹

這是一個即時系統監控器，專為樹莓派 Zero 2W 設計，使用 128x64 SSD1306 I2C OLED 顯示器，讓您隨時掌握系統狀態。

### ✨ 功能特色

- 🌐 顯示本機 IP 位址
- 🔧 CPU 使用率即時監測
- 🌡️ CPU 溫度顯示（超過 80°C 會閃爍警告）
- 📊 RAM 使用率監控
- 💾 SWAP 使用率監控
- ⚡ 每 0.5 秒自動刷新

## 🔧 硬體需求

- Raspberry Pi Zero 2W（也適用於 Pi 3 / Pi 4 / Pi 5）
- SSD1306 128x64 I2C OLED 顯示器

## 🔌 接線方式（I2C）

| OLED 腳位 | 樹莓派 Zero 2W 腳位 |
|-----------|-------------------|
| GND | Pin 6 (GND) |
| VCC | Pin 1 (3.3V) ⚠️**不可接 5V** |
| SDA | Pin 3 (GPIO2) |
| SCL | Pin 5 (GPIO3) |

> **I2C Address**：`0x3C`  
> **I2C Bus**：`/dev/i2c-1`

## 🚀 快速開始

### 1️⃣ 啟用 I2C

在終端輸入以下指令：

```bash
sudo raspi-config
```

選擇 **Interface Options** → **I2C** → **Enable**  
然後重開機：

```bash
sudo reboot
```

### 2️⃣ 偵測 OLED

安裝 I2C 工具：

```bash
sudo apt install -y i2c-tools
```

掃描 I2C bus：

```bash
i2cdetect -y 1
```

如果看到 `3c`，代表 OLED 已成功連接。

### 3️⃣ 安裝專案

下載專案：

```bash
git clone https://github.com/drownedfish71/rpi-oled-monitor.git
cd rpi-oled-monitor
```

給安裝腳本執行權限：

```bash
chmod +x install.sh
```

執行安裝腳本（會自動建立虛擬環境並安裝套件）：

```bash
./install.sh
```

或者手動安裝：

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4️⃣ 執行程式

```bash
# 進入虛擬環境
source venv/bin/activate

# 執行程式
python oled-monitor.py
```

## ⚙️ 開機自動執行（選用）

建立 systemd 服務：

```bash
sudo nano /etc/systemd/system/oled.service
```

貼入以下內容（請根據您的實際路徑修改）：

```ini
[Unit]
Description=OLED Monitor
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/rpi-oled-monitor
ExecStart=/home/pi/rpi-oled-monitor/venv/bin/python /home/pi/rpi-oled-monitor/oled-monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

啟用服務：

```bash
sudo systemctl daemon-reload
sudo systemctl enable oled.service
sudo systemctl start oled.service
```

查看服務狀態：

```bash
sudo systemctl status oled.service
```

## 📁 專案結構

```
rpi-oled-monitor/
├── oled-monitor.py     # 主程式
├── requirements.txt    # Python 套件需求
├── install.sh         # 自動安裝腳本
├── README.md          # 說明文件
├── IMG_5143.png       # 實際顯示照片
├── LICENSE             # 授權條款
└── venv/              # 虛擬環境（安裝後產生）
```

## 🔍 疑難排解

### OLED 無顯示
- 檢查接線是否正確
- 確認 I2C 已啟用
- 執行 `i2cdetect -y 1` 確認 OLED 位址
- Zero 2W 的 3.3V 電流足夠驅動 OLED

### 溫度顯示異常
- Zero 2W 正常溫度範圍 40-60°C
- 若無散熱片，滿載可能達 70-80°C

### 無法自動啟動
- 確認 systemd 服務檔案路徑正確
- 檢查執行權限
- 查看服務日誌：`sudo journalctl -u oled.service`

## 📝 授權條款

本專案採用 MIT 授權條款

## 🤝 貢獻指南

歡迎提交 Issues 和 Pull Requests！

## 📧 聯絡方式

專案連結：[https://github.com/drownedfish71/rpi-oled-monitor](https://github.com/drownedfish71/rpi-oled-monitor)

---

**如果這個專案對您有幫助，請給它一顆星星 ⭐**