# VeriAIDPO - Vietnamese PDPL Data Collection Guide
## Hybrid Approach Strategy for Production-Quality Dataset

> **🇻🇳 Vietnamese-First Data Collection**: This guide provides a comprehensive strategy for collecting 5,000+ Vietnamese PDPL compliance examples using a hybrid approach combining official sources, synthetic generation, and crowdsourcing.

---

## **Executive Summary**

**🎯 Goal**: Collect 4,500-5,000 Vietnamese PDPL examples for PhoBERT training  
**⏱️ Timeline**: 3-6 weeks (MVP) or 4-8 weeks (Production)  
**💰 Estimated Cost**: **$0 (MVP)** or **$1,500 (Production)**  
**🎯 Target Accuracy**: **90-93% (MVP)** or **95-97% (Production)**

---

### **🚀 MVP Path (Recommended for Prototype)**

**Perfect for**: Investor demo, proof of concept, initial testing, $0 budget

| Source | Examples | % of Total | Quality | Cost | Timeline |
|--------|----------|------------|---------|------|----------|
| **Official Documents** | 1,500 | 33% | High | Free | 2 weeks |
| **Media Articles** | 1,000 | 22% | Medium | Free | 1 week |
| **Business Documents** | 1,000 | 22% | Medium-High | Free | 1 week |
| **Synthetic Data** | 1,000 | 22% | Controlled | Free | 3 days |
| **MVP TOTAL** | **4,500** | **100%** | **Mixed** | **$0** | **3-4 weeks** |

**Expected Accuracy**: 90-93% across Vietnamese regions  
**When to use**: Pre-funding, demo stage, rapid prototyping

---

### **🎯 Production Path (Post-Funding)**

**Perfect for**: Enterprise customers, production launch, seed-funded startups

| Source | Examples | % of Total | Quality | Cost | Timeline |
|--------|----------|------------|---------|------|----------|
| **Official Documents** | 1,500 | 30% | High | Free | 2 weeks |
| **Media Articles** | 1,000 | 20% | Medium | Free | 1 week |
| **Business Documents** | 1,000 | 20% | Medium-High | Free | 1 week |
| **Synthetic Data** | 1,000 | 20% | Controlled | Free | 3 days |
| **Crowdsourced** ⭐ | 500 | 10% | Authentic | $1,500 | 2 weeks |
| **PRODUCTION TOTAL** | **5,000** | **100%** | **Premium** | **$1,500** | **4-6 weeks** |

**Expected Accuracy**: 95-97% across Vietnamese regions  
**When to use**: Post seed funding, enterprise sales, production deployment

**Regional Balance (Both Paths)**: 33% Bắc, 33% Trung, 34% Nam

---

## **Part 1: Official Vietnamese Documents (1,500 examples)**

### **1.1 Primary Legal Sources**

```python
# collect_official_documents.py
"""
Collect Vietnamese PDPL data from official government sources
High quality, legally accurate examples
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Official Vietnamese Legal Databases
LEGAL_SOURCES = {
    'thuvienphapluat': 'https://thuvienphapluat.vn/',
    'moj_vietnam': 'https://moj.gov.vn/',
    'mps_vietnam': 'https://bocongan.gov.vn/',
    'national_assembly': 'https://quochoi.vn/'
}

# PDPL 2025 Related Documents
PDPL_DOCUMENTS = {
    'law_91_2025': {
        'name': 'Luật Bảo vệ Dữ liệu Cá nhân số 91/2025/QH15',
        'url': 'https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/...',
        'type': 'primary_law',
        'priority': 'high'
    },
    'decree_13_2023': {
        'name': 'Nghị định 13/2023/NĐ-CP',
        'url': 'https://thuvienphapluat.vn/van-ban/Cong-nghe-thong-tin/...',
        'type': 'implementation_decree',
        'priority': 'high'
    },
    'mps_circulars': {
        'name': 'Thông tư Bộ Công an về PDPL',
        'url': 'https://bocongan.gov.vn/...',
        'type': 'circular',
        'priority': 'medium'
    }
}

def extract_pdpl_sections(document_url, document_type):
    """
    Extract PDPL-related sections from Vietnamese legal documents
    Returns: List of Vietnamese text snippets with metadata
    """
    
    examples = []
    
    try:
        response = requests.get(document_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract Vietnamese paragraphs
        paragraphs = soup.find_all(['p', 'div'], class_=['article', 'content'])
        
        for para in paragraphs:
            text = para.get_text(strip=True)
            
            # Filter Vietnamese PDPL-related content (min 50 chars)
            if len(text) >= 50 and any(keyword in text.lower() for keyword in [
                'dữ liệu cá nhân', 'bảo vệ', 'quyền', 'chủ thể', 
                'xử lý', 'thu thập', 'lưu trữ', 'bảo mật'
            ]):
                examples.append({
                    'text': text,
                    'source': document_url,
                    'type': document_type,
                    'date_collected': datetime.now().isoformat(),
                    'quality': 'high',
                    'origin': 'official'
                })
    
    except Exception as e:
        print(f"Error extracting from {document_url}: {e}")
    
    return examples

# Collect from all official sources
all_official_examples = []

for doc_id, doc_info in PDPL_DOCUMENTS.items():
    print(f"📄 Collecting from: {doc_info['name']}")
    examples = extract_pdpl_sections(doc_info['url'], doc_info['type'])
    all_official_examples.extend(examples)
    print(f"   ✅ Collected {len(examples)} examples")

print(f"\n🎯 Total official examples: {len(all_official_examples)}")
```

