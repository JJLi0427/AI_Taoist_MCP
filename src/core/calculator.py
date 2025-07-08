"""
BaZi calculation engine
"""
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from lunar_python import Lunar, Solar

from core.models import (
    BaZiChart, BaZiPillar, GanZhi, TianGan, DiZhi,
    WuXing, YinYang, ElementStrength
)
from data.loader import TIANGAN_DICT, DIZHI_DICT, GANZHI_60


class BaZiCalculator:
    """八字计算器"""
    
    def __init__(self):
        self.tiangan_list = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        self.dizhi_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    def create_ganzhi(self, gan_name: str, zhi_name: str) -> GanZhi:
        """创建干支组合"""
        gan = TIANGAN_DICT[gan_name]
        zhi = DIZHI_DICT[zhi_name]
        
        # 计算六十甲子序号
        gan_index = self.tiangan_list.index(gan_name)
        zhi_index = self.dizhi_list.index(zhi_name)
        
        # 使用六十甲子公式计算序号
        number = None
        ganzhi_name = f"{gan_name}{zhi_name}"
        for num, name in GANZHI_60.items():
            if name == ganzhi_name:
                number = int(num)
                break
        
        return GanZhi(
            gan=gan,
            zhi=zhi,
            name=ganzhi_name,
            number=number or 1
        )
    
    def calculate_bazi_from_datetime(
        self, 
        birth_datetime: datetime, 
        is_male: bool = True,
        timezone_offset: int = 8
    ) -> BaZiChart:
        """从出生时间计算八字"""
        
        # 转换为Solar对象
        solar = Solar.fromYmdHms(
            birth_datetime.year,
            birth_datetime.month,
            birth_datetime.day,
            birth_datetime.hour,
            birth_datetime.minute,
            birth_datetime.second
        )
        
        # 转换为农历
        lunar = solar.getLunar()
        
        # 获取八字
        bazi = lunar.getEightChar()
        
        # 创建年柱
        year_pillar = BaZiPillar(
            gan_zhi=self.create_ganzhi(bazi.getYear()[0], bazi.getYear()[1]),
            pillar_type="年",
            solar_date=birth_datetime,
            lunar_date=f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}"
        )
        
        # 创建月柱
        month_pillar = BaZiPillar(
            gan_zhi=self.create_ganzhi(bazi.getMonth()[0], bazi.getMonth()[1]),
            pillar_type="月",
            solar_date=birth_datetime,
            lunar_date=f"{lunar.getMonthInChinese()}月"
        )
        
        # 创建日柱
        day_pillar = BaZiPillar(
            gan_zhi=self.create_ganzhi(bazi.getDay()[0], bazi.getDay()[1]),
            pillar_type="日",
            solar_date=birth_datetime,
            lunar_date=f"{lunar.getDayInChinese()}"
        )
        
        # 创建时柱
        hour_pillar = BaZiPillar(
            gan_zhi=self.create_ganzhi(bazi.getTime()[0], bazi.getTime()[1]),
            pillar_type="时",
            solar_date=birth_datetime,
            lunar_date=""
        )
        
        # 创建八字命盘
        chart = BaZiChart(
            year_pillar=year_pillar,
            month_pillar=month_pillar,
            day_pillar=day_pillar,
            hour_pillar=hour_pillar,
            birth_info={
                "solar_date": birth_datetime.isoformat(),
                "lunar_date": f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}",
                "is_male": is_male,
                "timezone_offset": timezone_offset
            }
        )
        
        return chart
    
    def calculate_element_strength(self, chart: BaZiChart) -> ElementStrength:
        """计算五行力量"""
        strength = ElementStrength()
        
        # 天干力量基础值
        gan_base_power = 10
        # 地支力量基础值  
        zhi_base_power = 12
        # 藏干力量基础值
        hidden_base_power = 1
        
        for pillar in chart.all_pillars:
            gan = pillar.gan_zhi.gan
            zhi = pillar.gan_zhi.zhi
            
            # 计算天干五行力量
            self._add_element_strength(strength, gan.wu_xing, gan_base_power)
            
            # 计算地支本气五行力量
            self._add_element_strength(strength, zhi.wu_xing, zhi_base_power)
            
            # 计算地支藏干五行力量
            for hidden_gan_name, power in zhi.hidden_stems.items():
                hidden_gan = TIANGAN_DICT[hidden_gan_name]
                self._add_element_strength(
                    strength, 
                    hidden_gan.wu_xing, 
                    power * hidden_base_power
                )
        
        return strength
    
    def _add_element_strength(self, strength: ElementStrength, wu_xing: WuXing, power: float):
        """添加五行力量"""
        if wu_xing == WuXing.WOOD:
            strength.wood += power
        elif wu_xing == WuXing.FIRE:
            strength.fire += power
        elif wu_xing == WuXing.EARTH:
            strength.earth += power
        elif wu_xing == WuXing.METAL:
            strength.metal += power
        elif wu_xing == WuXing.WATER:
            strength.water += power
    
    def get_ten_gods_relationship(self, day_gan: str, target_gan: str) -> str:
        """获取十神关系"""
        day_index = self.tiangan_list.index(day_gan)
        target_index = self.tiangan_list.index(target_gan)
        
        # 计算五行关系
        day_wuxing = TIANGAN_DICT[day_gan].wu_xing
        target_wuxing = TIANGAN_DICT[target_gan].wu_xing
        
        # 计算阴阳关系
        day_yinyang = TIANGAN_DICT[day_gan].yin_yang
        target_yinyang = TIANGAN_DICT[target_gan].yin_yang
        same_yinyang = day_yinyang == target_yinyang
        
        # 根据五行关系和阴阳关系确定十神
        if day_wuxing == target_wuxing:
            return "比肩" if same_yinyang else "劫财"
        elif self._is_sheng_relationship(day_wuxing, target_wuxing):  # 我生
            return "食神" if same_yinyang else "伤官"
        elif self._is_ke_relationship(day_wuxing, target_wuxing):  # 我克
            return "偏财" if same_yinyang else "正财"
        elif self._is_ke_relationship(target_wuxing, day_wuxing):  # 克我
            return "七杀" if same_yinyang else "正官"
        elif self._is_sheng_relationship(target_wuxing, day_wuxing):  # 生我
            return "偏印" if same_yinyang else "正印"
        else:
            return "未知"
    
    def _is_sheng_relationship(self, source: WuXing, target: WuXing) -> bool:
        """判断是否为相生关系"""
        sheng_map = {
            WuXing.WOOD: WuXing.FIRE,
            WuXing.FIRE: WuXing.EARTH,
            WuXing.EARTH: WuXing.METAL,
            WuXing.METAL: WuXing.WATER,
            WuXing.WATER: WuXing.WOOD,
        }
        return sheng_map.get(source) == target
    
    def _is_ke_relationship(self, source: WuXing, target: WuXing) -> bool:
        """判断是否为相克关系"""
        ke_map = {
            WuXing.WOOD: WuXing.EARTH,
            WuXing.EARTH: WuXing.WATER,
            WuXing.WATER: WuXing.FIRE,
            WuXing.FIRE: WuXing.METAL,
            WuXing.METAL: WuXing.WOOD,
        }
        return ke_map.get(source) == target
