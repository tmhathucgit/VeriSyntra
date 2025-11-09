# Vietnamese Fonts for PDF Generation

This directory contains Vietnamese-compatible fonts for ROPA PDF generation.

## Required Fonts

**Noto Sans Vietnamese** (Recommended)
- Supports all Vietnamese diacritics: á à ả ã ạ ă â ê ô ơ ư đ
- Download from: https://fonts.google.com/noto/specimen/Noto+Sans
- License: SIL Open Font License (free for commercial use)

## Installation

### Option 1: Download from Google Fonts

1. Visit: https://fonts.google.com/noto/specimen/Noto+Sans
2. Click "Download family"
3. Extract the ZIP file
4. Copy these files to this directory:
   - `NotoSans-Regular.ttf`
   - `NotoSans-Bold.ttf` (optional, but recommended)
   - `NotoSans-Italic.ttf` (optional)

### Option 2: Use System Fonts (Windows)

If you have Noto Sans installed on Windows, create symlinks:

```powershell
# PowerShell (run as Administrator)
$systemFonts = "C:\Windows\Fonts"
$projectFonts = "C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\backend\veri_ai_data_inventory\exporters\fonts"

New-Item -ItemType SymbolicLink -Path "$projectFonts\NotoSans-Regular.ttf" -Target "$systemFonts\NotoSans-Regular.ttf"
New-Item -ItemType SymbolicLink -Path "$projectFonts\NotoSans-Bold.ttf" -Target "$systemFonts\NotoSans-Bold.ttf"
```

## Verification

After placing fonts, verify with Python:

```python
from pathlib import Path

font_dir = Path(__file__).parent / "fonts"
regular = font_dir / "NotoSans-Regular.ttf"
bold = font_dir / "NotoSans-Bold.ttf"

print(f"Regular font exists: {regular.exists()}")
print(f"Bold font exists: {bold.exists()}")
```

## Fallback Behavior

If Vietnamese fonts are not found:
- PDF generator will use **Helvetica** (built-in font)
- Vietnamese diacritics will display as **"?"** or **missing characters**
- Warning message logged: `[WARNING] Vietnamese font not found`

## File Structure

```
fonts/
├── README.md                  # This file
├── NotoSans-Regular.ttf       # Main font (REQUIRED)
├── NotoSans-Bold.ttf          # Bold variant (recommended)
└── NotoSans-Italic.ttf        # Italic variant (optional)
```

## Testing Vietnamese Diacritics

Test characters that require proper font:
- Lowercase vowels: à á ả ã ạ ă ắ ằ ẳ ẵ ặ â ấ ầ ẩ ẫ ậ
- Uppercase vowels: À Á Ả Ã Ạ Ă Ắ Ằ Ẳ Ẵ Ặ Â Ấ Ầ Ẩ Ẫ Ậ
- Special: đ Đ ê ề ế ể ễ ệ ô ố ồ ổ ỗ ộ ơ ớ ờ ở ỡ ợ ư ứ ừ ử ữ ự

Example Vietnamese text for testing:
> **Bộ Công an** (Ministry of Public Security)  
> **Sổ đăng ký hoạt động xử lý dữ liệu cá nhân**  
> **Người bảo vệ dữ liệu** (Data Protection Officer)

If these display correctly in generated PDFs, font setup is successful!

## License

Noto Sans is licensed under the **SIL Open Font License 1.1**
- Free for commercial use
- Free to modify and distribute
- Font files NOT included in repository (download separately)

---

**Document #3 Section 6 Implementation**  
**VeriSyntra - Vietnamese PDPL 2025 Compliance Platform**