**Expected Output**: 1,500 high-quality Vietnamese examples from official sources

---

## **Part 2: Vietnamese Media Articles (1,000 examples)**

```python
# collect_media_articles.py
"""
Collect Vietnamese PDPL articles from news media
Medium quality, current context
"""

VIETNAMESE_MEDIA = {
    'vnexpress': 'https://vnexpress.net/phap-luat',
    'tuoitre': 'https://tuoitre.vn/phap-luat.htm',
    'thanhnien': 'https://thanhnien.vn/phap-luat/',
    'vietnamnet': 'https://vietnamnet.vn/phap-luat',
    'dantri': 'https://dantri.com.vn/phap-luat.htm'
}

SEARCH_KEYWORDS = [
    'bảo vệ dữ liệu cá nhân',
    'PDPL 2025',
    'Nghị định 13/2023',
    'quyền riêng tư dữ liệu',
    'an toàn thông tin cá nhân',
    'tuân thủ bảo vệ dữ liệu'
]

def search_media_pdpl_articles(media_url, keywords):
    """Search Vietnamese media for PDPL articles"""
    
    articles = []
    
    for keyword in keywords:
        search_url = f"{media_url}/tim-kiem?q={keyword}"
        
        try:
            response = requests.get(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract article snippets (Vietnamese)
            article_divs = soup.find_all('div', class_=['article-item', 'news-item'])
            
            for article in article_divs[:20]:  # Max 20 per keyword
                title = article.find(['h3', 'h2', 'a'])
                description = article.find('p', class_='description')
                
                if title and description:
                    combined_text = f"{title.get_text(strip=True)}. {description.get_text(strip=True)}"
                    
                    articles.append({
                        'text': combined_text,
                        'source': media_url,
                        'keyword': keyword,
                        'type': 'media_article',
                        'quality': 'medium'
                    })
        
        except Exception as e:
            print(f"Error searching {media_url}: {e}")
    
    return articles

# Collect from all media sources
media_examples = []

for media_name, media_url in VIETNAMESE_MEDIA.items():
    print(f"📰 Collecting from: {media_name}")
    articles = search_media_pdpl_articles(media_url, SEARCH_KEYWORDS)
    media_examples.extend(articles)
    print(f"   ✅ Collected {len(articles)} articles")

print(f"\n🎯 Total media examples: {len(media_examples)}")
```

---

## **Part 3: Business Privacy Policies (1,000 examples)**

