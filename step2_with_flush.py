print("="*70, flush=True)
print("STEP 2: BILINGUAL DATA INGESTION", flush=True)
print("="*70 + "\n", flush=True)

# Generate bilingual synthetic data
print("🌏 Generating BILINGUAL synthetic PDPL dataset (70% Vietnamese + 30% English)...", flush=True)

import json
import random
from datetime import datetime

# PDPL Categories
PDPL_CATEGORIES_VI = {
    0: "Tính hợp pháp, công bằng và minh bạch",
    1: "Hạn chế mục đích",
    2: "Tối thiểu hóa dữ liệu",
    3: "Tính chính xác",
    4: "Hạn chế lưu trữ",
    5: "Tính toàn vẹn và bảo mật",
    6: "Trách nhiệm giải trình",
    7: "Quyền của chủ thể dữ liệu"
}

PDPL_CATEGORIES_EN = {
    0: "Lawfulness, fairness and transparency",
    1: "Purpose limitation",
    2: "Data minimization",
    3: "Accuracy",
    4: "Storage limitation",
    5: "Integrity and confidentiality",
    6: "Accountability",
    7: "Data subject rights"
}

# Vietnamese companies
VIETNAMESE_COMPANIES = ['VNG', 'FPT', 'Viettel', 'Shopee', 'Lazada', 'Tiki',
                        'VPBank', 'Techcombank', 'Grab', 'MoMo', 'ZaloPay']

# English companies
ENGLISH_COMPANIES = ['TechCorp', 'DataSystems Inc', 'SecureData Ltd', 'InfoProtect Co',
                     'CloudVault', 'PrivacyFirst Inc', 'SafeData Solutions', 'DataGuard Corp',
                     'TrustBank', 'SecureFinance Ltd', 'E-Commerce Global', 'OnlineMarket Inc']

# Vietnamese templates by region
TEMPLATES_VI = {
    0: {
        'bac': ["Công ty {company} cần phải thu thập dữ liệu cá nhân một cách hợp pháp, công bằng và minh bạch theo quy định của PDPL 2025.",
                "Các tổ chức cần phải đảm bảo tính hợp pháp khi thu thập và xử lý dữ liệu cá nhân của khách hàng.",
                "Doanh nghiệp {company} cần phải thông báo rõ ràng cho chủ thể dữ liệu về mục đích thu thập thông tin."],
        'trung': ["Công ty {company} cần thu thập dữ liệu cá nhân hợp pháp và công khai theo luật PDPL.",
                  "Tổ chức cần bảo đảm công bằng trong việc xử lý thông tin khách hàng."],
        'nam': ["Công ty {company} cần thu thập dữ liệu của họ một cách hợp pháp và công bằng.",
                "Tổ chức cần đảm bảo minh bạch khi xử lý thông tin cá nhân."]
    },
    1: {
        'bac': ["Dữ liệu cá nhân chỉ được sử dụng cho các mục đích đã thông báo trước cho chủ thể dữ liệu.",
                "Công ty {company} cần phải hạn chế việc sử dụng dữ liệu theo đúng mục đích đã công bố."],
        'trung': ["Dữ liệu chỉ dùng cho mục đích đã nói với người dùng trước đó.",
                  "Công ty {company} cần giới hạn việc dùng dữ liệu theo mục đích ban đầu."],
        'nam': ["Dữ liệu của họ chỉ được dùng cho mục đích đã nói trước.",
                "Công ty {company} cần hạn chế dùng dữ liệu đúng mục đích."]
    },
    2: {
        'bac': ["Công ty {company} chỉ nên thu thập dữ liệu cá nhân cần thiết cho mục đích cụ thể.",
                "Tổ chức cần phải hạn chế thu thập dữ liệu ở mức tối thiểu cần thiết."],
        'trung': ["Công ty {company} chỉ nên lấy dữ liệu cần thiết cho mục đích cụ thể.",
                  "Tổ chức cần hạn chế thu thập dữ liệu ở mức tối thiểu."],
        'nam': ["Công ty {company} chỉ nên lấy dữ liệu của họ khi thực sự cần.",
                "Tổ chức cần hạn chế lấy thông tin ở mức tối thiểu."]
    },
    3: {
        'bac': ["Công ty {company} phải đảm bảo dữ liệu cá nhân được cập nhật chính xác và kịp thời.",
                "Dữ liệu không chính xác cần được sửa chữa hoặc xóa ngay lập tức."],
        'trung': ["Công ty {company} phải đảm bảo dữ liệu cá nhân được cập nhật chính xác.",
                  "Dữ liệu sai cần được sửa hoặc xóa ngay."],
        'nam': ["Công ty {company} phải đảm bảo dữ liệu của họ được cập nhật đúng.",
                "Dữ liệu sai của họ cần được sửa hoặc xóa ngay."]
    },
    4: {
        'bac': ["Công ty {company} chỉ được lưu trữ dữ liệu cá nhân trong thời gian cần thiết.",
                "Tổ chức phải xóa dữ liệu cá nhân khi không còn mục đích sử dụng hợp pháp."],
        'trung': ["Công ty {company} chỉ được lưu dữ liệu cá nhân trong thời gian cần thiết.",
                  "Tổ chức phải xóa dữ liệu khi không còn dùng nữa."],
        'nam': ["Công ty {company} chỉ được lưu dữ liệu của họ trong thời gian cần.",
                "Tổ chức phải xóa dữ liệu của họ khi không dùng nữa."]
    },
    5: {
        'bac': ["Công ty {company} phải bảo vệ dữ liệu cá nhân khỏi truy cập trái phép.",
                "Các biện pháp bảo mật thích hợp cần được áp dụng để bảo vệ dữ liệu."],
        'trung': ["Công ty {company} phải bảo vệ dữ liệu cá nhân khỏi truy cập trái phép.",
                  "Biện pháp bảo mật cần được áp dụng để bảo vệ dữ liệu."],
        'nam': ["Công ty {company} phải bảo vệ dữ liệu của họ khỏi truy cập trái phép.",
                "Biện pháp bảo mật cần được dùng để bảo vệ dữ liệu của họ."]
    },
    6: {
        'bac': ["Công ty {company} phải chịu trách nhiệm về việc tuân thủ các quy định PDPL.",
                "Tổ chức cần có hồ sơ chứng minh việc tuân thủ bảo vệ dữ liệu cá nhân."],
        'trung': ["Công ty {company} phải chịu trách nhiệm về việc tuân thủ PDPL.",
                  "Tổ chức cần có hồ sơ chứng minh tuân thủ bảo vệ dữ liệu."],
        'nam': ["Công ty {company} phải chịu trách nhiệm về việc tuân thủ PDPL.",
                "Tổ chức cần có hồ sơ chứng minh họ tuân thủ bảo vệ dữ liệu."]
    },
    7: {
        'bac': ["Chủ thể dữ liệu có quyền truy cập, sửa đổi hoặc xóa dữ liệu cá nhân của mình.",
                "Công ty {company} phải tôn trọng quyền của người dùng đối với dữ liệu cá nhân."],
        'trung': ["Chủ thể dữ liệu có quyền truy cập, sửa hoặc xóa dữ liệu của mình.",
                  "Công ty {company} phải tôn trọng quyền của người dùng về dữ liệu."],
        'nam': ["Chủ thể dữ liệu có quyền xem, sửa hoặc xóa dữ liệu của họ.",
                "Công ty {company} phải tôn trọng quyền của họ về dữ liệu cá nhân."]
    }
}

