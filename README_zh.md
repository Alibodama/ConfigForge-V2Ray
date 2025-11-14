🌐 提供语言: [English](README.md) | [فارسی](README_FA.md) | [Русский](README_ru.md) | [中文](README_zh.md)

# 🌍 ConfigForge V2Ray（中文）

**ConfigForge V2Ray** 是一个先进的开源平台，用于收集和优化来自多个来源的 V2Ray 配置。  
系统会自动检测您的所在地区，并推荐 **最快的节点**，通过 **Check-Host API 延迟测试** 验证，确保速度和稳定性。

---

## 🌐 网页界面

### 香港快速订阅（直接链接）
这些链接可以在任何支持 V2Ray 的客户端中使用（如 v2rayNG、V2RayN、Shadowrocket 等）。  
复制链接并粘贴到客户端的 **Subscriptions** 中即可。

| 文件 | 描述 | 链接 |
|---|---|---|
| `all.txt` | 香港完整列表（按延迟排序） | [打开](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/hk/all.txt) · [镜像](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/hk/all.txt) |
| `light.txt` | 香港最快 30 个节点 | [打开](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/hk/light.txt) · [镜像](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/hk/light.txt) |
| `vless.txt` | 仅 VLESS | [打开](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/hk/vless.txt) · [镜像](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/hk/vless.txt) |
| `vmess.txt` | 仅 VMess | [打开](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/hk/vmess.txt) · [镜像](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/hk/vmess.txt) |
| `shadowsocks.txt` | 仅 Shadowsocks | [打开](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/hk/shadowsocks.txt) · [镜像](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/hk/shadowsocks.txt) |
| `trojan.txt` | 仅 Trojan | [打开](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/hk/trojan.txt) · [镜像](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/hk/trojan.txt) |
| `unknown.txt` | 其他/未知协议 | [打开](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/hk/unknown.txt) · [镜像](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/hk/unknown.txt) |

---

## 🚀 为什么选择 ConfigForge?
与普通的配置仓库不同，**ConfigForge V2Ray**：
- ✅ 持续从多个来源获取配置  
- ✅ 使用 [Check-Host API](https://check-host.net/) 测试延迟  
- ✅ 根据地区推荐最快的服务器  
- ✅ 提供分类好的订阅文件（VLESS、VMess、Shadowsocks、Trojan）  
- ✅ 通过 GitHub Actions 自动运行，无需服务器！

---

## ✨ 功能特点
- 🌍 国家/地区选择 — 自动检测或手动选择  
- 🔍 延迟测试推荐 — 只保留最快可用节点  
- 🌐 多语言支持  
- 📂 订阅文件：  
  - `all.txt` → 完整列表  
  - `light.txt` → 前 30 个节点  
  - 各协议单独文件 (VLESS, VMess, Shadowsocks, Trojan)  
- 🔄 自动更新（GitHub Actions）  
- ⚡ 简单快速  
- 🛠 易于扩展和定制  

---

## 🛠 使用方法

### ✅ 方式一：本地运行
克隆仓库：
```bash
git clone https://github.com/Alibodama/ConfigForge.git
cd ConfigForge
```

安装依赖：
```bash
pip install -r source/requirements.txt
```

运行：
```bash
python source/main.py
```

### ✅ 方式二：在 GitHub 上自动运行（无需服务器）
只需 **Fork** 仓库并启用 GitHub Actions，一切将自动完成！  

---

## ⭐ 项目人气
![Stargazers over time](https://starchart.cc/Alibodama/ConfigForge-V2Ray.svg?variant=adaptive)

---
本项目使用 **GPL-3.0 协议** 发布。  
