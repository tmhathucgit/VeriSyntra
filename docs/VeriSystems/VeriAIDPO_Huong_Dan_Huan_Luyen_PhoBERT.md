# VeriAIDPO - Hướng Dẫn Huấn Luyện PhoBERT
## Cách Huấn Luyện PhoBERT trên Dữ Liệu PDPL 2025 Việt Nam

### **Tóm Tắt**

Tài liệu này cung cấp hướng dẫn chi tiết từng bước để huấn luyện PhoBERT trên bộ dữ liệu tuân thủ PDPL Việt Nam. Làm theo các bước này để tạo ra mô hình phân loại văn bản pháp lý tiếng Việt thành 8 nguyên tắc tuân thủ PDPL.

---

## **📋 Tổng Quan: Bạn Sẽ Xây Dựng Gì**

**Mục tiêu**: Huấn luyện PhoBERT để phân loại văn bản PDPL tiếng Việt vào các danh mục tuân thủ

**Đầu vào**: Văn bản tiếng Việt (VD: "Công ty phải bảo vệ dữ liệu cá nhân")
**Đầu ra**: Danh mục tuân thủ (VD: "Tối thiểu hóa dữ liệu") + độ tin cậy

**Quy Trình Huấn Luyện**:
```
Bước 1: Chuẩn bị dữ liệu (văn bản pháp lý PDPL + nhãn)
   ↓
Bước 2: Tiền xử lý với VnCoreNLP (tách từ tiếng Việt)
   ↓
Bước 3: Huấn luyện PhoBERT (học chuyển giao)
   ↓
Bước 4: Đánh giá mô hình (kiểm tra độ chính xác)
   ↓
Bước 5: Lưu & triển khai mô hình
```

---

## **Bước 1: Chuẩn Bị Dữ Liệu PDPL Việt Nam**

### **1.1 Cấu Trúc Dữ Liệu**

Tạo dữ liệu huấn luyện dạng JSONL (mỗi dòng 1 đối tượng JSON):

```jsonl
{"text": "Công ty phải thu thập dữ liệu một cách hợp pháp và minh bạch", "label": 0}
{"text": "Dữ liệu cá nhân chỉ được sử dụng cho mục đích đã thông báo", "label": 1}
{"text": "Chỉ thu thập dữ liệu cần thiết cho mục đích cụ thể", "label": 2}
{"text": "Dữ liệu phải chính xác và được cập nhật thường xuyên", "label": 3}
{"text": "Không lưu trữ dữ liệu lâu hơn thời gian cần thiết", "label": 4}
{"text": "Dữ liệu phải được mã hóa và bảo vệ an toàn", "label": 5}
{"text": "Doanh nghiệp chịu trách nhiệm về việc xử lý dữ liệu", "label": 6}
{"text": "Người dùng có quyền truy cập và xóa dữ liệu cá nhân", "label": 7}
```

### **1.2 Ánh Xạ Nhãn (8 Nguyên Tắc PDPL Việt Nam)**

**Quan trọng**: Sử dụng tiếng Việt làm ngôn ngữ chính, tiếng Anh làm phụ.

