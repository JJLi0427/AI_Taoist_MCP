"""
Utility functions for BaZi analysis
"""
from typing import List, Dict, Tuple
from core.models import BaZiChart
from data.loader import DIZHI_DICT, TIANGAN_DICT


class BaZiUtils:
    """八字工具类"""
    
    @staticmethod
    def check_gan_he(gan1: str, gan2: str) -> bool:
        """检查天干相合"""
        he_pairs = [
            ("甲", "己"), ("乙", "庚"), ("丙", "辛"), 
            ("丁", "壬"), ("戊", "癸")
        ]
        return (gan1, gan2) in he_pairs or (gan2, gan1) in he_pairs
    
    @staticmethod
    def check_gan_chong(gan1: str, gan2: str) -> bool:
        """检查天干相冲"""
        chong_pairs = [
            ("甲", "庚"), ("乙", "辛"), ("丙", "壬"), ("丁", "癸")
        ]
        return (gan1, gan2) in chong_pairs or (gan2, gan1) in chong_pairs
    
    @staticmethod
    def check_zhi_he(zhi1: str, zhi2: str) -> bool:
        """检查地支相合"""
        he_pairs = [
            ("子", "丑"), ("寅", "亥"), ("卯", "戌"), 
            ("辰", "酉"), ("巳", "申"), ("午", "未")
        ]
        return (zhi1, zhi2) in he_pairs or (zhi2, zhi1) in he_pairs
    
    @staticmethod
    def check_zhi_chong(zhi1: str, zhi2: str) -> bool:
        """检查地支相冲"""
        chong_pairs = [
            ("子", "午"), ("丑", "未"), ("寅", "申"), 
            ("卯", "酉"), ("辰", "戌"), ("巳", "亥")
        ]
        return (zhi1, zhi2) in chong_pairs or (zhi2, zhi1) in chong_pairs
    
    @staticmethod
    def check_zhi_xing(zhi1: str, zhi2: str, zhi3: str) -> str:
        """检查地支三刑"""
        xing_groups = [
            ["子", "卯"],  # 子卯相刑
            ["寅", "巳", "申"],  # 寅巳申三刑
            ["丑", "未", "戌"],  # 丑未戌三刑
            ["辰", "辰"], ["午", "午"], ["酉", "酉"], ["亥", "亥"]  # 自刑
        ]
        
        zhis = [zhi1, zhi2, zhi3]
        for group in xing_groups:
            if all(zhi in group for zhi in zhis if zhi in group):
                if len(group) == 2 and len([z for z in zhis if z in group]) >= 2:
                    return f"{''.join(group)}相刑"
                elif len(group) == 3 and all(g in zhis for g in group):
                    return f"{''.join(group)}三刑"
                elif len(group) == 1 and zhis.count(group[0]) >= 2:
                    return f"{group[0]}自刑"
        
        return ""
    
    @staticmethod
    def check_zhi_harm(zhi1: str, zhi2: str) -> bool:
        """检查地支相害"""
        harm_pairs = [
            ("子", "未"), ("丑", "午"), ("寅", "巳"), 
            ("卯", "辰"), ("申", "亥"), ("酉", "戌")
        ]
        return (zhi1, zhi2) in harm_pairs or (zhi2, zhi1) in harm_pairs
    
    @staticmethod
    def check_zhi_ju(zhis: List[str]) -> List[str]:
        """检查地支合局"""
        ju_patterns = [
            (["亥", "卯", "未"], "木局"),
            (["寅", "午", "戌"], "火局"),
            (["巳", "酉", "丑"], "金局"),
            (["申", "子", "辰"], "水局"),
            (["辰", "戌", "丑", "未"], "土局")
        ]
        
        results = []
        for pattern, name in ju_patterns:
            if len(pattern) == 3:
                # 三合局
                if all(p in zhis for p in pattern):
                    results.append(f"{name}三合")
                # 半合局
                elif sum(1 for p in pattern if p in zhis) >= 2:
                    found = [p for p in pattern if p in zhis]
                    results.append(f"{''.join(found)}半合{name}")
            else:
                # 四库土局
                if sum(1 for p in pattern if p in zhis) >= 3:
                    results.append(name)
        
        return results
    
    @staticmethod
    def get_empty_death(day_pillar: str) -> List[str]:
        """获取旬空亡"""
        empty_map = {
            "甲子": ["戌", "亥"], "甲戌": ["申", "酉"], "甲申": ["午", "未"],
            "甲午": ["辰", "巳"], "甲辰": ["寅", "卯"], "甲寅": ["子", "丑"]
        }
        
        # 找到对应的旬
        for xun, empty in empty_map.items():
            if day_pillar.startswith(xun[0]):
                return empty
        
        return []
    
    @staticmethod
    def calculate_yinyang_score(chart: BaZiChart) -> Dict[str, int]:
        """计算阴阳分数"""
        yang_count = 0
        yin_count = 0
        
        for pillar in chart.all_pillars:
            # 天干阴阳
            if pillar.gan_zhi.gan.yin_yang.value == "阳":
                yang_count += 1
            else:
                yin_count += 1
            
            # 地支阴阳
            if pillar.gan_zhi.zhi.yin_yang.value == "阳":
                yang_count += 1
            else:
                yin_count += 1
        
        return {"阳": yang_count, "阴": yin_count}
    
    @staticmethod
    def format_chart_display(chart: BaZiChart) -> str:
        """格式化八字显示"""
        lines = []
        lines.append("=" * 50)
        lines.append("八字排盘".center(46))
        lines.append("=" * 50)
        
        # 天干行
        gan_line = "    ".join([
            pillar.gan_zhi.gan.name for pillar in chart.all_pillars
        ])
        lines.append(f"天干: {gan_line}")
        
        # 地支行
        zhi_line = "    ".join([
            pillar.gan_zhi.zhi.name for pillar in chart.all_pillars
        ])
        lines.append(f"地支: {zhi_line}")
        
        # 柱名行
        pillar_line = "    ".join([
            f"{pillar.pillar_type}柱" for pillar in chart.all_pillars
        ])
        lines.append(f"      {pillar_line}")
        
        lines.append("=" * 50)
        
        return "\n".join(lines)


class ColorUtils:
    """颜色工具类"""
    
    COLORS = {
        "木": "\033[32m",  # 绿色
        "火": "\033[31m",  # 红色
        "土": "\033[33m",  # 黄色
        "金": "\033[37m",  # 白色
        "水": "\033[34m",  # 蓝色
        "reset": "\033[0m"  # 重置颜色
    }
    
    @classmethod
    def colorize_wuxing(cls, text: str, wuxing: str) -> str:
        """为五行文字添加颜色"""
        color = cls.COLORS.get(wuxing, "")
        reset = cls.COLORS["reset"]
        return f"{color}{text}{reset}"
    
    @classmethod
    def colorize_gan(cls, gan: str) -> str:
        """为天干添加颜色"""
        gan_obj = TIANGAN_DICT.get(gan)
        if gan_obj:
            return cls.colorize_wuxing(gan, gan_obj.wu_xing.value)
        return gan
    
    @classmethod
    def colorize_zhi(cls, zhi: str) -> str:
        """为地支添加颜色"""
        zhi_obj = DIZHI_DICT.get(zhi)
        if zhi_obj:
            return cls.colorize_wuxing(zhi, zhi_obj.wu_xing.value)
        return zhi