```python
# collect_business_policies.py
"""
Collect public Vietnamese privacy policies
Practical, real-world examples
"""

VIETNAMESE_COMPANIES = [
    # E-commerce
    {'name': 'Shopee Vietnam', 'url': 'https://shopee.vn/legaldoc/privacy', 'sector': 'ecommerce'},
    {'name': 'Lazada Vietnam', 'url': 'https://www.lazada.vn/privacy-policy/', 'sector': 'ecommerce'},
    {'name': 'Tiki.vn', 'url': 'https://tiki.vn/dieu-khoan-su-dung', 'sector': 'ecommerce'},
    {'name': 'Sendo', 'url': 'https://www.sendo.vn/chinh-sach-bao-mat', 'sector': 'ecommerce'},
    
    # Technology
    {'name': 'VNG', 'url': 'https://www.vng.com.vn/privacy', 'sector': 'tech'},
    {'name': 'FPT', 'url': 'https://fpt.com.vn/chinh-sach-bao-mat', 'sector': 'tech'},
    {'name': 'Viettel', 'url': 'https://viettel.com.vn/privacy', 'sector': 'telecom'},
    
    # Banking
    {'name': 'VPBank', 'url': 'https://www.vpbank.com.vn/chinh-sach-bao-mat', 'sector': 'banking'},
    {'name': 'Techcombank', 'url': 'https://www.techcombank.com.vn/privacy', 'sector': 'banking'},
    {'name': 'VietinBank', 'url': 'https://www.vietinbank.vn/privacy-policy', 'sector': 'banking'},
]

def extract_privacy_policy_sections(company_info):
    """Extract Vietnamese privacy policy sections"""
    
    sections = []
    
    try:
        response = requests.get(company_info['url'])
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find Vietnamese policy sections
        policy_sections = soup.find_all(['div', 'section'], class_=['policy', 'privacy'])
        
        for section in policy_sections:
            paragraphs = section.find_all('p')
            
            for para in paragraphs:
                text = para.get_text(strip=True)
                
                if len(text) >= 50:
                    sections.append({
                        'text': text,
                        'source': company_info['name'],
                        'sector': company_info['sector'],
                        'url': company_info['url'],
                        'type': 'privacy_policy',
                        'quality': 'medium-high'
                    })
    
    except Exception as e:
        print(f"Error extracting from {company_info['name']}: {e}")
    
    return sections

# Collect from all companies
business_examples = []

for company in VIETNAMESE_COMPANIES:
    print(f"🏢 Collecting from: {company['name']}")
    sections = extract_privacy_policy_sections(company)
    business_examples.extend(sections)
    print(f"   ✅ Collected {len(sections)} sections")

print(f"\n🎯 Total business examples: {len(business_examples)}")
```

---

## **Part 4: Synthetic Data Generation (1,000 examples)**