```python
# label_mapping.py
"""
Nhãn Danh Mục Tuân Thủ PDPL 2025 Việt Nam (Song Ngữ)
"""

# Nhãn tiếng Việt (sử dụng chính trong VeriPortal)
PDPL_NHAN_VI = {
    0: "Tính hợp pháp, công bằng và minh bạch",
    1: "Hạn chế mục đích",
    2: "Tối thiểu hóa dữ liệu",
    3: "Tính chính xác",
    4: "Hạn chế lưu trữ",
    5: "Tính toàn vẹn và bảo mật",
    6: "Trách nhiệm giải trình",
    7: "Quyền của chủ thể dữ liệu"
}

# Nhãn tiếng Anh (sử dụng phụ cho báo cáo quốc tế)
PDPL_NHAN_EN = {
    0: "Lawfulness, fairness and transparency",
    1: "Purpose limitation",
    2: "Data minimization",
    3: "Accuracy",
    4: "Storage limitation",
    5: "Integrity and confidentiality",
    6: "Accountability",
    7: "Rights of data subjects"
}

# Sử dụng tiếng Việt làm mặc định (ưu tiên văn hóa Việt Nam)
PDPL_NHAN = PDPL_NHAN_VI

# Ánh xạ ngược
NHAN_TO_ID = {v: k for k, v in PDPL_NHAN.items()}

# Hàm lấy nhãn theo ngôn ngữ
def lay_nhan(ma_nhan, ngon_ngu='vi'):
    """
    Lấy nhãn PDPL theo ngôn ngữ
    
    Tham số:
        ma_nhan (int): Mã nhãn (0-7)
        ngon_ngu (str): 'vi' cho tiếng Việt (mặc định), 'en' cho tiếng Anh
    
    Trả về:
        str: Nhãn theo ngôn ngữ đã chọn
    """
    if ngon_ngu == 'en':
        return PDPL_NHAN_EN[ma_nhan]
    else:
        return PDPL_NHAN_VI[ma_nhan]
```

**Tại sao thiết kế như vậy?**

1. ✅ **Tiếng Việt là ngôn ngữ chính** → Phù hợp với văn hóa và người dùng Việt Nam
2. ✅ **Tiếng Anh là ngôn ngữ phụ** → Hỗ trợ báo cáo quốc tế
3. ✅ **Dữ liệu huấn luyện bằng tiếng Việt** → PhoBERT học ngôn ngữ pháp lý Việt Nam
4. ✅ **Tôn trọng đa dạng vùng miền** → Hỗ trợ tiếng Việt Bắc, Trung, Nam

### **1.3 Tạo Tệp Huấn Luyện**

Tạo ba tệp trong thư mục `du_lieu/`:

```
du_lieu/
├── huan_luyen.jsonl     (70% dữ liệu, VD: 700 mẫu)
├── kiem_tra.jsonl       (15% dữ liệu, VD: 150 mẫu)
└── danh_gia.jsonl       (15% dữ liệu, VD: 150 mẫu)
```

**Kích thước dữ liệu tối thiểu**: 500-1000 mẫu cho kết quả tốt
**Khuyến nghị**: 2000+ mẫu cho chất lượng sản xuất

### **1.4 Đa Dạng Vùng Miền Việt Nam**

**Quan trọng**: Thu thập dữ liệu từ cả 3 miền để mô hình hiểu được sự đa dạng ngôn ngữ:

```python
# Ví dụ đa dạng vùng miền
du_lieu_mien = {
    'Miền Bắc': [
        "Doanh nghiệp phải đảm bảo dữ liệu được bảo mật",
        "Công ty cần tuân thủ quy định về bảo vệ dữ liệu cá nhân"
    ],
    'Miền Trung': [
        "Doanh nghiệp phải bảo đảm dữ liệu được bảo mật",
        "Công ty cần tuân thủ quy định bảo vệ dữ liệu cá nhân"
    ],
    'Miền Nam': [
        "Doanh nghiệp phải đảm bảo dữ liệu được bảo mật",
        "Công ty cần tuân thủ quy định về bảo vệ dữ liệu cá nhân"
    ]
}
```

**Lưu ý ngôn ngữ vùng miền**:
- **Miền Bắc**: "Cần phải", "đảm bảo", "quy định về"
- **Miền Trung**: "Cần", "bảo đảm", "quy định"  
- **Miền Nam**: "Cần", "đảm bảo", "quy định về"

---

## **❓ Câu Hỏi Thường Gặp: Tại Sao Mã Nhãn Dùng Số Thay Vì Chữ?**

### **Câu hỏi:**
> "Tại sao `label: 0` thay vì `label: "Tính hợp pháp"`?"

### **Trả lời:**

**Văn bản huấn luyện** (văn bản PhoBERT học) là **tiếng Việt**:
```jsonl
{"text": "Công ty phải bảo vệ dữ liệu cá nhân", "label": 5}  ← Văn bản tiếng Việt
```

**Nhãn** chỉ là **mã số** (0-7) đại diện cho các danh mục:

