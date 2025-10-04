"""
Vietnamese Cultural Intelligence Module
Provides cultural context and business intelligence for Vietnamese market
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import pytz
from enum import Enum

class VietnameseRegion(Enum):
    """Vietnamese regional business contexts"""
    NORTH = "northern_vietnam"  # Hanoi region
    SOUTH = "southern_vietnam"  # Ho Chi Minh City region  
    CENTRAL = "central_vietnam" # Da Nang, Hue region

class BusinessSector(Enum):
    """Vietnamese business sectors"""
    TECHNOLOGY = "technology"
    MANUFACTURING = "manufacturing"
    FINANCE = "finance_banking"
    RETAIL = "retail_commerce"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    GOVERNMENT = "government_public"

class VietnameseCulturalIntelligence:
    """
    Vietnamese Cultural Intelligence System for PDPL 2025 Compliance
    Provides cultural context, business practices, and localization for Vietnamese enterprises
    """
    
    def __init__(self):
        self.timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        self.provinces = self._load_vietnamese_provinces()
        self.business_cultures = self._load_business_cultures()
        
    def _load_vietnamese_provinces(self) -> List[str]:
        """Load Vietnamese provinces for business validation"""
        return [
            # Major business centers
            "Hà Nội", "Thành phố Hồ Chí Minh", "Đà Nẵng", "Hải Phòng",
            "Cần Thơ", "Biên Hòa", "Nha Trang", "Huế", "Quy Nhon",
            
            # Northern provinces
            "Hà Giang", "Cao Bằng", "Bắc Kạn", "Tuyên Quang", "Lào Cai",
            "Điện Biên", "Lai Châu", "Sơn La", "Yên Bái", "Hòa Bình",
            "Thái Nguyên", "Lạng Sơn", "Quảng Ninh", "Bắc Giang", "Phú Thọ",
            
            # Central provinces  
            "Nghệ An", "Hà Tĩnh", "Quảng Bình", "Quảng Trị", "Thừa Thiên Huế",
            "Quảng Nam", "Quảng Ngãi", "Bình Định", "Phú Yên", "Khánh Hòa",
            "Ninh Thuận", "Bình Thuận", "Kon Tum", "Gia Lai", "Đắk Lắk",
            
            # Southern provinces
            "Lâm Đồng", "Bình Phước", "Tây Ninh", "Bình Dương", "Đồng Nai",
            "Bà Rịa - Vũng Tàu", "Long An", "Tiền Giang", "Bến Tre", "Trà Vinh",
            "Vĩnh Long", "Đồng Tháp", "An Giang", "Kiên Giang", "Cà Mau"
        ]
    
    def _load_business_cultures(self) -> Dict[VietnameseRegion, Dict]:
        """Load Vietnamese regional business cultures"""
        return {
            VietnameseRegion.NORTH: {
                "formality_level": "high",
                "hierarchy_importance": "critical", 
                "government_proximity": "very_high",
                "communication_style": "formal_vietnamese",
                "meeting_preferences": "structured_hierarchical",
                "decision_speed": "deliberate",
                "cultural_notes": "Traditional business protocols, government influence"
            },
            VietnameseRegion.SOUTH: {
                "formality_level": "moderate",
                "hierarchy_importance": "important",
                "government_proximity": "moderate", 
                "communication_style": "business_mix",
                "meeting_preferences": "results_oriented",
                "decision_speed": "faster",
                "cultural_notes": "International business exposure, entrepreneurial"
            },
            VietnameseRegion.CENTRAL: {
                "formality_level": "traditional",
                "hierarchy_importance": "high",
                "government_proximity": "moderate",
                "communication_style": "respectful_traditional",
                "meeting_preferences": "consensus_building", 
                "decision_speed": "careful",
                "cultural_notes": "Cultural preservation focus, traditional values"
            }
        }
    
    def get_regional_context(self, region: VietnameseRegion) -> Dict[str, Any]:
        """Get cultural business context for Vietnamese region"""
        return self.business_cultures.get(region, {})
    
    def get_sector_practices(self, sector: BusinessSector) -> Dict[str, Any]:
        """Get Vietnamese business sector practices"""
        practices = {
            BusinessSector.TECHNOLOGY: {
                "meeting_style": "informal_collaborative",
                "decision_speed": "fast",
                "compliance_focus": "data_security_critical",
                "communication": "technical_vietnamese_english_mix",
                "innovation_openness": "high"
            },
            BusinessSector.MANUFACTURING: {
                "meeting_style": "structured_formal",
                "decision_speed": "deliberate", 
                "compliance_focus": "worker_data_supply_chain",
                "communication": "formal_vietnamese_preferred",
                "safety_priority": "critical"
            },
            BusinessSector.FINANCE: {
                "meeting_style": "highly_formal",
                "decision_speed": "careful_risk_managed",
                "compliance_focus": "customer_data_audit_trails",
                "communication": "formal_vietnamese_required",
                "regulatory_adherence": "strict"
            }
        }
        return practices.get(sector, {})
    
    def validate_vietnamese_business_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Vietnamese business data format and content"""
        validation_result = {
            "valid": True,
            "errors": [],
            "cultural_suggestions": []
        }
        
        # Validate province if provided
        if "province" in data:
            if data["province"] not in self.provinces:
                validation_result["valid"] = False
                validation_result["errors"].append("Invalid Vietnamese province")
        
        # Validate Vietnamese business name format
        if "company_name" in data:
            name = data["company_name"]
            if not any(char in "aàáảãạăằắẳẵặâầấẩẫậeèéẻẽẹêềếểễệiìíỉĩịoòóỏõọôồốổỗộơờớởỡợuùúủũụưừứửữựyỳýỷỹỵ" for char in name.lower()):
                validation_result["cultural_suggestions"].append("Consider Vietnamese language elements in company name")
        
        return validation_result
    
    def get_pdpl_cultural_guidance(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get PDPL 2025 compliance guidance with Vietnamese cultural context"""
        region = context.get("region", VietnameseRegion.SOUTH)
        sector = context.get("sector", BusinessSector.TECHNOLOGY)
        
        regional_context = self.get_regional_context(region)
        sector_practices = self.get_sector_practices(sector)
        
        return {
            "compliance_approach": self._get_compliance_approach(regional_context, sector_practices),
            "communication_guidelines": self._get_communication_guidelines(regional_context),
            "implementation_timeline": self._get_implementation_timeline(sector_practices),
            "vietnamese_requirements": {
                "language": "Vietnamese mandatory for all data subject notices",
                "cultural_adaptation": "Respect for hierarchy in consent processes",
                "local_practices": "Align with Vietnamese business customs"
            }
        }
    
    def _get_compliance_approach(self, regional: Dict, sector: Dict) -> str:
        """Determine culturally appropriate compliance approach"""
        if regional.get("formality_level") == "high":
            return "formal_structured_approach"
        elif sector.get("decision_speed") == "fast":
            return "agile_iterative_approach"
        else:
            return "balanced_collaborative_approach"
    
    def _get_communication_guidelines(self, regional: Dict) -> Dict[str, str]:
        """Get Vietnamese communication guidelines"""
        style = regional.get("communication_style", "business_mix")
        
        guidelines = {
            "formal_vietnamese": {
                "tone": "Respectful and formal",
                "language": "Proper Vietnamese required",
                "hierarchy": "Address senior roles appropriately"
            },
            "business_mix": {
                "tone": "Professional but approachable",
                "language": "Vietnamese preferred, English acceptable",
                "hierarchy": "Moderate formality required"
            }
        }
        
        return guidelines.get(style, guidelines["business_mix"])
    
    def _get_implementation_timeline(self, sector: Dict) -> Dict[str, str]:
        """Get culturally appropriate implementation timeline"""
        speed = sector.get("decision_speed", "deliberate")
        
        if speed == "fast":
            return {"phase1": "2-4 weeks", "phase2": "1-2 months", "full_implementation": "3-4 months"}
        elif speed == "careful_risk_managed":
            return {"phase1": "1-2 months", "phase2": "3-4 months", "full_implementation": "6-8 months"}
        else:
            return {"phase1": "3-4 weeks", "phase2": "2-3 months", "full_implementation": "4-6 months"}
    
    def get_current_vietnam_time(self) -> datetime:
        """Get current Vietnam time"""
        return datetime.now(self.timezone)
    
    def format_vietnamese_datetime(self, dt: datetime = None) -> str:
        """Format datetime for Vietnamese context"""
        if dt is None:
            dt = self.get_current_vietnam_time()
        return dt.strftime("%d/%m/%Y %H:%M:%S")