```python
# generate_synthetic_data.py
"""
Generate synthetic Vietnamese PDPL compliance data
Controlled quality, perfect regional balance
"""

import random

# 8 PDPL Categories (Vietnamese)
PDPL_CATEGORIES = {
    0: "Tính hợp pháp, công bằng và minh bạch",
    1: "Hạn chế mục đích",
    2: "Tối thiểu hóa dữ liệu",
    3: "Tính chính xác",
    4: "Hạn chế lưu trữ",
    5: "Tính toàn vẹn và bảo mật",
    6: "Trách nhiệm giải trình",
    7: "Quyền của chủ thể dữ liệu"
}

# Vietnamese Templates by Region
TEMPLATES = {
    0: {  # Lawfulness, fairness, transparency
        'bac': [
            "Công ty {company} cần phải thu thập dữ liệu cá nhân một cách hợp pháp, công bằng và minh bạch theo quy định của PDPL 2025.",
            "Các tổ chức cần phải đảm bảo tính hợp pháp khi thu thập và xử lý dữ liệu cá nhân của khách hàng.",
            "Doanh nghiệp {company} cần phải thông báo rõ ràng cho chủ thể dữ liệu về mục đích thu thập thông tin."
        ],
        'trung': [
            "Công ty {company} cần thu thập dữ liệu cá nhân hợp pháp và công khai theo luật PDPL.",
            "Tổ chức cần bảo đảm công bằng trong việc xử lý thông tin khách hàng.",
            "Doanh nghiệp {company} cần cho biết mục đích thu thập dữ liệu một cách minh bạch."
        ],
        'nam': [
            "Công ty {company} cần thu thập dữ liệu của họ một cách hợp pháp và công bằng.",
            "Tổ chức cần đảm bảo minh bạch khi xử lý thông tin cá nhân.",
            "Doanh nghiệp {company} cần cho khách hàng biết tại sao họ thu thập dữ liệu."
        ]
    },
    1: {  # Purpose limitation
        'bac': [
            "Dữ liệu cá nhân chỉ được sử dụng cho các mục đích đã thông báo trước cho chủ thể dữ liệu.",
            "Công ty {company} cần phải hạn chế việc sử dụng dữ liệu theo đúng mục đích đã công bố.",
            "Không được sử dụng dữ liệu cá nhân cho các mục đích khác ngoài những gì đã thông báo."
        ],
        'trung': [
            "Dữ liệu chỉ dùng cho mục đích đã nói với người dùng trước đó.",
            "Công ty {company} cần giới hạn việc dùng dữ liệu theo mục đích ban đầu.",
            "Không được dùng thông tin cá nhân cho việc khác."
        ],
        'nam': [
            "Dữ liệu của họ chỉ được dùng cho mục đích đã nói trước.",
            "Công ty {company} cần hạn chế dùng dữ liệu đúng mục đích.",
            "Không được dùng thông tin của họ cho việc khác."
        ]
    },
    # ... (continue for all 8 categories)
}

VIETNAMESE_COMPANIES = [
    'VNG', 'FPT', 'Viettel', 'Shopee', 'Lazada', 'Tiki',
    'VPBank', 'Techcombank', 'Grab', 'Gojek', 'MoMo', 'ZaloPay'
]

def generate_synthetic_dataset(num_samples=1000):
    """
    Generate synthetic Vietnamese PDPL dataset
    Balanced across categories and regions
    """
    
    dataset = []
    samples_per_category = num_samples // 8  # 125 per category
    samples_per_region = samples_per_category // 3  # ~42 per region
    
    for category in range(8):
        for region in ['bac', 'trung', 'nam']:
            templates = TEMPLATES.get(category, {}).get(region, [])
            
            if not templates:
                continue
            
            for _ in range(samples_per_region):
                template = random.choice(templates)
                company = random.choice(VIETNAMESE_COMPANIES)
                text = template.format(company=company)
                
                dataset.append({
                    'text': text,
                    'label': category,
                    'region': region,
                    'source': 'synthetic',
                    'category_name_vi': PDPL_CATEGORIES[category],
                    'quality': 'controlled'
                })
    
    return dataset

# Generate synthetic data
synthetic_data = generate_synthetic_dataset(1000)

# Save to JSONL
with open('vietnamese_pdpl_synthetic.jsonl', 'w', encoding='utf-8') as f:
    for item in synthetic_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"✅ Generated {len(synthetic_data)} synthetic examples")
print(f"📊 Regional distribution:")
print(f"   Bắc: {sum(1 for d in synthetic_data if d['region'] == 'bac')}")
print(f"   Trung: {sum(1 for d in synthetic_data if d['region'] == 'trung')}")
print(f"   Nam: {sum(1 for d in synthetic_data if d['region'] == 'nam')}")
```

---

## **Part 5: Crowdsourced Data (500 examples) - OPTIONAL** ⭐

> **💡 Skip this for MVP**: Crowdsourcing is **optional** and costs $1,500. Start with 4,500 free examples (Parts 1-4), then add crowdsourcing later when funded.

### **Why Add Crowdsourcing? (Post-Funding)**

✅ **Authentic regional variations** (real Vietnamese speakers)  
✅ **+5-7% accuracy improvement** (90-93% → 95-97%)  
✅ **Natural language diversity** (not just formal legal text)  
✅ **3x validation** (3 workers per example)  
✅ **Production-ready quality** for enterprise customers

### **When to Add Crowdsourcing:**
- ✅ After raising seed funding ($50K+)
- ✅ Before production launch to enterprises
- ✅ When accuracy matters for SLA commitments
- ❌ **Skip for MVP/demo** (use free data sources only)

---