| Lý do | Giải thích |
|-------|------------|
| 🔧 **Kỹ thuật ML** | Các thư viện ML (PyTorch, scikit-learn) xử lý số nhanh hơn chữ |
| 💾 **Tiết kiệm bộ nhớ** | Số 0-7 (1 byte) < Chuỗi "Tính hợp pháp..." (40 bytes) |
| 🌍 **Tương thích quốc tế** | Dễ so sánh với nghiên cứu GDPR toàn cầu |
| 🎯 **Linh hoạt hiển thị** | Dễ dàng chuyển đổi giữa tiếng Việt và tiếng Anh |

### **Cách hoạt động:**

```
Giai đoạn huấn luyện (PhoBERT học gì):
┌─────────────────────────────────────────────────┐
│ Văn bản tiếng Việt → Mã nhãn                    │
│ "Công ty phải bảo vệ dữ liệu" → 5               │
│ "Dữ liệu phải chính xác" → 3                    │
│                                                 │
│ PhoBERT học các mẫu ngôn ngữ tiếng Việt!        │
└─────────────────────────────────────────────────┘

Giai đoạn dự đoán (Người dùng thấy gì):
┌─────────────────────────────────────────────────┐
│ Văn bản tiếng Việt → Mã nhãn → Hiển thị         │
│ "Dữ liệu phải mã hóa" → 5 → "Bảo mật" (VI)      │
│                            → "Integrity" (EN)    │
│                                                 │
│ Bạn chọn ngôn ngữ hiển thị cho người dùng!      │
└─────────────────────────────────────────────────┘
```

### **Thực hành tốt:**
- ✅ Dùng **mã số** trong code huấn luyện (hướng dẫn này)
- ✅ Hiển thị **tiếng Việt** cho người dùng Việt Nam (VeriPortal)
- ✅ Hiển thị **tiếng Anh** cho báo cáo/API quốc tế
- ✅ Dữ liệu huấn luyện **luôn bằng tiếng Việt** (PhoBERT học tiếng Việt!)

---

## **Bước 2: Cài Đặt Các Gói Cần Thiết**

### **2.1 Tạo Môi Trường Ảo**

```bash
# Tạo môi trường ảo
python -m venv veriaidpo-env

# Kích hoạt (Windows)
veriaidpo-env\Scripts\activate

# Kích hoạt (Linux/Mac)
source veriaidpo-env/bin/activate
```

### **2.2 Cài Đặt Các Gói**

```bash
# Cài đặt PyTorch (phiên bản CPU cho kiểm tra local)
pip install torch torchvision torchaudio

# Cài đặt Hugging Face Transformers
pip install transformers==4.35.0

# Cài đặt công cụ huấn luyện
pip install datasets==2.14.0
pip install accelerate==0.24.0
pip install scikit-learn==1.3.0

# Cài đặt VnCoreNLP (cho xử lý tiếng Việt)
pip install vncorenlp==1.0.3

# Tải VnCoreNLP JAR (một lần duy nhất)
# Windows PowerShell:
Invoke-WebRequest -Uri "https://github.com/vncorenlp/VnCoreNLP/raw/master/VnCoreNLP-1.2.jar" -OutFile "VnCoreNLP-1.2.jar"
```

### **2.3 Kiểm Tra Cài Đặt**

```python
# kiem_tra_cai_dat.py
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification

print(f"Phiên bản PyTorch: {torch.__version__}")
print(f"Phiên bản Transformers: {transformers.__version__}")
print(f"CUDA khả dụng: {torch.cuda.is_available()}")

# Kiểm tra tải PhoBERT
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
print("✅ Đã tải thành công tokenizer PhoBERT")
```

---

## **Bước 3: Tiền Xử Lý Dữ Liệu với VnCoreNLP**

### **3.1 Tại Sao Cần Tiền Xử Lý?**

Tách từ tiếng Việt cải thiện độ chính xác của PhoBERT:
- **Không tách từ**: "Công ty phải bảo vệ dữ liệu" → PhoBERT thấy các âm tiết
- **Có VnCoreNLP**: "Công_ty phải bảo_vệ dữ_liệu" → PhoBERT thấy các từ