# English templates by style
TEMPLATES_EN = {
    0: {
        'formal': ["Company {company} must collect personal data in a lawful, fair and transparent manner in accordance with PDPL 2025.",
                   "Organizations need to ensure lawfulness when collecting and processing customer personal data."],
        'business': ["Company {company} needs to collect data legally and fairly according to PDPL standards.",
                     "Organizations should ensure fairness when handling customer information."]
    },
    1: {
        'formal': ["Personal data may only be used for purposes previously disclosed to the data subject.",
                   "Company {company} must limit data usage to stated purposes only."],
        'business': ["Data can only be used for purposes already told to users.",
                     "Company {company} needs to limit data use to original purposes."]
    },
    2: {
        'formal': ["Company {company} should only collect personal data necessary for specific purposes.",
                   "Organizations must limit data collection to the minimum necessary."],
        'business': ["Company {company} should only collect data needed for specific purposes.",
                     "Organizations need to limit data collection to minimum levels."]
    },
    3: {
        'formal': ["Company {company} must ensure personal data is updated accurately and timely.",
                   "Inaccurate data must be corrected or deleted immediately."],
        'business': ["Company {company} must ensure personal data is updated correctly.",
                     "Wrong data needs to be fixed or deleted right away."]
    },
    4: {
        'formal': ["Company {company} may only store personal data for the necessary period.",
                   "Organizations must delete personal data when there is no longer a lawful purpose."],
        'business': ["Company {company} can only store personal data for necessary time.",
                     "Organizations must delete data when no longer needed."]
    },
    5: {
        'formal': ["Company {company} must protect personal data from unauthorized access.",
                   "Appropriate security measures must be applied to protect data."],
        'business': ["Company {company} must protect personal data from unauthorized access.",
                     "Security measures need to be used to protect data."]
    },
    6: {
        'formal': ["Company {company} must be responsible for compliance with PDPL regulations.",
                   "Organizations need records proving personal data protection compliance."],
        'business': ["Company {company} must be accountable for PDPL compliance.",
                     "Organizations need records proving data protection compliance."]
    },
    7: {
        'formal': ["Data subjects have the right to access, modify or delete their personal data.",
                   "Company {company} must respect users' rights to personal data."],
        'business': ["Data subjects have right to access, modify or delete their data.",
                     "Company {company} must respect users' rights to personal data."]
    }
}