```python
# crowdsource_vietnamese_data.py
"""
Crowdsource Vietnamese PDPL examples using MTurk
Diverse, authentic regional variations
⚠️ OPTIONAL: Only run this for production deployment
"""

import boto3

mturk = boto3.client('mturk', region_name='us-east-1')

VIETNAMESE_HIT_TEMPLATE = """
<HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
    <HTMLContent><![CDATA[
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8"/>
        <title>Viết câu về PDPL 2025</title>
    </head>
    <body>
        <h2>Viết câu về tuân thủ PDPL 2025 (Tiếng Việt)</h2>
        
        <p><strong>Danh mục:</strong> {category_vi}</p>
        <p><strong>Vùng miền:</strong> {region}</p>
        
        <p>Viết một câu tiếng Việt về tuân thủ bảo vệ dữ liệu cá nhân:</p>
        
        <textarea name="pdpl_example" rows="4" cols="80" required placeholder="Ví dụ: Công ty cần phải bảo vệ dữ liệu cá nhân một cách an toàn..."></textarea>
        
        <p><em>Lưu ý:</em> Câu cần rõ ràng, đúng ngữ pháp tiếng Việt, và liên quan đến danh mục trên.</p>
    </body>
    </html>
    ]]></HTMLContent>
    <FrameHeight>500</FrameHeight>
</HTMLQuestion>
"""

def create_vietnamese_pdpl_hits(num_hits=500, reward=0.50):
    """
    Create HITs for Vietnamese PDPL data collection
    Target: Vietnamese workers only
    """
    
    hit_ids = []
    
    for i in range(num_hits):
        # Rotate through categories and regions
        category = i % 8
        region_idx = i % 3
        region = ['Miền Bắc', 'Miền Trung', 'Miền Nam'][region_idx]
        category_vi = PDPL_CATEGORIES[category]
        
        hit_template = VIETNAMESE_HIT_TEMPLATE.format(
            category_vi=category_vi,
            region=region
        )
        
        response = mturk.create_hit(
            Title='Viết câu về tuân thủ PDPL 2025 (Tiếng Việt)',
            Description='Write a Vietnamese sentence about PDPL 2025 compliance',
            Keywords='vietnamese, legal, PDPL, data protection, compliance',
            Reward=str(reward),
            MaxAssignments=3,  # 3 Vietnamese workers per HIT
            LifetimeInSeconds=86400,  # 24 hours
            AssignmentDurationInSeconds=600,  # 10 minutes
            QualificationRequirements=[
                {
                    'QualificationTypeId': '00000000000000000071',  # Locale
                    'Comparator': 'EqualTo',
                    'LocaleValues': [{'Country': 'VN'}],  # Vietnam only
                    'ActionsGuarded': 'Accept'
                },
                {
                    'QualificationTypeId': '000000000000000000L0',  # Approval rate
                    'Comparator': 'GreaterThanOrEqualTo',
                    'IntegerValues': [95],  # 95%+ approval
                    'ActionsGuarded': 'Accept'
                }
            ],
            Question=hit_template
        )
        
        hit_ids.append(response['HIT']['HITId'])
        
        if (i + 1) % 50 == 0:
            print(f"✅ Created {i + 1} HITs")
    
    print(f"\n🎯 Total HITs created: {len(hit_ids)}")
    print(f"💰 Total cost: ${len(hit_ids) * reward * 3:.2f} (including fees)")
    
    return hit_ids

# Create crowdsourcing tasks
hit_ids = create_vietnamese_pdpl_hits(num_hits=500, reward=0.50)
```

**Expected Cost**: 500 HITs × $0.50 × 3 workers = $750 + fees ≈ **$1,500 total**

---

## **Data Quality Control**

```python
# quality_control.py
"""
Quality control for collected Vietnamese data
Ensures accuracy and regional balance
"""

def validate_vietnamese_text(text):
    """Validate Vietnamese text quality"""
    
    checks = {
        'min_length': len(text) >= 50,
        'has_vietnamese': any(char in text for char in 'àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệ'),
        'not_too_long': len(text) <= 500,
        'no_html': '<' not in text and '>' not in text
    }
    
    return all(checks.values()), checks

def balance_regional_distribution(dataset):
    """Ensure 33% Bắc, 33% Trung, 34% Nam"""
    
    bac = [d for d in dataset if d.get('region') == 'bac']
    trung = [d for d in dataset if d.get('region') == 'trung']
    nam = [d for d in dataset if d.get('region') == 'nam']
    
    target = len(dataset) // 3
    
    balanced = []
    balanced.extend(random.sample(bac, min(target, len(bac))))
    balanced.extend(random.sample(trung, min(target, len(trung))))
    balanced.extend(random.sample(nam, min(target, len(nam))))
    
    return balanced

# Apply quality control
validated_dataset = []

for example in all_collected_data:
    is_valid, checks = validate_vietnamese_text(example['text'])
    
    if is_valid:
        validated_dataset.append(example)
    else:
        print(f"❌ Rejected: {checks}")

# Balance regions
final_dataset = balance_regional_distribution(validated_dataset)

print(f"\n✅ Final dataset: {len(final_dataset)} examples")
```

---

## **Complete Collection Workflow**

### **🚀 MVP Workflow (Recommended Start)**