**Cải thiện độ chính xác**: +5-10%

**Đặc biệt quan trọng cho tiếng Việt** vì:
- Tiếng Việt là ngôn ngữ đơn lập (từ ghép từ nhiều âm tiết)
- VD: "bảo vệ" (2 âm tiết) = 1 từ
- VnCoreNLP giúp PhoBERT hiểu ranh giới từ đúng

### **3.2 Script Tiền Xử Lý**

```python
# tien_xu_ly_du_lieu.py
"""
Tiền xử lý dữ liệu PDPL Việt Nam với VnCoreNLP
"""

from vncorenlp import VnCoreNLP
import json

# Khởi tạo VnCoreNLP
print("🔄 Đang khởi tạo VnCoreNLP...")
annotator = VnCoreNLP("./VnCoreNLP-1.2.jar", annotators="wseg", max_heap_size='-Xmx2g')
print("✅ Đã khởi tạo VnCoreNLP")

def tach_tu_tieng_viet(van_ban):
    """Tách từ văn bản tiếng Việt với VnCoreNLP"""
    tach = annotator.tokenize(van_ban)
    # Nối các từ bằng dấu gạch dưới
    xu_ly = ' '.join(['_'.join(cau) for cau in tach])
    return xu_ly

def xu_ly_tep(tep_dau_vao, tep_dau_ra):
    """Xử lý tệp JSONL"""
    so_dong = 0
    with open(tep_dau_vao, 'r', encoding='utf-8') as f_in:
        with open(tep_dau_ra, 'w', encoding='utf-8') as f_out:
            for dong in f_in:
                du_lieu = json.loads(dong)
                # Tách từ văn bản tiếng Việt
                du_lieu['text'] = tach_tu_tieng_viet(du_lieu['text'])
                # Ghi vào tệp đầu ra
                f_out.write(json.dumps(du_lieu, ensure_ascii=False) + '\n')
                so_dong += 1
    print(f"✅ Đã xử lý {so_dong} dòng: {tep_dau_vao} → {tep_dau_ra}")

# Xử lý tất cả các tệp
print("\n📊 Bắt đầu tiền xử lý dữ liệu...")
xu_ly_tep('du_lieu/huan_luyen.jsonl', 'du_lieu/huan_luyen_da_xu_ly.jsonl')
xu_ly_tep('du_lieu/kiem_tra.jsonl', 'du_lieu/kiem_tra_da_xu_ly.jsonl')
xu_ly_tep('du_lieu/danh_gia.jsonl', 'du_lieu/danh_gia_da_xu_ly.jsonl')

annotator.close()
print("\n✅ Hoàn tất tiền xử lý tất cả các tệp!")
```

**Chạy tiền xử lý:**
```bash
python tien_xu_ly_du_lieu.py
```

**Kết quả mong đợi:**
```
🔄 Đang khởi tạo VnCoreNLP...
✅ Đã khởi tạo VnCoreNLP

📊 Bắt đầu tiền xử lý dữ liệu...
✅ Đã xử lý 700 dòng: du_lieu/huan_luyen.jsonl → du_lieu/huan_luyen_da_xu_ly.jsonl
✅ Đã xử lý 150 dòng: du_lieu/kiem_tra.jsonl → du_lieu/kiem_tra_da_xu_ly.jsonl
✅ Đã xử lý 150 dòng: du_lieu/danh_gia.jsonl → du_lieu/danh_gia_da_xu_ly.jsonl

✅ Hoàn tất tiền xử lý tất cả các tệp!
```

---

## **Bước 4: Tải và Chuẩn Bị Dữ Liệu**

### **4.1 Tạo Bộ Tải Dữ Liệu**

