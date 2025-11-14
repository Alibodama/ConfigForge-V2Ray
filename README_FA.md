🌐 در دسترس به: [English](README.md) | [فارسی](README_FA.md) | [Русский](README_ru.md) | [中文](README_zh.md)

# 🌍 ConfigForge V2Ray

یک پلتفرم متن‌باز پیشرفته است که کانفیگ‌های V2Ray را از منابع مختلف جمع‌آوری و بهینه‌سازی می‌کند.  
این ابزار به‌طور خودکار کشور شما را تشخیص می‌دهد و سریع‌ترین کانفیگ‌ها را پیشنهاد می‌دهد؛ این پیشنهادها با استفاده از **API سرویس Check-Host** تست می‌شوند تا بهترین سرعت و پایداری اتصال را تضمین کنند.

---

## 🌐 دسترسی به وب‌اینترفیس

### اشتراک‌های سریع برای ایران (لینک مستقیم)
از این لینک‌ها می‌توانید در هر کلاینت سازگار با V2Ray (مثل v2rayNG، V2RayN، Shadowrocket و ...) استفاده کنید.  
کافیست لینک را کپی کنید و در بخش **Subscriptions** کلاینت قرار دهید.

| فایل | توضیح | لینک مستقیم |
|---|---|---|
| `all.txt` | لیست کامل ایران (مرتب‌شده بر اساس میانگین تاخیر) | [باز کردن](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ir/all.txt) · [Mirror](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ir/all.txt) |
| `light.txt` | ۳۰ کانفیگ سریع ایران | [باز کردن](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ir/light.txt) · [Mirror](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ir/light.txt) |
| `vless.txt` | لیست فقط VLESS | [باز کردن](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ir/vless.txt) · [Mirror](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ir/vless.txt) |
| `vmess.txt` | لیست فقط VMess | [باز کردن](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ir/vmess.txt) · [Mirror](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ir/vmess.txt) |
| `shadowsocks.txt` | لیست فقط Shadowsocks | [باز کردن](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ir/shadowsocks.txt) · [Mirror](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ir/shadowsocks.txt) |
| `trojan.txt` | لیست فقط Trojan | [باز کردن](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ir/trojan.txt) · [Mirror](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ir/trojan.txt) |
| `unknown.txt` | پروتکل‌های ناشناخته | [باز کردن](https://raw.githubusercontent.com/Alibodama/ConfigForge-V2Ray/main/configs/ir/unknown.txt) · [Mirror](https://cdn.jsdelivr.net/gh/Alibodama/ConfigForge-V2Ray@main/configs/ir/unknown.txt) |

---

## 🚀 چرا ConfigForge؟
برخلاف مخزن‌های ساده، **ConfigForge V2Ray**:
- ✅ به‌طور مداوم کانفیگ‌ها را از منابع مختلف جمع‌آوری می‌کند  
- ✅ تاخیر هر کشور را با استفاده از [Check-Host API](https://check-host.net/) تست می‌کند  
- ✅ سریع‌ترین سرورها را متناسب با موقعیت شما پیشنهاد می‌دهد  
- ✅ کانفیگ‌ها را در قالب فایل‌های سبک و دسته‌بندی‌شده (VLESS، VMess، Shadowsocks، Trojan) ارائه می‌دهد  
- ✅ به‌صورت خودکار با GitHub Actions اجرا می‌شود – بدون نیاز به سرور!

---

## ✨ ویژگی‌ها
- 🌍 انتخاب بر اساس کشور – تشخیص خودکار یا انتخاب دستی  
- 🔍 پیشنهاد سرورهای تست‌شده – فقط سریع‌ترین و پایدارترین‌ها  
- 🌐 پشتیبانی چندزبانه – رابط کاربری با ترجمه پویا  
- 📂 فایل‌های اشتراک آماده:  
  - لیست کامل کانفیگ‌ها  
  -  ۳۰ کانفیگ برتر  
  - فایل‌های جدا برای هر پروتکل (VLESS, VMess, Shadowsocks, Trojan)  
- 🔄 به‌روزرسانی خودکار با GitHub Actions  
- ⚡ بهینه برای سرعت و سادگی  
- 🛠 قابلیت توسعه آسان برای پروتکل‌ها یا منابع جدید  

---

## 🛠 نحوه استفاده

### ✅ روش ۱: اجرا روی سیستم شخصی
ابتدا ریپازیتوری را کلون کنید:
```bash
git clone https://github.com/Alibodama/ConfigForge.git
cd ConfigForge
```

نصب پیش‌نیازها:
```bash
pip install -r source/requirements.txt
```

اجرای اسکریپت اصلی:
```bash
python source/main.py
```

### ✅ روش ۲: اجرای خودکار روی GitHub (بدون سرور)
کافیست ریپو را **Fork** کنید و اجازه دهید **GitHub Actions** همه کارها را انجام دهد!  

---

## ⭐ محبوبیت پروژه
![Stargazers over time](https://starchart.cc/Alibodama/ConfigForge-V2Ray.svg?variant=adaptive)

---
این پروژه تحت مجوز **GPL-3.0** منتشر شده است.  