```bash
# Week 1-2: Collect official documents
python collect_official_documents.py

# Week 2: Collect media articles
python collect_media_articles.py

# Week 3: Collect business policies
python collect_business_policies.py

# Week 3: Generate synthetic data (3 days)
python generate_synthetic_data.py

# Week 4: Quality control
python quality_control.py

# Week 4: Merge all sources (4,500 examples)
python merge_datasets.py --sources official,media,business,synthetic

# Week 4: Upload to S3
python upload_to_s3.py

# ✅ MVP Dataset Ready: 4,500 examples, $0 cost, 90-93% accuracy
```

---

### **🎯 Production Workflow (Post-Funding)**

```bash
# Complete MVP workflow first (4,500 examples)
# Then add crowdsourcing:

# Week 5-6: Launch crowdsourcing (OPTIONAL)
python crowdsource_vietnamese_data.py

# Week 6: Wait for HITs completion
python check_mturk_results.py

# Week 6: Quality control on crowdsourced data
python quality_control.py --source crowdsourced

# Week 6: Merge all sources (5,000 examples)
python merge_datasets.py --sources official,media,business,synthetic,crowdsourced

# Week 6: Re-upload to S3
python upload_to_s3.py

# ✅ Production Dataset Ready: 5,000 examples, $1,500 cost, 95-97% accuracy
```

---

### **💡 Alternative: University Partnership (Free Crowdsourcing)**

```bash
# Instead of MTurk, partner with Vietnamese universities
# Cost: $0, Timeline: 6-8 weeks

# Contact universities:
python contact_universities.py --universities hanoi_law,hcmc_law,ftu

# Coordinate with professors:
python setup_student_tasks.py --target_examples 500

# Review student submissions:
python review_submissions.py --min_quality 0.8

# ✅ Free alternative to MTurk (slower but $0 cost)
```

---

## **Expected Results**

### **🚀 MVP Results (No Crowdsourcing)**

**Dataset Composition:**
- **Total Examples**: 4,500
- **Format**: JSONL (UTF-8 encoded)
- **Regional Balance**: 1,485 Bắc, 1,485 Trung, 1,530 Nam
- **Category Balance**: ~563 per PDPL category
- **Quality Mix**: 33% High, 45% Medium-High, 22% Controlled

**Timeline & Cost:**
- **Total Time**: 3-4 weeks
- **Total Cost**: **$0** ✅
- **Expected Accuracy**: **90-93%**
- **Good for**: Investor demo, MVP, proof of concept

---

### **🎯 Production Results (With Crowdsourcing)**

**Dataset Composition:**
- **Total Examples**: 5,000
- **Format**: JSONL (UTF-8 encoded)
- **Regional Balance**: 1,650 Bắc, 1,650 Trung, 1,700 Nam
- **Category Balance**: ~625 per PDPL category
- **Quality Mix**: 30% High, 40% Medium-High, 20% Controlled, 10% Authentic

**Timeline & Cost:**
- **Total Time**: 4-6 weeks
- **Total Cost**: **$1,500**
- **Expected Accuracy**: **95-97%**
- **Good for**: Enterprise customers, production deployment, SLA commitments

---

### **📊 Comparison: MVP vs. Production**

| Metric | MVP (Free) | Production (+$1,500) | Difference |
|--------|-----------|---------------------|------------|
| **Examples** | 4,500 | 5,000 | +500 (+11%) |
| **Accuracy** | 90-93% | 95-97% | +5-7% |
| **Cost** | $0 | $1,500 | +$1,500 |
| **Timeline** | 3-4 weeks | 4-6 weeks | +1-2 weeks |
| **Authenticity** | Medium | High | Better |
| **Regional Diversity** | Good | Excellent | Better |
| **Use Case** | Demo, MVP | Production | - |

**💡 Recommendation**: Start with MVP (free), validate with investors/users, then upgrade to Production when funded.

---

## 🏢 Company Lists: Web Scraping vs. Dataset Generation

### **Important Distinction**

This guide contains a **hardcoded company list** for **one-time web scraping** (lines 239-249). This is **different** from the **Dynamic Company Registry** used for ongoing dataset generation.

### **Two Different Purposes:**

#### **1. Web Scraping List (This Guide) - ONE-TIME USE**

