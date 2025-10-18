# VeriAIDPO - Hard Dataset Generation Guide with Ambiguity
## Vietnamese PDPL 2025 - Production-Grade Training Data

**Document Version**: 1.0  
**Created**: October 14, 2025  
**Purpose**: Generate challenging, ambiguous datasets for robust Vietnamese model training  
**Target**: VeriAIDPO_Principles_VI and all future Vietnamese models

---

## 🎯 Problem with Current Dataset

### **Current Issues (from VeriAIDPO_Colab_Training_CLEAN.ipynb)**:

```python
# TOO SIMPLE - Easy keyword matching
"Công ty {company} cần thu thập dữ liệu một cách hợp pháp trong lĩnh vực {context}."
# Problem: "hợp pháp" = instant Lawfulness classification

"Dữ liệu {context} chỉ được sử dụng cho mục đích đã thông báo."
# Problem: "mục đích" = instant Purpose Limitation classification

"Dữ liệu {context} phải được {company} đảm bảo chính xác."
# Problem: "chính xác" = instant Accuracy classification
```

### **Why This is Bad**:
- ✅ **100% accuracy on synthetic data** (model memorizes keywords)
- ❌ **Poor generalization** to real Vietnamese business documents
- ❌ **No ambiguity handling** (real scenarios overlap multiple principles)
- ❌ **Keyword dependency** (model doesn't understand context)
- ❌ **Not production-ready** for Vietnamese enterprises

---

## 🚨 Real-World Vietnamese Compliance Challenges

### **Example 1: Overlapping Principles**

**Real Vietnamese Privacy Policy Excerpt**:
```vietnamese
"Chúng tôi thu thập tên, email và số điện thoại của quý khách để xử lý đơn hàng. 
Thông tin này chỉ được sử dụng cho việc giao hàng và liên hệ về đơn hàng của quý khách. 
Chúng tôi sẽ lưu trữ thông tin này trong 2 năm kể từ ngày mua hàng cuối cùng."
```

**Multiple Principles Apply**:
- ✅ **Lawfulness** (thu thập có mục đích hợp pháp)
- ✅ **Purpose Limitation** (chỉ dùng cho giao hàng)
- ✅ **Data Minimization** (chỉ thu tên, email, SĐT)
- ✅ **Storage Limitation** (lưu 2 năm)

**Challenge**: Model must identify PRIMARY principle (Purpose Limitation in this case)

---

### **Example 2: Subtle Vietnamese Business Context**

**Northern Vietnam (Formal, Government-influenced)**:
```vietnamese
"Căn cứ Luật An toàn thông tin mạng và Nghị định 13/2023/NĐ-CP, đơn vị chúng tôi 
thực hiện thu thập dữ liệu cá nhân của công dân theo đúng quy định pháp luật hiện hành."
```
**Principle**: Lawfulness (formal legal language, government context)

**Southern Vietnam (Business-oriented, Practical)**:
```vietnamese
"Công ty cam kết chỉ lấy thông tin cần thiết để phục vụ quý khách tốt nhất. 
Chúng tôi không thu thập thêm dữ liệu không liên quan đến dịch vụ."
```
**Principle**: Data Minimization (practical business language, customer focus)

**Challenge**: Same concept, different regional expression styles

---

### **Example 3: Vietnamese Legal vs Colloquial Language**

**Legal Vietnamese (Government documents)**:
```vietnamese
"Bên xử lý dữ liệu có nghĩa vụ đảm bảo tính chính xác, đầy đủ và cập nhật của 
dữ liệu cá nhân trong suốt quá trình xử lý."
```
**Principle**: Accuracy

**Colloquial Vietnamese (Startup privacy policy)**:
```vietnamese
"Chúng mình luôn cố gắng giữ thông tin của bạn được chính xác nhất. 
Nếu phát hiện sai sót, bạn có thể liên hệ để chúng mình sửa ngay nhé."
```
**Principle**: Accuracy (same meaning, casual tone)

**Challenge**: Model must handle formal "bên xử lý" and casual "chúng mình"

---

## 💡 Hard Dataset Generation Strategy

### **Principle 1: Multi-Principle Overlap Scenarios**

Generate samples where 2-3 principles overlap, requiring contextual understanding:

```python
AMBIGUOUS_SCENARIOS = {
    "lawfulness_purpose_overlap": {
        "vi": [
            "Căn cứ hợp đồng cung cấp dịch vụ, {company} thu thập {context} để thực hiện nghĩa vụ hợp đồng với khách hàng, đảm bảo việc sử dụng thông tin này chỉ phục vụ cho mục đích giao hàng và thanh toán.",
            # PRIMARY: Lawfulness (legal basis: contract)
            # SECONDARY: Purpose Limitation (chỉ cho giao hàng)
            
            "Theo quy định tại Điều 13 Luật BVDLCN, {company} xử lý dữ liệu {context} cho mục đích cung cấp dịch vụ được nêu rõ trong chính sách bảo mật, không mở rộng sang các mục đích khác.",
            # PRIMARY: Purpose Limitation (không mở rộng mục đích)
            # SECONDARY: Lawfulness (theo quy định Điều 13)
        ],
        "primary_label": "varies",  # Context-dependent
        "difficulty": "HARD"
    },
    
    "minimization_storage_overlap": {
        "vi": [
            "{company} chỉ thu thập {context} tối thiểu cần thiết cho việc xử lý đơn hàng và sẽ xóa dữ liệu này sau 6 tháng khi không còn sử dụng.",
            # PRIMARY: Storage Limitation (xóa sau 6 tháng)
            # SECONDARY: Data Minimization (thu tối thiểu)
            
            "Để tuân thủ nguyên tắc tối thiểu hóa, {company} chỉ yêu cầu {context} cần thiết và không lưu trữ thông tin này quá thời hạn quy định.",
            # PRIMARY: Data Minimization (nguyên tắc tối thiểu hóa)
            # SECONDARY: Storage Limitation (không lưu quá thời hạn)
        ],
        "primary_label": "varies",
        "difficulty": "HARD"
    },
    
    "accuracy_transparency_overlap": {
        "vi": [
            "{company} công khai quy trình kiểm tra và cập nhật {context} để đảm bảo thông tin luôn chính xác, đồng thời cho phép khách hàng xem và chỉnh sửa dữ liệu của mình.",
            # PRIMARY: Accuracy (đảm bảo chính xác)
            # SECONDARY: Transparency (công khai quy trình)
            
            "Chúng tôi thông báo rõ ràng về việc thu thập {context} và cam kết duy trì độ chính xác của thông tin này thông qua hệ thống tự động kiểm tra.",
            # PRIMARY: Transparency (thông báo rõ ràng)
            # SECONDARY: Accuracy (duy trì độ chính xác)
        ],
        "primary_label": "varies",
        "difficulty": "VERY_HARD"
    }
}
```

---

### **Principle 2: Regional Vietnamese Variation**

Create same principle with different regional expressions:

```python
REGIONAL_VARIATIONS = {
    "lawfulness": {
        "north": [
            # Formal, government-influenced, legal terminology
            "Căn cứ vào quy định pháp luật hiện hành, đơn vị chúng tôi thực hiện việc thu thập {context}.",
            "Theo Nghị định 13/2023/NĐ-CP, {company} tiến hành xử lý dữ liệu cá nhân với cơ sở pháp lý rõ ràng.",
            "Đơn vị có văn bản pháp lý cho phép thu thập và xử lý {context} của công dân.",
        ],
        "central": [
            # Traditional, consensus-building, balanced formal-informal
            "Doanh nghiệp chúng tôi tuân thủ đầy đủ quy định về bảo vệ dữ liệu khi thu thập {context}.",
            "{company} thực hiện việc xử lý thông tin theo đúng các quy định hiện hành của pháp luật.",
            "Chúng tôi có đầy đủ cơ sở pháp lý để thu thập {context} từ khách hàng.",
        ],
        "south": [
            # Business-casual, practical, customer-focused
            "Công ty mình thu thập {context} hoàn toàn hợp pháp và đúng quy định nhé.",
            "{company} cam kết thu thập thông tin của bạn theo đúng luật Việt Nam.",
            "Chúng mình xử lý dữ liệu {context} có cơ sở pháp lý rõ ràng, bạn yên tâm.",
        ]
    },
    
    "data_minimization": {
        "north": [
            "Đơn vị chỉ thu thập các dữ liệu {context} cần thiết, tuân thủ nguyên tắc tối thiểu hóa.",
            "{company} áp dụng nghiêm ngặt nguyên tắc hạn chế phạm vi thu thập dữ liệu cá nhân.",
        ],
        "central": [
            "Doanh nghiệp chỉ yêu cầu những thông tin {context} thực sự cần thiết cho hoạt động.",
            "{company} hạn chế thu thập dữ liệu ở mức tối thiểu cần thiết.",
        ],
        "south": [
            "Công ty mình chỉ lấy {context} cần thiết thôi, không thu thập dư thừa đâu.",
            "{company} chỉ hỏi thông tin thực sự cần cho dịch vụ, không hỏi thêm.",
        ]
    }
}
```

---

### **Principle 3: Semantic Ambiguity (No Keywords)**

Generate samples WITHOUT obvious PDPL keywords:

```python
NO_KEYWORD_SAMPLES = {
    "lawfulness": [
        # No "hợp pháp", "quy định", "luật" - must understand CONTRACT context
        "{company} thu thập {context} dựa trên thỏa thuận mua bán giữa hai bên.",
        "Theo điều khoản đã ký kết, {company} được quyền xử lý {context} của khách hàng.",
        "Việc thu thập {context} là một phần của hợp đồng dịch vụ.",
    ],
    
    "purpose_limitation": [
        # No "mục đích" - must understand SCOPE restriction
        "{company} sử dụng {context} cho việc giao hàng, không dùng cho việc khác.",
        "Thông tin {context} chỉ phục vụ cho hoạt động vận chuyển sản phẩm.",
        "{company} không mở rộng phạm vi sử dụng {context} ngoài những gì đã thông báo.",
    ],
    
    "data_minimization": [
        # No "tối thiểu", "hạn chế" - must understand SUFFICIENCY concept
        "{company} chỉ hỏi {context} đủ để hoàn thành dịch vụ.",
        "Chúng tôi không yêu cầu thông tin {context} không liên quan đến giao dịch.",
        "{company} thu thập vừa đủ {context} cần thiết, không thừa.",
    ],
    
    "accuracy": [
        # No "chính xác" - must understand VERIFICATION/CORRECTION
        "{company} cho phép khách hàng kiểm tra và sửa đổi {context}.",
        "Nếu {context} có sai sót, chúng tôi sẽ cập nhật ngay.",
        "{company} có hệ thống để khách hàng xác minh lại {context} của mình.",
    ],
    
    "storage_limitation": [
        # No "lưu trữ", "thời hạn" - must understand RETENTION concept
        "{company} giữ {context} trong 2 năm sau đó sẽ xóa.",
        "Thông tin {context} chỉ được duy trì đến khi hết mục đích sử dụng.",
        "{company} không giữ {context} mãi mãi, sẽ xóa khi không cần.",
    ]
}
```

---

### **Principle 4: Vietnamese Business Context Complexity**

Embed PDPL principles in realistic Vietnamese business scenarios:

```python
BUSINESS_CONTEXT_SAMPLES = {
    "ecommerce_lawfulness": [
        """Khi anh/chị đặt hàng trên {company}.vn, chúng tôi cần số điện thoại và địa chỉ 
        để shipper liên hệ giao hàng. Việc này là bắt buộc để hoàn tất đơn hàng theo 
        hợp đồng mua bán giữa hai bên.""",
        # PRIMARY: Lawfulness (legal basis = contract performance)
        # Difficulty: Real e-commerce scenario, multiple clauses
    ],
    
    "fintech_purpose_limitation": [
        """Ví điện tử {company} thu thập CMND/CCCD của quý khách để xác minh danh tính 
        theo quy định của Ngân hàng Nhà nước. Thông tin này chỉ dùng cho việc KYC, 
        không chia sẻ cho bên thứ ba với mục đích marketing.""",
        # PRIMARY: Purpose Limitation (chỉ dùng cho KYC)
        # Difficulty: Financial regulation context, multi-purpose scenario
    ],
    
    "healthtech_accuracy": [
        """Thông tin sức khỏe trong hồ sơ bệnh án điện tử của {company} cần được cập nhật 
        chính xác. Bác sĩ có thể chỉnh sửa hồ sơ sau mỗi lần khám, và bệnh nhân được quyền 
        yêu cầu sửa đổi nếu phát hiện sai sót.""",
        # PRIMARY: Accuracy (cập nhật chính xác, quyền sửa đổi)
        # Difficulty: Healthcare context, professional terminology
    ],
    
    "edtech_data_minimization": [
        """Nền tảng học online {company} chỉ yêu cầu học sinh cung cấp họ tên, email và 
        lớp học. Chúng tôi không thu thập thông tin gia đình, địa chỉ nhà, hoặc số điện 
        thoại phụ huynh trừ khi có nhu cầu liên hệ khẩn cấp.""",
        # PRIMARY: Data Minimization (chỉ yêu cầu họ tên, email, lớp)
        # Difficulty: Children's data context, conditional collection
    ]
}
```

---

## 🎨 Implementation: Hard Dataset Generator for Vietnamese

### **Enhanced Template System**

```python
class VietnameseHardDatasetGenerator:
    """
    Generate production-grade Vietnamese datasets with ambiguity
    """
    
    def __init__(self):
        self.ambiguity_levels = ['EASY', 'MEDIUM', 'HARD', 'VERY_HARD']
        self.regional_styles = ['north', 'central', 'south']
        self.formality_levels = ['legal', 'formal', 'business', 'casual']
        
    def generate_hard_sample(
        self, 
        category_id: int, 
        ambiguity: str = 'HARD',
        region: str = 'south',
        formality: str = 'business'
    ) -> Dict:
        """
        Generate single hard sample with controlled ambiguity
        """
        
        if ambiguity == 'VERY_HARD':
            # Multi-principle overlap, no keywords, complex context
            return self._generate_multi_principle_sample(category_id, region)
            
        elif ambiguity == 'HARD':
            # No obvious keywords, regional variation, business context
            return self._generate_no_keyword_sample(category_id, region, formality)
            
        elif ambiguity == 'MEDIUM':
            # Subtle keywords, some ambiguity, standard business language
            return self._generate_subtle_keyword_sample(category_id, region)
            
        else:  # EASY
            # Clear keywords (similar to current dataset)
            return self._generate_clear_sample(category_id)
    
    def _generate_multi_principle_sample(self, primary_category: int, region: str) -> Dict:
        """
        Generate sample where 2-3 principles overlap
        Model must identify PRIMARY principle from context
        """
        
        if primary_category == 0:  # Lawfulness as PRIMARY
            overlapping_principles = [
                {
                    'text': "Căn cứ hợp đồng dịch vụ đã ký, {company} thu thập {context} để thực hiện nghĩa vụ giao hàng, đảm bảo chỉ sử dụng cho mục đích này và không chia sẻ cho bên thứ ba.",
                    'primary': 0,  # Lawfulness (hợp đồng = legal basis)
                    'secondary': [1],  # Purpose limitation (chỉ sử dụng cho mục đích này)
                    'keywords_to_avoid': ['hợp pháp', 'luật'],  # Force context understanding
                },
                {
                    'text': "Theo thỏa thuận với khách hàng, {company} xử lý {context} trong phạm vi cung cấp dịch vụ, cam kết chỉ giữ thông tin đến khi hoàn tất giao dịch.",
                    'primary': 0,  # Lawfulness (thỏa thuận = contract)
                    'secondary': [1, 4],  # Purpose + Storage limitation
                    'keywords_to_avoid': ['hợp pháp', 'quy định'],
                }
            ]
            
        elif primary_category == 1:  # Purpose Limitation as PRIMARY
            overlapping_principles = [
                {
                    'text': "{company} sử dụng {context} chỉ để xử lý đơn hàng như đã thông báo, không mở rộng sang marketing hoặc chia sẻ bên thứ ba, đồng thời xóa sau 6 tháng.",
                    'primary': 1,  # Purpose limitation (không mở rộng)
                    'secondary': [4],  # Storage limitation (xóa sau 6 tháng)
                    'keywords_to_avoid': ['mục đích'],  # Force "không mở rộng" understanding
                },
                {
                    'text': "Thông tin {context} thu thập từ khách hàng chỉ phục vụ cho việc giao hàng và thanh toán, {company} cam kết không sử dụng cho bất kỳ hoạt động nào khác.",
                    'primary': 1,  # Purpose limitation (chỉ phục vụ giao hàng)
                    'secondary': [0],  # Lawfulness (implicit contract basis)
                    'keywords_to_avoid': ['mục đích', 'hạn chế'],
                }
            ]
        
        # Select one sample and fill with regional business context
        sample = random.choice(overlapping_principles)
        filled_text = self._fill_with_regional_context(sample['text'], region)
        
        return {
            'text': filled_text,
            'label': sample['primary'],
            'ambiguity': 'VERY_HARD',
            'overlapping_principles': sample['secondary'],
            'difficulty_reason': 'Multiple principles overlap, no obvious keywords'
        }
    
    def _generate_no_keyword_sample(self, category_id: int, region: str, formality: str) -> Dict:
        """
        Generate samples WITHOUT obvious PDPL keywords
        Forces model to understand semantic meaning
        """
        
        NO_KEYWORD_TEMPLATES = {
            0: {  # Lawfulness (no "hợp pháp", "luật", "quy định")
                'legal': [
                    "Dựa trên thỏa thuận ký kết giữa hai bên, {company} được quyền xử lý {context}.",
                    "Theo điều khoản hợp đồng, việc thu thập {context} là bắt buộc để thực hiện dịch vụ.",
                ],
                'business': [
                    "Khi đăng ký dịch vụ, bạn đã đồng ý cho {company} sử dụng {context} để hoàn tất giao dịch.",
                    "{company} thu thập {context} dựa trên sự cho phép của khách hàng trong hợp đồng.",
                ],
                'casual': [
                    "Bạn đã đồng ý cho mình thu thập {context} khi đặt hàng rồi nhé.",
                    "Theo thỏa thuận mua bán, {company} được phép sử dụng {context} của bạn.",
                ]
            },
            
            1: {  # Purpose Limitation (no "mục đích", "hạn chế")
                'legal': [
                    "{company} sử dụng {context} trong phạm vi cung cấp dịch vụ, không mở rộng sang hoạt động khác.",
                    "Thông tin {context} chỉ phục vụ cho việc giao hàng, không dùng cho marketing.",
                ],
                'business': [
                    "{company} chỉ dùng {context} để xử lý đơn hàng, không chia sẻ cho bên thứ ba.",
                    "Dữ liệu {context} chỉ phục vụ cho hoạt động vận chuyển sản phẩm.",
                ],
                'casual': [
                    "Mình chỉ dùng {context} để giao hàng thôi, không làm gì khác đâu.",
                    "{company} không sử dụng {context} của bạn ngoài việc ship hàng.",
                ]
            },
            
            2: {  # Data Minimization (no "tối thiểu", "hạn chế")
                'legal': [
                    "{company} chỉ yêu cầu {context} cần thiết để thực hiện dịch vụ, không thu thập thêm.",
                    "Phạm vi thu thập {context} được giới hạn ở mức đủ để hoàn tất giao dịch.",
                ],
                'business': [
                    "{company} chỉ hỏi {context} cần thiết cho đơn hàng, không yêu cầu thông tin thừa.",
                    "Chúng tôi chỉ thu {context} đủ để xử lý, không lấy thêm dữ liệu không liên quan.",
                ],
                'casual': [
                    "Mình chỉ hỏi {context} cần thiết thôi, không hỏi lung tung.",
                    "{company} chỉ lấy thông tin vừa đủ, không thu quá nhiều.",
                ]
            },
            
            3: {  # Accuracy (no "chính xác", "đúng")
                'legal': [
                    "{company} cho phép khách hàng kiểm tra và chỉnh sửa {context} bất kỳ lúc nào.",
                    "Nếu phát hiện sai sót trong {context}, khách hàng có quyền yêu cầu cập nhật.",
                ],
                'business': [
                    "{company} hỗ trợ khách hàng cập nhật {context} khi có thay đổi.",
                    "Bạn có thể liên hệ để sửa đổi {context} nếu thấy có lỗi.",
                ],
                'casual': [
                    "Nếu {context} sai, bạn báo mình sửa ngay nhé.",
                    "{company} cho phép bạn kiểm tra và đổi {context} bất cứ lúc nào.",
                ]
            },
            
            4: {  # Storage Limitation (no "lưu trữ", "thời hạn")
                'legal': [
                    "{company} giữ {context} trong 2 năm sau giao dịch cuối cùng, sau đó sẽ xóa.",
                    "Dữ liệu {context} chỉ được duy trì đến khi hoàn tất dịch vụ.",
                ],
                'business': [
                    "{company} không giữ {context} mãi mãi, sẽ xóa sau 6 tháng không sử dụng.",
                    "Thông tin {context} chỉ tồn tại đến khi bạn còn là khách hàng.",
                ],
                'casual': [
                    "Mình chỉ giữ {context} trong 1 năm thôi, sau đó xóa.",
                    "{company} không lưu {context} lâu dài, chỉ giữ khi cần.",
                ]
            },
            
            5: {  # Integrity & Confidentiality (no "bảo mật", "an toàn")
                'legal': [
                    "{company} áp dụng mã hóa để bảo vệ {context} khỏi truy cập trái phép.",
                    "Dữ liệu {context} được kiểm soát chặt chẽ, chỉ nhân viên được phép mới truy cập.",
                ],
                'business': [
                    "{company} sử dụng công nghệ hiện đại để bảo vệ {context} của bạn.",
                    "Thông tin {context} được giữ kín, không chia sẻ cho bên ngoài.",
                ],
                'casual': [
                    "Mình mã hóa {context} của bạn để không ai đọc trộm được.",
                    "{company} bảo vệ {context} rất kỹ, yên tâm nhé.",
                ]
            },
            
            6: {  # Accountability (no "trách nhiệm", "giải trình")
                'legal': [
                    "{company} chỉ định DPO để giám sát việc xử lý {context}.",
                    "Chúng tôi có nhân viên chuyên trách quản lý và kiểm soát {context}.",
                ],
                'business': [
                    "{company} có bộ phận chịu trách nhiệm về việc xử lý {context}.",
                    "Chúng tôi chỉ định người phụ trách để đảm bảo {context} được quản lý đúng.",
                ],
                'casual': [
                    "{company} có người chuyên lo về {context} của bạn.",
                    "Mình có team riêng để quản lý {context} cho an toàn.",
                ]
            },
            
            7: {  # Data Subject Rights (no "quyền", "chủ thể")
                'legal': [
                    "Khách hàng có thể yêu cầu {company} cung cấp bản sao {context}.",
                    "Bạn được phép xóa {context} của mình khỏi hệ thống {company} bất kỳ lúc nào.",
                ],
                'business': [
                    "{company} cho phép bạn tải về dữ liệu {context} của mình.",
                    "Nếu không muốn tiếp tục, bạn có thể yêu cầu xóa {context}.",
                ],
                'casual': [
                    "Bạn muốn xem hoặc xóa {context}, cứ liên hệ mình nhé.",
                    "{company} sẽ gửi {context} cho bạn nếu bạn cần.",
                ]
            }
        }
        
        templates = NO_KEYWORD_TEMPLATES[category_id][formality]
        selected = random.choice(templates)
        filled_text = self._fill_with_regional_context(selected, region)
        
        return {
            'text': filled_text,
            'label': category_id,
            'ambiguity': 'HARD',
            'difficulty_reason': 'No obvious keywords, semantic understanding required'
        }
```

---

## 📊 Recommended Dataset Composition for Vietnamese Models

### **Training Set (75% of data)**

```python
TRAINING_COMPOSITION = {
    'VERY_HARD': 0.30,    # 30% multi-principle overlap scenarios
    'HARD': 0.40,         # 40% no-keyword, semantic understanding
    'MEDIUM': 0.20,       # 20% subtle keywords, some ambiguity
    'EASY': 0.10,         # 10% clear examples (for baseline learning)
}

# Total: 5,000 training samples per category
# VERY_HARD: 1,500 samples
# HARD: 2,000 samples
# MEDIUM: 1,000 samples
# EASY: 500 samples
```

### **Validation Set (15% of data)**

```python
VALIDATION_COMPOSITION = {
    'VERY_HARD': 0.40,    # Higher proportion of hard samples for robust validation
    'HARD': 0.40,
    'MEDIUM': 0.15,
    'EASY': 0.05,
}

# Total: 1,000 validation samples per category
```

### **Test Set (10% of data)**

```python
TEST_COMPOSITION = {
    'VERY_HARD': 0.50,    # Majority hard samples to test generalization
    'HARD': 0.35,
    'MEDIUM': 0.10,
    'EASY': 0.05,
}

# Total: 800 test samples per category
```

---

## 🎯 Expected Model Performance with Hard Dataset

### **Realistic Target Accuracy** (vs 100% on easy dataset)

| Dataset Type | Training Acc | Validation Acc | Test Acc | Production Expectation |
|--------------|--------------|----------------|----------|------------------------|
| **Current (Easy)** | 100% | 100% | 100% | 60-70% (overfitting) |
| **Hard (Proposed)** | 82-88% | 78-85% | 75-82% | 75-82% (generalizes!) |

### **Why Lower Accuracy is BETTER**:

✅ **Generalization**: Model learns context, not keywords  
✅ **Production-Ready**: Handles real Vietnamese business documents  
✅ **Robust**: Works with regional variations and ambiguity  
✅ **Investor-Confident**: Realistic performance metrics  

❌ **100% accuracy** = Overfitting to synthetic templates (NOT production-ready)

---

## 🚀 Implementation Steps

### **Step 1: Update VeriAIDPO_Colab_Training_CLEAN.ipynb**

Replace `VietnameseTemplateGenerator` with `VietnameseHardDatasetGenerator`

### **Step 2: Generate Hard Dataset**

```python
generator = VietnameseHardDatasetGenerator()

hard_dataset = []
for category_id in range(8):
    # 5000 samples per category with controlled ambiguity
    for ambiguity, count in [
        ('VERY_HARD', 1500),
        ('HARD', 2000),
        ('MEDIUM', 1000),
        ('EASY', 500)
    ]:
        for _ in range(count):
            sample = generator.generate_hard_sample(
                category_id, 
                ambiguity=ambiguity,
                region=random.choice(['north', 'central', 'south']),
                formality=random.choice(['legal', 'formal', 'business', 'casual'])
            )
            hard_dataset.append(sample)
```

### **Step 3: Train VeriAIDPO_Principles_VI with Hard Dataset**

Expected timeline: 2-3 days (same as easy dataset)  
Expected accuracy: **78-88%** (realistic, production-grade)

### **Step 4: Validate on Real Vietnamese Documents**

Test model on actual Vietnamese privacy policies, terms of service, compliance documents

---

## ✅ Success Criteria

### **Model Performance**:
- ✅ **Training Accuracy**: 82-88% (not 100%)
- ✅ **Validation Accuracy**: 78-85%
- ✅ **Test Accuracy**: 75-82%
- ✅ **Real Document Accuracy**: 70-80% (acceptable for production)

### **Dataset Quality**:
- ✅ 30% samples have multi-principle overlap
- ✅ 40% samples have no obvious keywords
- ✅ 100% samples use realistic Vietnamese business language
- ✅ Regional variation coverage: 33% North, 33% Central, 33% South

### **Model Robustness**:
- ✅ Handles formal legal Vietnamese (government documents)
- ✅ Handles casual business Vietnamese (startup policies)
- ✅ Correctly identifies PRIMARY principle in overlapping scenarios
- ✅ No keyword dependency (semantic understanding)

---

## 🏢 Company Name Strategy: Dynamic Registry Integration

### **Overview**

All dataset generation uses **REAL Vietnamese company names** from the Dynamic Company Registry, then normalizes them during training to enable zero-retraining scalability.

### **Why Real Company Names?**

**Production Realism:**
- Vietnamese businesses use specific brand names in compliance contexts
- Regional patterns: "Vietcombank tại chi nhánh Hà Nội" vs "VCB ở chi nhánh TPHCM"
- Industry-specific terminology: FinTech (MoMo, ZaloPay) vs Healthcare (Vinmec, FV Hospital)

**Training Quality:**
- Models learn real Vietnamese business language patterns
- Captures authentic company-context relationships
- Reflects actual compliance documentation style

### **Company Selection Strategy**

```python
class VietnameseHardDatasetGenerator:
    """
    Enhanced with Dynamic Company Registry integration
    """
    
    def __init__(self):
        from app.core.company_registry import CompanyRegistry
        
        self.company_registry = CompanyRegistry()
        self.ambiguity_levels = ['EASY', 'MEDIUM', 'HARD', 'VERY_HARD']
        
    def _select_company_for_context(
        self, 
        industry: str,
        region: str = None,
        company_size: str = None
    ) -> str:
        """
        Select appropriate Vietnamese company from registry
        based on industry, region, and size context
        """
        
        # Get companies matching industry
        companies = self.company_registry.get_companies_by_industry(industry)
        
        # Filter by region if specified
        if region:
            companies = [c for c in companies if region in c.get('regions', [])]
        
        # Filter by size if specified
        if company_size:
            companies = [c for c in companies if c.get('size') == company_size]
        
        # Randomly select from matching companies
        import random
        return random.choice(companies)['name']
    
    def generate_financial_sample(self, region: str) -> Dict:
        """
        Example: Generate financial sector sample with real bank
        """
        
        # Select real Vietnamese bank
        company = self._select_company_for_context(
            industry='finance',
            region=region,
            company_size='large'
        )
        # Returns: "Vietcombank", "BIDV", "Techcombank", etc.
        
        # Generate sample with real company name
        text = f"""Căn cứ hợp đồng mở tài khoản, {company} thu thập CMND/CCCD, 
        giấy tờ chứng minh thu nhập, và thông tin liên hệ của khách hàng. 
        Thông tin này được sử dụng để thẩm định hồ sơ vay vốn theo quy định 
        của Ngân hàng Nhà nước."""
        
        return {
            'text': text,
            'category_id': 1,  # Contractual Necessity
            'company': company,  # Metadata for tracking
            'industry': 'finance',
            'region': region
        }
```

### **Industry-Company Mapping**

The Dynamic Company Registry includes **150+ Vietnamese companies** across 9 industries:

| Industry | Count | Examples | Context Usage |
|----------|-------|----------|---------------|
| **Technology** | 30-40 | Shopee, Tiki, Grab, VNG, FPT, Viettel | E-commerce, ride-hailing, telecom compliance |
| **Finance** | 25-30 | VCB, BIDV, Techcombank, MoMo, ZaloPay | Banking, FinTech, payment processing |
| **Healthcare** | 15-20 | Vinmec, FV Hospital, Bệnh viện Bạch Mai | Medical records, telemedicine, health apps |
| **Education** | 10-12 | ELSA, Topica, CoderSchool | EdTech, student data, learning analytics |
| **Retail** | 15-20 | VinMart, Co.opmart, BigC, Sendo | Loyalty programs, customer data |
| **Transportation** | 8-10 | Vietnam Airlines, Vietjet, GSM Logistics | Passenger data, tracking systems |
| **Real Estate** | 8-10 | Vingroup, Novaland, Hưng Thịnh | Property transactions, customer CRM |
| **Telecom** | 5-7 | Viettel, VNPT, MobiFone, VinaPhone | Subscriber data, usage analytics |
| **Government** | 5-8 | Bộ Y tế, Bộ GD&ĐT, UBND TPHCM | Citizen data, public services |

### **Regional Company Selection**

**North (Hanoi) - 33% of samples:**
```python
# Formal, government-aligned companies
north_examples = [
    "Vietcombank",  # State-owned bank
    "BIDV",         # State-owned bank
    "Viettel",      # Military-owned telecom
    "VNPT",         # State telecom
    "Bệnh viện Bạch Mai"  # Government hospital
]
```

**Central (Da Nang/Hue) - 33% of samples:**
```python
# Traditional businesses, tourism, government services
central_examples = [
    "FPT",                    # Tech company HQ in Da Nang
    "Vingroup",               # Tourism/hospitality
    "Bệnh viện Đà Nẵng",      # Regional hospital
    "UBND Thừa Thiên Huế"     # Provincial government
]
```

**South (HCMC) - 33% of samples:**
```python
# Entrepreneurial, startup, international businesses
south_examples = [
    "Shopee",           # E-commerce startup
    "Grab",             # Ride-hailing
    "Techcombank",      # Private bank
    "MoMo",             # FinTech startup
    "Vinmec",           # Private healthcare
    "ELSA"              # EdTech startup
]
```

### **Normalization Pipeline (Separate from Generation)**

**CRITICAL**: Dataset generation uses REAL company names. Normalization happens during model training:

```python
# Step 1: GENERATION (this guide) - Use real companies
sample = {
    'text': "MoMo thu thập CMND của khách hàng để xác thực tài khoản...",
    'category_id': 1,
    'company': 'MoMo'
}

# Step 2: NORMALIZATION (training pipeline) - Replace with token
from app.core.text_normalizer import PDPLTextNormalizer

normalizer = PDPLTextNormalizer()
normalized_text = normalizer.normalize_company_names(sample['text'])
# Result: "[COMPANY] thu thập CMND của khách hàng để xác thực tài khoản..."

# Step 3: TRAINING - Model learns company-agnostic patterns
training_sample = {
    'text': normalized_text,
    'category_id': 1
}
```

### **Benefits of This Approach**

**1. Production Realism During Training:**
- Models see authentic Vietnamese business language
- Learn regional variations (VCB vs Vietcombank vs Ngân hàng TMCP Ngoại thương Việt Nam)
- Understand industry-specific contexts

**2. Company-Agnostic Prediction:**
- After normalization, model works with ANY company name
- No bias toward specific brands
- Generalizes to unseen companies

**3. Zero-Retraining Scalability:**
- Add new companies to registry: 5 minutes, $0 cost
- No model retraining required
- Future-proof architecture

**4. Cost Savings:**
- Traditional approach (hardcoded): $220-320 + 7 weeks per company update
- Dynamic registry: $0 + 5 minutes for unlimited company additions
- **Lifetime savings**: $440-640 + 14 weeks for just 3 company updates

### **Implementation References**

**Full Architecture**: See `VeriAIDPO_Dynamic_Company_Registry_Implementation.md` for:
- CompanyRegistry class implementation (500+ LOC)
- PDPLTextNormalizer class implementation (300+ LOC)
- Admin API for company management (7 endpoints)
- Classification API integration with normalization
- Testing suite and deployment guide

**Company Registry File**: `config/company_registry.json`
```json
{
  "companies": [
    {
      "id": "vietcombank",
      "name": "Vietcombank",
      "aliases": ["VCB", "Ngân hàng TMCP Ngoại thương Việt Nam"],
      "industry": "finance",
      "regions": ["north", "central", "south"],
      "size": "large",
      "type": "state-owned"
    },
    {
      "id": "momo",
      "name": "MoMo",
      "aliases": ["Ví MoMo", "M-Service"],
      "industry": "finance",
      "regions": ["south"],
      "size": "startup",
      "type": "private"
    }
    // ... 148+ more Vietnamese companies
  ]
}
```

### **Dataset Generation Workflow**

```bash
# 1. Load Company Registry
python -c "from app.core.company_registry import CompanyRegistry; 
           registry = CompanyRegistry(); 
           print(f'Loaded {len(registry.get_all_companies())} companies')"

# 2. Generate Hard Dataset with Real Companies
python scripts/generate_hard_dataset.py \
    --model-type VeriAIDPO_Principles \
    --language vi \
    --total-samples 24000 \
    --use-company-registry \
    --output datasets/vietnamese_pdpl_hard_principles.jsonl

# 3. Verify Company Distribution
python scripts/validate_dataset.py \
    --dataset datasets/vietnamese_pdpl_hard_principles.jsonl \
    --check-company-coverage

# 4. Train with Normalization
python scripts/train_model.py \
    --dataset datasets/vietnamese_pdpl_hard_principles.jsonl \
    --normalize-companies \
    --output models/VeriAIDPO_Principles_VI_v2

# 5. Add New Company (Anytime, Zero Retraining)
curl -X POST http://localhost:8000/api/v1/admin/companies/add \
    -H "Content-Type: application/json" \
    -d '{
      "name": "VPBank",
      "aliases": ["VP Bank", "Ngân hàng TMCP Việt Nam Thịnh Vượng"],
      "industry": "finance",
      "regions": ["north", "central", "south"],
      "size": "large"
    }'
```

### **Quality Validation**

After implementing Dynamic Company Registry, validate:

- ✅ **Company Coverage**: All 150+ Vietnamese brands in registry
- ✅ **Industry Distribution**: Matches production reality (25% tech, 20% finance, etc.)
- ✅ **Regional Balance**: 33% North, 33% Central, 33% South
- ✅ **Normalization Accuracy**: 99.9%+ company name detection rate
- ✅ **Model Performance**: No degradation vs hardcoded approach
- ✅ **Inference Speed**: <100ms including normalization overhead

---

## 📝 Next Steps

1. **Review this guide** and approve hard dataset strategy
2. **Update training notebook** with `VietnameseHardDatasetGenerator`
3. **Generate hard dataset** (40,000 samples total, 8 categories × 5,000)
4. **Train VeriAIDPO_Principles_VI** with hard dataset
5. **Validate** on real Vietnamese compliance documents
6. **Apply same strategy** to all 10 additional model types (Legal Basis, Breach Triage, etc.)

---

**Document Owner**: VeriSyntra ML Team  
**Last Updated**: October 14, 2025  
**Status**: 📋 Ready for Implementation  
**Priority**: 🚨 HIGH - Critical for Production Readiness
