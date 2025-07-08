"""
Core data models for BaZi analysis
"""
from typing import List, Dict, Optional, Tuple
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class WuXing(Enum):
    """五行枚举"""
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"


class YinYang(Enum):
    """阴阳枚举"""
    YANG = "阳"
    YIN = "阴"


class TianGan(BaseModel):
    """天干模型"""
    name: str = Field(..., description="天干名称")
    index: int = Field(..., description="天干序号")
    wu_xing: WuXing = Field(..., description="五行属性")
    yin_yang: YinYang = Field(..., description="阴阳属性")
    temperature: int = Field(..., description="温度值")


class DiZhi(BaseModel):
    """地支模型"""
    name: str = Field(..., description="地支名称")
    index: int = Field(..., description="地支序号")
    wu_xing: WuXing = Field(..., description="五行属性")
    yin_yang: YinYang = Field(..., description="阴阳属性")
    time_range: str = Field(..., description="时辰范围")
    temperature: int = Field(..., description="温度值")
    hidden_stems: Dict[str, int] = Field(default_factory=dict, description="藏干及其力量")


class GanZhi(BaseModel):
    """干支组合模型"""
    gan: TianGan = Field(..., description="天干")
    zhi: DiZhi = Field(..., description="地支")
    name: str = Field(..., description="干支名称")
    number: int = Field(..., description="六十甲子序号")

    @property
    def full_name(self) -> str:
        return f"{self.gan.name}{self.zhi.name}"


class BaZiPillar(BaseModel):
    """八字柱模型（年、月、日、时）"""
    gan_zhi: GanZhi = Field(..., description="干支组合")
    pillar_type: str = Field(..., description="柱类型: 年/月/日/时")
    solar_date: Optional[datetime] = Field(None, description="阳历日期")
    lunar_date: Optional[str] = Field(None, description="农历日期")


class BaZiChart(BaseModel):
    """八字命盘模型"""
    year_pillar: BaZiPillar = Field(..., description="年柱")
    month_pillar: BaZiPillar = Field(..., description="月柱")
    day_pillar: BaZiPillar = Field(..., description="日柱")
    hour_pillar: BaZiPillar = Field(..., description="时柱")
    birth_info: Dict = Field(default_factory=dict, description="出生信息")
    
    @property
    def all_pillars(self) -> List[BaZiPillar]:
        return [self.year_pillar, self.month_pillar, self.day_pillar, self.hour_pillar]
    
    @property
    def all_gans(self) -> List[str]:
        return [pillar.gan_zhi.gan.name for pillar in self.all_pillars]
    
    @property
    def all_zhis(self) -> List[str]:
        return [pillar.gan_zhi.zhi.name for pillar in self.all_pillars]


class TenGods(BaseModel):
    """十神关系模型"""
    name: str = Field(..., description="十神名称")
    description: str = Field(..., description="十神描述")
    relationship_type: str = Field(..., description="关系类型")


class ElementStrength(BaseModel):
    """五行力量分析"""
    wood: float = Field(default=0.0, description="木的力量")
    fire: float = Field(default=0.0, description="火的力量")
    earth: float = Field(default=0.0, description="土的力量")
    metal: float = Field(default=0.0, description="金的力量")
    water: float = Field(default=0.0, description="水的力量")
    
    @property
    def total(self) -> float:
        return self.wood + self.fire + self.earth + self.metal + self.water


class AnalysisResult(BaseModel):
    """分析结果模型"""
    chart: BaZiChart = Field(..., description="八字命盘")
    element_strength: ElementStrength = Field(..., description="五行力量分析")
    ten_gods_analysis: Dict[str, str] = Field(default_factory=dict, description="十神分析")
    special_patterns: List[str] = Field(default_factory=list, description="特殊格局")
    monthly_analysis: Optional[str] = Field(None, description="月令分析")
    time_analysis: Optional[str] = Field(None, description="时辰分析")
    general_fortune: Optional[str] = Field(None, description="总体运势")
    recommendations: List[str] = Field(default_factory=list, description="建议")