# Generate bilingual dataset (70% Vietnamese, 30% English)
num_samples = 5000
vietnamese_samples = int(num_samples * 0.7)  # 3500
english_samples = num_samples - vietnamese_samples  # 1500

dataset = []

# Generate Vietnamese examples (70%)
print(f"🇻🇳 Generating {vietnamese_samples} Vietnamese examples (PRIMARY - 70%)...", flush=True)
vi_per_category = vietnamese_samples // 8
vi_per_region = vi_per_category // 3

for category in range(8):
    for region in ['bac', 'trung', 'nam']:
        templates = TEMPLATES_VI.get(category, {}).get(region, [])
        for _ in range(vi_per_region):
            template = random.choice(templates)
            company = random.choice(VIETNAMESE_COMPANIES)
            text = template.format(company=company)

            dataset.append({
                'text': text,
                'label': category,
                'category_name_vi': PDPL_CATEGORIES_VI[category],
                'category_name_en': PDPL_CATEGORIES_EN[category],
                'language': 'vi',
                'region': region,
                'source': 'synthetic',
                'quality': 'controlled'
            })

# Generate English examples (30%)
print(f"🇬🇧 Generating {english_samples} English examples (SECONDARY - 30%)...", flush=True)
en_per_category = english_samples // 8
en_per_style = en_per_category // 2

for category in range(8):
    for style in ['formal', 'business']:
        templates = TEMPLATES_EN.get(category, {}).get(style, [])
        for _ in range(en_per_style):
            template = random.choice(templates)
            company = random.choice(ENGLISH_COMPANIES)
            text = template.format(company=company)

            dataset.append({
                'text': text,
                'label': category,
                'category_name_vi': PDPL_CATEGORIES_VI[category],
                'category_name_en': PDPL_CATEGORIES_EN[category],
                'language': 'en',
                'style': style,
                'source': 'synthetic',
                'quality': 'controlled'
            })

# Shuffle
random.shuffle(dataset)

# Split: 70% train, 15% val, 15% test
train_size = int(0.7 * len(dataset))
val_size = int(0.15 * len(dataset))

train_data = dataset[:train_size]
val_data = dataset[train_size:train_size + val_size]
test_data = dataset[train_size + val_size:]

# Count languages in each split
def count_languages(data):
    vi_count = sum(1 for item in data if item.get('language') == 'vi')
    en_count = sum(1 for item in data if item.get('language') == 'en')
    return vi_count, en_count

train_vi, train_en = count_languages(train_data)
val_vi, val_en = count_languages(val_data)
test_vi, test_en = count_languages(test_data)

# Save to JSONL
import os
os.makedirs('data', exist_ok=True)
print("📁 Created 'data' directory", flush=True)

with open('data/train.jsonl', 'w', encoding='utf-8') as f:
    for item in train_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

with open('data/val.jsonl', 'w', encoding='utf-8') as f:
    for item in val_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

with open('data/test.jsonl', 'w', encoding='utf-8') as f:
    for item in test_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

# Verify files created
files_created = [
    ('data/train.jsonl', os.path.exists('data/train.jsonl')),
    ('data/val.jsonl', os.path.exists('data/val.jsonl')),
    ('data/test.jsonl', os.path.exists('data/test.jsonl'))
]
print("\n📋 File verification:", flush=True)
for filename, exists in files_created:
    status = "✅" if exists else "❌"
    print(f"   {status} {filename}", flush=True)

if not all(exists for _, exists in files_created):
    raise FileNotFoundError("Failed to create data files!")

print(f"\n✅ Bilingual synthetic dataset generated:", flush=True)
print(f"   Train: {len(train_data)} examples ({train_vi} VI + {train_en} EN)", flush=True)
print(f"   Validation: {len(val_data)} examples ({val_vi} VI + {val_en} EN)", flush=True)
print(f"   Test: {len(test_data)} examples ({test_vi} VI + {test_en} EN)", flush=True)
print(f"   Total: {len(dataset)} examples", flush=True)
print(f"\n📊 Language Distribution:", flush=True)
print(f"   Vietnamese (PRIMARY): {train_vi + val_vi + test_vi} ({(train_vi + val_vi + test_vi) / len(dataset) * 100:.1f}%)", flush=True)
print(f"   English (SECONDARY):  {train_en + val_en + test_en} ({(train_en + val_en + test_en) / len(dataset) * 100:.1f}%)", flush=True)

print("\n✅ Bilingual data ingestion complete!\n", flush=True)