```python
# tai_du_lieu.py
"""
Tải dữ liệu PDPL Việt Nam cho huấn luyện PhoBERT
"""

from datasets import load_dataset
from transformers import AutoTokenizer

# Tải tokenizer PhoBERT
print("📥 Đang tải tokenizer PhoBERT...")
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
print("✅ Đã tải tokenizer PhoBERT")

# Tải dữ liệu từ các tệp JSONL
print("\n📂 Đang tải dữ liệu...")
bo_du_lieu = load_dataset('json', data_files={
    'train': 'du_lieu/huan_luyen_da_xu_ly.jsonl',
    'validation': 'du_lieu/kiem_tra_da_xu_ly.jsonl',
    'test': 'du_lieu/danh_gia_da_xu_ly.jsonl'
})

print(f"✅ Đã tải dữ liệu:")
print(f"  Huấn luyện: {len(bo_du_lieu['train'])} mẫu")
print(f"  Kiểm tra: {len(bo_du_lieu['validation'])} mẫu")
print(f"  Đánh giá: {len(bo_du_lieu['test'])} mẫu")

# Hàm tokenize
def ham_tokenize(cac_mau):
    """Tokenize văn bản tiếng Việt cho PhoBERT"""
    return tokenizer(
        cac_mau['text'],
        padding='max_length',
        truncation=True,
        max_length=256  # Độ dài chuỗi tối đa
    )

# Tokenize tất cả dữ liệu
print("\n🔄 Đang tokenize dữ liệu...")
bo_du_lieu_tokenized = bo_du_lieu.map(ham_tokenize, batched=True)

# Xóa cột văn bản gốc (giữ input_ids, attention_mask đã tokenize)
bo_du_lieu_tokenized = bo_du_lieu_tokenized.remove_columns(['text'])

# Đổi tên 'label' thành 'labels' (yêu cầu bởi Trainer)
bo_du_lieu_tokenized = bo_du_lieu_tokenized.rename_column('label', 'labels')

print("✅ Dữ liệu đã được tokenize và sẵn sàng cho huấn luyện")
```

---

## **Bước 5: Huấn Luyện PhoBERT**

### **5.1 Script Huấn Luyện (Tiếng Việt)**

