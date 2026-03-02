# rpi-oled-monitor
# 樹莓派 OLED 即時系統監控器

<div align="center">
  <img src="https://img.shields.io/badge/Raspberry%20Pi-Pi%204%20%7C%20Pi%205-red" alt="Raspberry Pi">
  <img src="https://img.shields.io/badge/Display-SSD1306%20128x64-blue" alt="SSD1306">
  <img src="https://img.shields.io/badge/Language-Python%203-green" alt="Python 3">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</div>

<p align="center">
  <img src="https://via.placeholder.com/400x200?text=OLED+Monitor+Demo" alt="Demo Preview">
</p>

## 📖 專案介紹

這是一個即時系統監控器，專為樹莓派設計，使用 128x64 SSD1306 I2C OLED 顯示器，讓您隨時掌握系統狀態。

### ✨ 功能特色

- 🌐 顯示本機 IP 位址
- 🔧 CPU 使用率即時監測
- 🌡️ CPU 溫度顯示（超過 80°C 會閃爍警告）
- 📊 RAM 使用率監控
- 💾 SWAP 使用率監控
- ⚡ 每 0.5 秒自動刷新

## 🔧 硬體需求

- Raspberry Pi（已測試於 Pi 4 / Pi 5）
- SSD1306 128x64 I2C OLED 顯示器

## 🔌 接線方式（I2C）

| OLED 腳位 | 樹莓派腳位 |
|-----------|------------|
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
git clone https://github.com/yourname/oled-monitor.git
cd oled-monitor
```

建立虛擬環境：

```bash
python3 -m venv venv
source venv/bin/activate
```

安裝套件：

```bash
pip install -r requirements.txt
```

**requirements.txt 內容**：
```
psutil
pillow
Adafruit_SSD1306
```

### 4️⃣ 執行程式

```bash
python monitor.py
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
WorkingDirectory=/home/pi/oled-monitor
ExecStart=/home/pi/oled-monitor/venv/bin/python /home/pi/oled-monitor/monitor.py
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
oled-monitor/
├── monitor.py          # 主程式
├── requirements.txt    # Python 套件需求
├── README.md          # 說明文件
└── venv/              # 虛擬環境
```

## 🔍 疑難排解

### OLED 無顯示
- 檢查接線是否正確
- 確認 I2C 已啟用
- 執行 `i2cdetect -y 1` 確認 OLED 位址

### 溫度顯示異常
- 確保樹莓派有散熱片
- 檢查溫度感測器是否正常

### 無法自動啟動
- 確認 systemd 服務檔案路徑正確
- 檢查執行權限
- 查看服務日誌：`sudo journalctl -u oled.service`

## 📝 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件

## 🤝 貢獻指南

歡迎提交 Issues 和 Pull Requests！

1. Fork 本專案
2. 建立您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的修改 (`git commit -m 'Add some AmazingFeature'`)
4. Push 到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📧 聯絡方式

專案連結：[https://github.com/yourname/oled-monitor](https://github.com/yourname/oled-monitor)

---

**如果這個專案對您有幫助，請給它一顆星星 ⭐**