```python
VIETNAMESE_COMPANIES = [
    {'name': 'Shopee Vietnam', 'url': 'https://shopee.vn/legaldoc/privacy'},
    {'name': 'Lazada Vietnam', 'url': 'https://www.lazada.vn/privacy-policy/'},
    # ... 10-20 companies
]
```

**Purpose**: Collect initial training data from public privacy policies  
**Frequency**: Once (during data collection phase)  
**Scope**: Limited to companies with accessible websites  
**Output**: Real-world Vietnamese compliance text  
**Maintenance**: Static list (no updates needed after collection)  

**Why Hardcoded is OK Here**:
- ✅ One-time data collection activity
- ✅ Small list (10-20 companies)
- ✅ URL-specific (not reusable)
- ✅ Quality filter (only companies with good policies)

---

#### **2. Dynamic Company Registry - ONGOING GENERATION**

```python
# From config/company_registry.json (150+ companies)
COMPANIES_ALL = load_from_registry()  # 150+ Vietnamese companies
company = select_company_for_template(template)
text = template.format(company=company)
```

**Purpose**: Generate synthetic training data at scale  
**Frequency**: Continuous (every training run)  
**Scope**: All Vietnamese companies (150+ and growing)  
**Output**: Company-normalized training samples  
**Maintenance**: Hot-reload updates (zero downtime)  

**Why Dynamic Registry Here**:
- ✅ Ongoing dataset generation
- ✅ Large list (150+ companies, growing)
- ✅ Template-based (reusable)
- ✅ Zero retraining for new companies

---

### **How They Work Together:**

```
STEP 1: DATA COLLECTION (This Guide)
├─ Scrape 10-20 company websites (hardcoded list)
├─ Extract 1,000 real Vietnamese privacy policy examples
├─ Feed into company_registry.json (enrich registry)
└─ One-time activity (MVP phase)

STEP 2: DATASET GENERATION (Dynamic Registry)
├─ Load 150+ companies from registry
├─ Generate 150,300 synthetic samples
├─ Normalize to [COMPANY] token
├─ Train company-agnostic models
└─ Ongoing activity (production phase)

STEP 3: ADD NEW COMPANIES (Dynamic Registry Only)
├─ Update company_registry.json (5 minutes)
├─ No web scraping needed
├─ No model retraining needed
└─ Future-proof scalability
```

### **When to Update Each List:**

| Scenario | Web Scraping List | Dynamic Registry |
|----------|------------------|------------------|
| **Initial MVP** | ✅ Update once | ✅ Create initial |
| **Add 1 company** | ❌ No update | ✅ Update JSON |
| **Add 10 companies** | ❌ No update | ✅ Update JSON |
| **Scrape new policies** | ✅ Update if needed | ❌ No update |
| **Generate new dataset** | ❌ No update | ✅ Use registry |

### **Best Practice Workflow:**

```bash
# Phase 1: Initial Data Collection (Once)
python collect_business_policies.py  # Uses hardcoded VIETNAMESE_COMPANIES

# Phase 2: Enrich Company Registry
python enrich_registry_from_scraped_data.py  # Add scraped companies to registry

# Phase 3: Generate Datasets (Ongoing)
python generate_hard_dataset.py --use-company-registry  # Uses Dynamic Registry

# Phase 4: Add New Companies (Anytime)
# Edit config/company_registry.json manually
# OR use Admin API
curl -X POST /api/v1/admin/companies/add -d '{...}'
```

### **Implementation Reference**

For complete Dynamic Company Registry architecture:
- **`VeriAIDPO_Dynamic_Company_Registry_Implementation.md`** - Full implementation plan
- **`VeriAIDPO_Hard_Dataset_Generation_Guide.md`** - Dataset generation with registry
- **`config/company_registry.json`** - 150+ Vietnamese companies database

### **Key Takeaway**

✅ **Web Scraping List**: Static, one-time, small (10-20 companies)  
✅ **Dynamic Registry**: Scalable, ongoing, large (150+ companies)  
✅ **Both Serve Different Purposes**: Don't confuse them!  
✅ **Scraped Data Enriches Registry**: They work together sequentially  

---

*Document Version: 2.0 (Company List Clarification)*  
*Last Updated: October 14, 2025*  
*Focus: Hybrid Data Collection Strategy*  
*Target: Production-Quality Vietnamese PDPL Dataset*  
*Changes: Added clarification distinguishing web scraping list from Dynamic Company Registry*

