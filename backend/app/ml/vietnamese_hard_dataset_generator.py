"""
Vietnamese Hard Dataset Generator with Company Normalization
Generates production-grade PDPL datasets using Dynamic Company Registry.

Author: VeriSyntra Development Team
Created: 2025-10-18
Version: 1.0.0
"""

import random
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.core.company_registry import get_registry
from app.core.pdpl_normalizer import get_normalizer


class VietnameseHardDatasetGenerator:
    """
    Generate production-grade Vietnamese PDPL datasets with:
    1. Real company names from Dynamic Company Registry
    2. Automatic normalization to [COMPANY] tokens
    3. Multi-level ambiguity (EASY, MEDIUM, HARD, VERY_HARD)
    4. Regional and cultural variations
    5. Support for 11 model types (Principles + 10 operational models)
    
    This ensures models are company-agnostic while training on realistic data.
    """
    
    # Model Type 0: VeriAIDPO_Principles (PDPL 2025 Core Principles)
    PDPL_CATEGORIES = {
        0: "Lawfulness",
        1: "Purpose Limitation",
        2: "Data Minimization",
        3: "Accuracy",
        4: "Storage Limitation",
        5: "Security",
        6: "Transparency",
        7: "Accountability"
    }
    
    # Model Type 1: VeriAIDPO_LegalBasis (Article 13.1 a-f)
    LEGAL_BASIS_CATEGORIES = {
        0: "Consent",
        1: "Contract Performance",
        2: "Legal Obligation",
        3: "Legitimate Interest"
    }
    
    # Model Type 2: VeriAIDPO_BreachTriage (Articles 37-38, Decree 13/2023 Article 18)
    BREACH_TRIAGE_CATEGORIES = {
        0: "Low Risk",
        1: "Medium Risk",
        2: "High Risk",
        3: "Critical Risk"
    }
    
    # Model Type 3: VeriAIDPO_CrossBorder (Articles 32-36, Decree 13/2023 Articles 10-11)
    CROSS_BORDER_CATEGORIES = {
        0: "Domestic Only",
        1: "Approved Country Transfer",
        2: "Requires MPS Approval",
        3: "Prohibited Transfer",
        4: "Emergency Exception"
    }
    
    # Model Type 4: VeriAIDPO_ConsentType (Article 12, Decree 13/2023 Article 4)
    CONSENT_TYPE_CATEGORIES = {
        0: "Explicit Consent",
        1: "Implied Consent",
        2: "Parental Consent",
        3: "Invalid Consent"
    }
    
    # Model Type 5: VeriAIDPO_DataSensitivity (Article 4, Article 11)
    DATA_SENSITIVITY_CATEGORIES = {
        0: "Basic Data",
        1: "Personal Data",
        2: "Sensitive Data",
        3: "Special Category Data"
    }
    
    # Model Type 6: VeriAIDPO_DPOTasks (Articles 35-38)
    DPO_TASKS_CATEGORIES = {
        0: "Advisory",
        1: "Policy Development",
        2: "Training",
        3: "Audit",
        4: "Regulatory Reporting"
    }
    
    # Model Type 7: VeriAIDPO_RiskLevel (Articles 38, 44)
    RISK_LEVEL_CATEGORIES = {
        0: "Low Risk",
        1: "Medium Risk",
        2: "High Risk (DPIA Required)",
        3: "Critical Risk"
    }
    
    # Model Type 8: VeriAIDPO_ComplianceStatus (Overall Compliance)
    COMPLIANCE_STATUS_CATEGORIES = {
        0: "Compliant",
        1: "Partially Compliant",
        2: "Non-Compliant",
        3: "Unknown Status"
    }
    
    # Model Type 9: VeriAIDPO_Regional (Vietnamese Regional Context)
    REGIONAL_CATEGORIES = {
        0: "North",
        1: "Central",
        2: "South"
    }
    
    # Model Type 10: VeriAIDPO_Industry (Industry-Specific Requirements)
    INDUSTRY_CATEGORIES = {
        0: "Finance",
        1: "Healthcare",
        2: "Education",
        3: "Technology"
    }
    
    # Model Type Registry (for dynamic selection)
    MODEL_TYPES = {
        'principles': PDPL_CATEGORIES,
        'legal_basis': LEGAL_BASIS_CATEGORIES,
        'breach_triage': BREACH_TRIAGE_CATEGORIES,
        'cross_border': CROSS_BORDER_CATEGORIES,
        'consent_type': CONSENT_TYPE_CATEGORIES,
        'data_sensitivity': DATA_SENSITIVITY_CATEGORIES,
        'dpo_tasks': DPO_TASKS_CATEGORIES,
        'risk_level': RISK_LEVEL_CATEGORIES,
        'compliance_status': COMPLIANCE_STATUS_CATEGORIES,
        'regional': REGIONAL_CATEGORIES,
        'industry': INDUSTRY_CATEGORIES
    }
    
    def __init__(self, model_type: str = 'principles'):
        """
        Initialize generator with registry and normalizer.
        
        Args:
            model_type (str): Type of model to generate data for.
                Options: 'principles', 'legal_basis', 'breach_triage', 'cross_border',
                         'consent_type', 'data_sensitivity', 'dpo_tasks', 'risk_level',
                         'compliance_status', 'regional', 'industry'
                Default: 'principles'
        """
        self.registry = get_registry()
        self.normalizer = get_normalizer()
        
        # Set model type and corresponding categories
        self.model_type = model_type
        if model_type not in self.MODEL_TYPES:
            raise ValueError(
                f"Invalid model_type '{model_type}'. Must be one of: {list(self.MODEL_TYPES.keys())}"
            )
        self.categories = self.MODEL_TYPES[model_type]
        
        # Configuration
        self.ambiguity_levels = ['EASY', 'MEDIUM', 'HARD', 'VERY_HARD']
        self.regional_styles = ['north', 'central', 'south']
        self.formality_levels = ['legal', 'formal', 'business', 'casual']
        
        # Vietnamese data contexts
        self.data_contexts = [
            'so dien thoai', 'dia chi email', 'dia chi nha',
            'ten day du', 'CMND/CCCD', 'thong tin thanh toan',
            'lich su mua hang', 'du lieu suc khoe', 'thong tin hoc sinh',
            'ho so benh an', 'du lieu vi tri', 'thong tin ngan hang',
            'hinh anh ca nhan', 'giay to tuy than', 'so tai khoan',
            'mat khau', 'sinh trắc hoc', 'du lieu hanh vi',
            'thong tin gia dinh', 'thu nhap', 'thong tin cong viec'
        ]
        
        # Get stats for balanced selection
        self.registry_stats = self.registry.get_statistics()
    
    def get_company_by_context(
        self,
        industry: Optional[str] = None,
        region: Optional[str] = None
    ) -> str:
        """
        Get random company name from registry with optional filters.
        
        Args:
            industry (str, optional): Filter by industry
            region (str, optional): Filter by region
        
        Returns:
            Company name (canonical or alias)
        """
        # Search with filters
        companies = self.registry.search_companies(
            industry=industry,
            region=region,
            limit=100
        )
        
        if not companies:
            # Fallback to all companies
            companies = self.registry.search_companies(limit=100)
        
        if not companies:
            # Ultimate fallback
            return "Cong ty ABC"
        
        # Select random company
        company = random.choice(companies)
        company_name = company['name']
        
        # 30% chance to use alias instead of canonical name
        if random.random() < 0.3:
            # Get aliases from original registry data
            for industry_name, regions in self.registry.companies.items():
                for region_name, company_list in regions.items():
                    for comp in company_list:
                        if comp['name'] == company_name and comp.get('aliases'):
                            return random.choice(comp['aliases'])
        
        return company_name
    
    def generate_hard_sample(
        self,
        category_id: int,
        ambiguity: str = 'HARD',
        region: str = 'south',
        formality: str = 'business',
        industry: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate single hard sample with company normalization.
        
        Args:
            category_id (int): Category ID (range depends on model type)
            ambiguity (str): Difficulty level (EASY, MEDIUM, HARD, VERY_HARD)
            region (str): Vietnamese region (north, central, south)
            formality (str): Language formality (legal, formal, business, casual)
            industry (str, optional): Company industry filter
        
        Returns:
            Dict with normalized text, label, and metadata:
            {
                'text': '[COMPANY] thu thap...',  # NORMALIZED for training
                'label': 0,
                'raw_text': 'Shopee VN thu thap...',  # Original with real company
                'ambiguity': 'HARD',
                'metadata': {...}
            }
        """
        # Validate category_id for current model type
        if category_id not in self.categories:
            raise ValueError(
                f"Invalid category_id {category_id} for model type '{self.model_type}'. "
                f"Valid range: 0-{len(self.categories)-1}"
            )
        
        # Get real company name for this sample
        company_name = self.get_company_by_context(industry=industry, region=region)
        context = random.choice(self.data_contexts)
        
        # Generate template based on ambiguity level
        if ambiguity == 'VERY_HARD':
            raw_text = self._generate_multi_principle_sample(
                category_id, company_name, context, region
            )
        elif ambiguity == 'HARD':
            raw_text = self._generate_no_keyword_sample(
                category_id, company_name, context, formality
            )
        elif ambiguity == 'MEDIUM':
            raw_text = self._generate_subtle_keyword_sample(
                category_id, company_name, context, region
            )
        else:  # EASY
            raw_text = self._generate_clear_sample(
                category_id, company_name, context
            )
        
        # CRITICAL: Normalize company name to [COMPANY] token
        normalized_text = self.normalizer.normalize_for_inference(raw_text)
        
        return {
            'text': normalized_text,  # This goes to model training
            'label': category_id,
            'raw_text': raw_text,  # For reference/debugging only
            'ambiguity': ambiguity,
            'metadata': {
                'company': company_name,
                'industry': industry or 'mixed',
                'region': region,
                'formality': formality,
                'context': context,
                'category_name': self.categories[category_id],
                'model_type': self.model_type
            }
        }
    
    def _generate_clear_sample(
        self,
        category_id: int,
        company: str,
        context: str
    ) -> str:
        """Generate EASY sample with clear PDPL keywords."""
        
        CLEAR_TEMPLATES = {
            0: [  # Lawfulness
                f"{company} thu thap {context} mot cach hop phap theo quy dinh PDPL.",
                f"{company} xu ly du lieu {context} dua tren co so phap ly ro rang.",
                f"Viec {company} thu thap {context} la hop phap va tuan thu PDPL 2025.",
            ],
            1: [  # Purpose Limitation
                f"{company} chi su dung {context} cho muc dich da noi ro trong chinh sach.",
                f"Du lieu {context} cua {company} chi phuc vu cho muc dich cu the da thong bao.",
                f"{company} dam bao {context} chi duoc xu ly dung muc dich da xac dinh.",
            ],
            2: [  # Data Minimization
                f"{company} chi thu thap {context} toi thieu can thiet cho dich vu.",
                f"Du lieu {context} duoc {company} giam thieu den muc toi da.",
                f"{company} ap dung nguyen tac giam thieu du lieu khi thu thap {context}.",
            ],
            3: [  # Accuracy
                f"{company} dam bao {context} luon chinh xac va cap nhat.",
                f"Du lieu {context} cua {company} duoc kiem tra tinh chinh xac thuong xuyen.",
                f"{company} co co che cap nhat {context} de dam bao do chinh xac.",
            ],
            4: [  # Storage Limitation
                f"{company} chi luu tru {context} trong thoi gian can thiet.",
                f"Du lieu {context} se bi xoa sau khi {company} hoan thanh muc dich xu ly.",
                f"{company} gioi han thoi gian luu tru {context} theo quy dinh.",
            ],
            5: [  # Security
                f"{company} bao mat {context} bang cac bien phap ky thuat phu hop.",
                f"Du lieu {context} duoc {company} bao ve bang ma hoa va kiem soat truy cap.",
                f"{company} ap dung cac bien phap bao mat de bao ve {context}.",
            ],
            6: [  # Transparency
                f"{company} thong bao ro rang ve cach thu thap {context}.",
                f"Nguoi dung duoc {company} thong tin day du ve xu ly {context}.",
                f"{company} minh bach trong viec su dung {context}.",
            ],
            7: [  # Accountability
                f"{company} chiu trach nhiem ve viec xu ly {context}.",
                f"Co che giam sat dam bao {company} chiu trach nhiem voi {context}.",
                f"{company} thiet lap quy trinh de chung minh trach nhiem voi {context}.",
            ]
        }
        
        templates = CLEAR_TEMPLATES.get(category_id, [
            f"{company} xu ly {context} theo quy dinh PDPL."
        ])
        
        return random.choice(templates)
    
    def _generate_subtle_keyword_sample(
        self,
        category_id: int,
        company: str,
        context: str,
        region: str
    ) -> str:
        """Generate MEDIUM difficulty sample with subtle keywords."""
        
        SUBTLE_TEMPLATES = {
            0: [
                f"{company} can {context} de thuc hien hop dong voi khach hang.",
                f"Khi su dung dich vu, ban cho phep {company} truy cap {context}.",
                f"{company} yeu cau {context} trong qua trinh dang ky tai khoan.",
            ],
            1: [
                f"{company} chi dung {context} de xu ly don hang, khong chia se voi ben thu ba.",
                f"Du lieu {context} chi phuc vu cho hoat dong giao hang cua {company}.",
                f"{company} khong su dung {context} cho bat ky muc dich nao khac.",
            ],
            2: [
                f"{company} chi yeu cau {context} thuc su can thiet.",
                f"Viec thu thap {context} cua {company} da duoc toi uu hoa.",
                f"{company} khong thu thap {context} khong lien quan.",
            ],
            3: [
                f"{company} kiem tra {context} de dam bao tinh hop le.",
                f"Ban co the cap nhat {context} tai {company} bat ky luc nao.",
                f"{company} xac nhan {context} truoc khi su dung.",
            ],
            4: [
                f"{company} xoa {context} sau 2 nam khong hoat dong.",
                f"Du lieu {context} duoc {company} luu trong thoi han nhat dinh.",
                f"{company} khong luu tru {context} lau hon muc can thiet.",
            ],
            5: [
                f"{company} bao ve {context} bang cong nghe hien dai.",
                f"He thong cua {company} dam bao an toan cho {context}.",
                f"{company} ap dung tieu chuan bao mat quoc te cho {context}.",
            ],
            6: [
                f"{company} giai thich ro cach su dung {context} trong chinh sach.",
                f"Ban co the xem cach {company} xu ly {context} trong dieu khoan.",
                f"{company} cung cap thong tin ve {context} khi ban yeu cau.",
            ],
            7: [
                f"{company} co DPO giam sat viec xu ly {context}.",
                f"Moi thac mac ve {context} co the gui den {company}.",
                f"{company} bao cao dinh ky ve xu ly {context}.",
            ]
        }
        
        templates = SUBTLE_TEMPLATES.get(category_id, [
            f"{company} quan ly {context} mot cach chuyen nghiep."
        ])
        
        return random.choice(templates)
    
    def _generate_no_keyword_sample(
        self,
        category_id: int,
        company: str,
        context: str,
        formality: str
    ) -> str:
        """Generate HARD sample without obvious PDPL keywords."""
        
        NO_KEYWORD_TEMPLATES = {
            0: {
                'business': [
                    f"{company} thu thap {context} dua tren thoa thuan mua ban giua hai ben.",
                    f"Khi dang ky dich vu, ban da dong y cho {company} su dung {context}.",
                    f"{company} can {context} theo yeu cau cua hop dong.",
                ],
                'casual': [
                    f"Ban da dong y cho {company} thu thap {context} khi dat hang roi nhe.",
                    f"{company} can {context} de giao hang cho ban.",
                    f"Dung {company} tuc la ban chap nhan chia se {context}.",
                ]
            },
            1: {
                'business': [
                    f"{company} chi dung {context} de xu ly don hang.",
                    f"Du lieu {context} chi phuc vu cho hoat dong van chuyen san pham cua {company}.",
                    f"{company} khong chia se {context} voi doi tac.",
                ],
                'casual': [
                    f"{company} chi dung {context} de giao hang thoi, khong lam gi khac dau.",
                    f"Yeu tam, {context} chi de {company} xu ly don hang.",
                    f"{company} khong ban {context} cua ban cho ai het.",
                ]
            },
            2: {
                'business': [
                    f"{company} chi yeu cau {context} can thiet.",
                    f"Viec thu thap {context} da duoc toi gian.",
                    f"{company} khong hoi qua nhieu thong tin.",
                ],
                'casual': [
                    f"{company} khong hoi thua {context} gi ca.",
                    f"Chi can {context} la du roi, {company} khong can gi khac.",
                    f"{company} chi lay thong tin toi thieu thoi.",
                ]
            },
            3: {
                'business': [
                    f"{company} kiem tra {context} truoc khi su dung.",
                    f"Ban nen cap nhat {context} neu co thay doi.",
                    f"{company} xac nhan lai {context} dinh ky.",
                ],
                'casual': [
                    f"Nho cap nhat {context} de {company} khong bi sai nha.",
                    f"{company} se hoi lai neu {context} khong chac chan.",
                    f"Neu {context} thay doi thi bao {company} nhe.",
                ]
            },
            4: {
                'business': [
                    f"{company} xoa {context} sau thoi han.",
                    f"Du lieu {context} khong duoc luu mai mai.",
                    f"{company} chi giu {context} trong thoi gian ho tro.",
                ],
                'casual': [
                    f"{company} se xoa {context} sau mot thoi gian.",
                    f"Khong dung lo, {context} khong bi luu mai dau.",
                    f"{company} chi giu {context} khi can thiet thoi.",
                ]
            },
            5: {
                'business': [
                    f"{company} bao ve {context} bang he thong hien dai.",
                    f"Du lieu {context} duoc ma hoa khi truyen tai.",
                    f"{company} co cac bien phap phong chong hack.",
                ],
                'casual': [
                    f"{company} khoa chat {context} cua ban.",
                    f"Yeu tam, {context} duoc bao ve ky.",
                    f"{company} khong de lo {context} dau.",
                ]
            },
            6: {
                'business': [
                    f"{company} giai thich ro cach su dung {context}.",
                    f"Ban co the doc ve {context} trong dieu khoan.",
                    f"{company} thong bao truoc khi dung {context}.",
                ],
                'casual': [
                    f"{company} noi ro cach dung {context} roi ma.",
                    f"Doc ky chinh sach la biet {company} lam gi voi {context}.",
                    f"{company} khong giau giem gi ca.",
                ]
            },
            7: {
                'business': [
                    f"{company} co bo phan giam sat {context}.",
                    f"Ban co the lien he {company} neu co van de ve {context}.",
                    f"{company} bao cao dinh ky ve xu ly du lieu.",
                ],
                'casual': [
                    f"{company} co nguoi cham soc van de {context} nay.",
                    f"Co gi lien he {company} la duoc.",
                    f"{company} co DPO de xu ly khieu nai.",
                ]
            }
        }
        
        # Get templates for category and formality
        category_templates = NO_KEYWORD_TEMPLATES.get(category_id, {})
        templates = category_templates.get(formality, [])
        
        # Fallback if no templates found
        if not templates:
            # Try any formality for this category
            for form, temps in category_templates.items():
                if temps:
                    templates = temps
                    break
        
        if not templates:
            templates = [f"{company} xu ly {context} theo tieu chuan."]
        
        return random.choice(templates)
    
    def _generate_multi_principle_sample(
        self,
        category_id: int,
        company: str,
        context: str,
        region: str
    ) -> str:
        """Generate VERY_HARD sample with overlapping multiple principles."""
        
        MULTI_PRINCIPLE_TEMPLATES = {
            0: [  # Lawfulness (but mentions purpose, security, storage)
                f"{company} thu thap {context} dua tren hop dong de xu ly don hang, chi su dung cho muc dich nay va xoa sau 2 nam.",
                f"Khi dang ky, ban dong y {company} truy cap {context} phuc vu giao hang, du lieu duoc ma hoa va tu dong xoa sau 1 nam.",
                f"{company} can {context} theo thoa thuan, chi dung cho dich vu, bao mat an toan va khong luu qua 18 thang.",
            ],
            1: [  # Purpose Limitation (but mentions lawfulness, minimization)
                f"{company} chi dung {context} theo hop dong da ky, khong thu thap thua, chi phuc vu cho muc dich cu the.",
                f"Dua tren dong y cua ban, {company} chi xu ly {context} toi thieu cho giao hang, khong cho bat ky muc dich nao khac.",
                f"{company} thu thap {context} hop phap, chi lay thong tin can thiet va chi dung de hoan thanh don hang.",
            ],
            2: [  # Data Minimization (but mentions purpose, accuracy)
                f"{company} chi thu thap {context} toi thieu can cho giao hang, kiem tra tinh chinh xac va chi dung dung muc dich.",
                f"Du lieu {context} duoc {company} toi uu hoa, cap nhat thuong xuyen va chi phuc vu cho xu ly don hang.",
                f"{company} khong thu thap {context} thua, dam bao do chinh xac va chi su dung khi thuc su can.",
            ],
            3: [  # Accuracy (but mentions security, storage)
                f"{company} dam bao {context} chinh xac, bao mat bang ma hoa va chi luu trong thoi han can thiet.",
                f"Du lieu {context} duoc {company} kiem tra, bao ve an toan va tu dong xoa sau thoi gian quy dinh.",
                f"{company} cap nhat {context} dinh ky, ap dung cac bien phap bao mat va khong luu tru lau hon muc can.",
            ],
            4: [  # Storage Limitation (but mentions security, purpose)
                f"{company} chi luu {context} trong 2 nam phuc vu bao hanh, bao mat bang SSL va chi dung cho ho tro khach hang.",
                f"Du lieu {context} bi xoa sau 18 thang, duoc ma hoa khi luu tru va chi phuc vu muc dich da thong bao.",
                f"{company} gioi han luu {context} theo quy dinh, dam bao an toan va chi su dung cho dich vu da dong y.",
            ],
            5: [  # Security (but mentions lawfulness, transparency)
                f"{company} bao mat {context} bang ma hoa dua tren hop dong hop phap va thong bao ro rang cho nguoi dung.",
                f"Du lieu {context} duoc {company} bao ve theo tieu chuan quoc te, thu thap hop ly va co chinh sach minh bach.",
                f"{company} ap dung cac bien phap bao mat, xu ly du lieu hop phap va giai thich ro cach su dung {context}.",
            ],
            6: [  # Transparency (but mentions accountability, purpose)
                f"{company} thong bao ro ve {context}, co DPO giam sat va chi dung cho muc dich da noi.",
                f"Chinh sach cua {company} giai thich cach xu ly {context}, co bo phan chiu trach nhiem va gioi han muc dich su dung.",
                f"{company} minh bach ve {context}, thiet lap co che trach nhiem va dam bao dung muc dich.",
            ],
            7: [  # Accountability (but mentions all principles)
                f"{company} co DPO giam sat {context} duoc thu thap hop phap, toi thieu, chinh xac, bao mat, luu han che va minh bach.",
                f"Bo phan DPO cua {company} dam bao {context} hop ly, dung muc dich, toi uu, chinh xac, an toan, co thoi han va ro rang.",
                f"{company} chiu trach nhiem toan bo quy trinh {context}: hop phap, muc dich ro, du lieu toi thieu, chinh xac, bao mat, xoa dung han, minh bach.",
            ]
        }
        
        templates = MULTI_PRINCIPLE_TEMPLATES.get(category_id, [
            f"{company} xu ly {context} tuan thu tat ca cac nguyen tac PDPL 2025."
        ])
        
        return random.choice(templates)
    
    def generate_dataset(
        self,
        samples_per_category: int = 100,
        num_categories: Optional[int] = None,
        output_file: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate complete dataset with company normalization.
        
        Args:
            samples_per_category (int): Number of samples per category
            num_categories (int, optional): Number of categories (defaults to all for model type)
            output_file (str, optional): Path to save JSONL file
        
        Returns:
            List of normalized samples ready for model training
        """
        # Use all categories for current model type if not specified
        if num_categories is None:
            num_categories = len(self.categories)
        
        # Validate num_categories
        if num_categories > len(self.categories):
            raise ValueError(
                f"num_categories ({num_categories}) exceeds available categories "
                f"({len(self.categories)}) for model type '{self.model_type}'"
            )
        
        dataset = []
        
        # Ambiguity distribution (following production standards)
        composition = {
            'VERY_HARD': 0.40,
            'HARD': 0.40,
            'MEDIUM': 0.14,
            'EASY': 0.06
        }
        
        # Available industries from registry
        industries = list(self.registry_stats['industry_list'])
        
        print(f"Generating dataset for model type: {self.model_type}")
        print(f"Dataset: {samples_per_category} samples x {num_categories} categories")
        print(f"Total samples: {samples_per_category * num_categories}")
        print(f"Ambiguity distribution: {composition}")
        print()
        
        for category_id in range(num_categories):
            category_name = self.categories[category_id]
            print(f"Category {category_id}: {category_name}")
            
            for ambiguity, ratio in composition.items():
                count = int(samples_per_category * ratio)
                
                for i in range(count):
                    # Vary region, formality, industry for diversity
                    sample = self.generate_hard_sample(
                        category_id=category_id,
                        ambiguity=ambiguity,
                        region=random.choice(self.regional_styles),
                        formality=random.choice(self.formality_levels),
                        industry=random.choice(industries) if industries else None
                    )
                    
                    dataset.append(sample)
                
                print(f"  {ambiguity}: {count} samples")
            print()
        
        # Save to file if requested
        if output_file:
            self._save_dataset(dataset, output_file)
            print(f"Dataset saved to: {output_file}")
        
        return dataset
    
    def _save_dataset(self, dataset: List[Dict], output_file: str) -> None:
        """
        Save dataset to JSONL file.
        
        Args:
            dataset (List[Dict]): Generated dataset
            output_file (str): Output file path
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for sample in dataset:
                json.dump(sample, f, ensure_ascii=False)
                f.write('\n')
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get generator statistics and configuration.
        
        Returns:
            Dict with generator stats
        """
        return {
            'model_type': self.model_type,
            'categories': self.categories,
            'num_categories': len(self.categories),
            'company_registry': {
                'total_companies': self.registry_stats['total_companies'],
                'industries': self.registry_stats['industry_list'],
                'regions': self.registry_stats['region_list']
            },
            'configuration': {
                'ambiguity_levels': self.ambiguity_levels,
                'regional_styles': self.regional_styles,
                'formality_levels': self.formality_levels,
                'data_contexts': len(self.data_contexts)
            },
            'available_model_types': list(self.MODEL_TYPES.keys())
        }