```python
# huan_luyen_phobert.py
"""
Huấn luyện PhoBERT trên dữ liệu tuân thủ PDPL Việt Nam
"""

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from datasets import load_dataset
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Đặt seed ngẫu nhiên để tái tạo kết quả
torch.manual_seed(42)

print("="*60)
print("🇻🇳 HUẤN LUYỆN PHOBERT CHO PDPL VIỆT NAM 🇻🇳")
print("="*60)

# Tải tokenizer
print("\n📥 Đang tải tokenizer PhoBERT...")
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
print("✅ Đã tải tokenizer")

# Tải dữ liệu
print("\n📂 Đang tải dữ liệu...")
bo_du_lieu = load_dataset('json', data_files={
    'train': 'du_lieu/huan_luyen_da_xu_ly.jsonl',
    'validation': 'du_lieu/kiem_tra_da_xu_ly.jsonl',
    'test': 'du_lieu/danh_gia_da_xu_ly.jsonl'
})

print(f"✅ Đã tải dữ liệu:")
print(f"  📚 Huấn luyện: {len(bo_du_lieu['train'])} mẫu")
print(f"  🔍 Kiểm tra: {len(bo_du_lieu['validation'])} mẫu")
print(f"  📊 Đánh giá: {len(bo_du_lieu['test'])} mẫu")

# Hàm tokenize
def ham_tokenize(cac_mau):
    return tokenizer(
        cac_mau['text'],
        padding='max_length',
        truncation=True,
        max_length=256
    )

# Tokenize dữ liệu
print("\n🔄 Đang tokenize dữ liệu...")
bo_du_lieu_tokenized = bo_du_lieu.map(ham_tokenize, batched=True)
bo_du_lieu_tokenized = bo_du_lieu_tokenized.remove_columns(['text'])
bo_du_lieu_tokenized = bo_du_lieu_tokenized.rename_column('label', 'labels')
print("✅ Hoàn tất tokenize")

# Tải mô hình PhoBERT (8 lớp đầu ra cho 8 danh mục PDPL)
print("\n📥 Đang tải mô hình PhoBERT...")
mo_hinh = AutoModelForSequenceClassification.from_pretrained(
    "vinai/phobert-base",
    num_labels=8  # 8 nguyên tắc tuân thủ PDPL
)
print("✅ Đã tải mô hình PhoBERT")

# Data collator
du_lieu_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Định nghĩa metrics
def tinh_metrics(eval_pred):
    """Tính accuracy, precision, recall, F1"""
    du_doan, nhan = eval_pred
    du_doan = np.argmax(du_doan, axis=1)
    
    do_chinh_xac = accuracy_score(nhan, du_doan)
    do_chinh_xac_chi_tiet, recall, f1, _ = precision_recall_fscore_support(
        nhan, du_doan, average='weighted'
    )
    
    return {
        'do_chinh_xac': do_chinh_xac,
        'precision': do_chinh_xac_chi_tiet,
        'recall': recall,
        'f1': f1
    }

# Tham số huấn luyện (tối ưu cho PC Việt Nam)
tham_so_huan_luyen = TrainingArguments(
    output_dir='./phobert-pdpl-viet-nam',
    
    # Tham số huấn luyện
    num_train_epochs=5,              # Số epoch huấn luyện
    per_device_train_batch_size=16,  # Kích thước batch huấn luyện
    per_device_eval_batch_size=32,   # Kích thước batch đánh giá
    learning_rate=2e-5,              # Tốc độ học
    weight_decay=0.01,               # Weight decay (L2 regularization)
    warmup_steps=500,                # Bước khởi động cho learning rate
    
    # Đánh giá & lưu
    evaluation_strategy='epoch',     # Đánh giá mỗi epoch
    save_strategy='epoch',           # Lưu checkpoint mỗi epoch
    load_best_model_at_end=True,    # Tải mô hình tốt nhất sau huấn luyện
    metric_for_best_model='do_chinh_xac',  # Dùng độ chính xác để chọn mô hình tốt nhất
    
    # Logging
    logging_dir='./logs',
    logging_steps=100,
    
    # Hiệu suất
    fp16=torch.cuda.is_available(),  # Dùng mixed precision nếu có GPU
    dataloader_num_workers=0,        # Số worker tải dữ liệu
)

# Khởi tạo Trainer
print("\n🎯 Đang khởi tạo Trainer...")
trainer = Trainer(
    model=mo_hinh,
    args=tham_so_huan_luyen,
    train_dataset=bo_du_lieu_tokenized['train'],
    eval_dataset=bo_du_lieu_tokenized['validation'],
    tokenizer=tokenizer,
    data_collator=du_lieu_collator,
    compute_metrics=tinh_metrics,
)
print("✅ Đã khởi tạo Trainer")

# Huấn luyện mô hình
print("\n" + "="*60)
print("🚀 BẮT ĐẦU HUẤN LUYỆN PHOBERT...")
print("="*60 + "\n")

trainer.train()

# Đánh giá trên tập kiểm tra
print("\n" + "="*60)
print("📊 ĐÁNH GIÁ TRÊN TẬP KIỂM TRA...")
print("="*60 + "\n")

ket_qua_test = trainer.evaluate(bo_du_lieu_tokenized['test'])
print(f"\n✅ Kết quả kiểm tra:")
for ten_metric, gia_tri in ket_qua_test.items():
    print(f"  {ten_metric}: {gia_tri:.4f}")

# Lưu mô hình cuối cùng
print("\n💾 Đang lưu mô hình...")
trainer.save_model('./phobert-pdpl-viet-nam-final')
tokenizer.save_pretrained('./phobert-pdpl-viet-nam-final')

print("\n" + "="*60)
print("✅ HOÀN TẤT HUẤN LUYỆN!")
print("📁 Mô hình đã lưu tại: ./phobert-pdpl-viet-nam-final")
print("="*60)
```

### **5.2 Chạy Huấn Luyện**

```bash
# Bắt đầu huấn luyện (CPU - chậm hơn)
python huan_luyen_phobert.py

# HOẶC với GPU (nhanh hơn) - Linux/Mac
CUDA_VISIBLE_DEVICES=0 python huan_luyen_phobert.py

# HOẶC với GPU (nhanh hơn) - Windows PowerShell
$env:CUDA_VISIBLE_DEVICES="0"; python huan_luyen_phobert.py
```

**Thời gian huấn luyện dự kiến** (PC của bạn - Intel Iris Xe):
- **CPU**: 2.5-4 giờ (1000 mẫu, 5 epochs)
- **Google Colab GPU**: 15-30 phút (**Khuyến nghị!**)

---

## **📊 Thời Gian Huấn Luyện Dự Kiến (PC Việt Nam)**

### **PC Của Bạn: Intel Iris Xe Graphics**

| Phần cứng | Thời gian mỗi epoch | Tổng thời gian (5 epochs) |
|-----------|---------------------|---------------------------|
| **CPU (Intel)** | ~35-45 phút | **2.5-4 giờ** |
| **Đề xuất: Google Colab GPU** | ~3-4 phút | **15-30 phút** |

### **Chiến Lược Tối Ưu:**

1. ✅ **Kiểm tra với 100 mẫu đầu tiên** (20 phút trên PC)
   - Đảm bảo mọi thứ hoạt động
   - Kiểm tra PC có đủ khả năng

2. ✅ **Nếu kiểm tra thành công, chọn**:
   - **Kiên nhẫn**: Huấn luyện qua đêm trên PC (3-4 giờ, miễn phí)
   - **Nhanh chóng**: Dùng Google Colab GPU (30 phút, miễn phí)

3. ✅ **Cho sản xuất** (2000+ mẫu):
   - Dùng AWS SageMaker (xem `VeriAIDPO_ML_AWS_Training_Plan.md`)
   - Chi phí: ~$5-10 cho huấn luyện, 10-20 phút

---

## **🎯 Mẹo Để Kết Quả Tốt Hơn**

### **Chất Lượng Dữ Liệu**
- ✅ **Nhiều dữ liệu = độ chính xác cao hơn** (mục tiêu 2000+ mẫu)
- ✅ **Cân bằng các lớp** (số mẫu bằng nhau cho mỗi danh mục)
- ✅ **Ví dụ thực tế** (văn bản tuân thủ PDPL thực tế)
- ✅ **Đa dạng vùng miền** (Bắc, Trung, Nam Việt Nam)

### **Tối Ưu Huấn Luyện**
- ✅ **Dùng GPU** (nhanh hơn CPU 10-20 lần)
- ✅ **Tăng epochs** (5-10 epochs để hội tụ tốt hơn)
- ✅ **Điều chỉnh learning rate** (thử 1e-5, 2e-5, 3e-5)
- ✅ **Dùng VnCoreNLP preprocessing** (+5-10% độ chính xác)

### **Cải Thiện Mô Hình**
- ✅ **Thử PhoBERT-large** (độ chính xác cao hơn, chậm hơn)
- ✅ **Ensemble models** (kết hợp nhiều mô hình)
- ✅ **Data augmentation** (paraphrase, back-translation)
- ✅ **Active learning** (huấn luyện lại với các mẫu sai)

---

## **✅ Các Bước Tiếp Theo**

Sau khi huấn luyện mô hình:

1. ✅ **Triển khai lên AWS** (xem `VeriAIDPO_ML_AWS_Training_Plan.md`)
2. ✅ **Tích hợp với VeriPortal** (thêm vào compliance wizards)
3. ✅ **Học liên tục** (huấn luyện lại hàng tháng với dữ liệu mới)
4. ✅ **A/B testing** (so sánh với baseline)
5. ✅ **Chứng nhận ISO 42001** (ghi lại quy trình huấn luyện)

---

**Bạn đã sẵn sàng để huấn luyện PhoBERT trên dữ liệu PDPL Việt Nam!** 🚀🇻🇳

---

*Phiên bản tài liệu: 1.0*
*Cập nhật lần cuối: 5 tháng 10, 2025*
*Người sở hữu: Nhóm AI/ML VeriSyntra*
