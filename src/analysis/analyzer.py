"""
BaZi analysis engine
"""
from typing import Dict, List, Optional
import json

from core.models import BaZiChart, AnalysisResult, ElementStrength
from core.calculator import BaZiCalculator
from data.loader import data_loader


class BaZiAnalyzer:
    """八字分析器"""
    
    def __init__(self):
        self.calculator = BaZiCalculator()
        self.monthly_data = self._load_monthly_data()
        self.time_data = self._load_time_data()
        self.ten_gods_data = data_loader.load_ten_gods_data()
    
    def _load_monthly_data(self) -> Dict:
        """加载月令分析数据"""
        try:
            return data_loader.load_json("monthly_analysis.json")
        except FileNotFoundError:
            return {"monthly_analysis": {}}
    
    def _load_time_data(self) -> Dict:
        """加载时辰分析数据"""
        try:
            return data_loader.load_json("time_analysis.json")
        except FileNotFoundError:
            return {"time_analysis": {}}
    
    def analyze_chart(self, chart: BaZiChart) -> AnalysisResult:
        """分析八字命盘"""
        
        # 计算五行力量
        element_strength = self.calculator.calculate_element_strength(chart)
        
        # 十神分析
        ten_gods_analysis = self._analyze_ten_gods(chart)
        
        # 特殊格局分析
        special_patterns = self._analyze_special_patterns(chart)
        
        # 月令分析
        monthly_analysis = self._analyze_monthly(chart)
        
        # 时辰分析
        time_analysis = self._analyze_time(chart)
        
        # 总体运势
        general_fortune = self._analyze_general_fortune(chart, element_strength)
        
        # 生活建议
        recommendations = self._generate_recommendations(chart, element_strength)
        
        return AnalysisResult(
            chart=chart,
            element_strength=element_strength,
            ten_gods_analysis=ten_gods_analysis,
            special_patterns=special_patterns,
            monthly_analysis=monthly_analysis,
            time_analysis=time_analysis,
            general_fortune=general_fortune,
            recommendations=recommendations
        )
    
    def _analyze_ten_gods(self, chart: BaZiChart) -> Dict[str, str]:
        """分析十神关系"""
        day_gan = chart.day_pillar.gan_zhi.gan.name
        analysis = {}
        
        for pillar in chart.all_pillars:
            if pillar.pillar_type != "日":
                gan_name = pillar.gan_zhi.gan.name
                ten_god = self.calculator.get_ten_gods_relationship(day_gan, gan_name)
                analysis[f"{pillar.pillar_type}干_{gan_name}"] = ten_god
                
                # 分析地支藏干
                zhi = pillar.gan_zhi.zhi
                for hidden_gan, _ in zhi.hidden_stems.items():
                    if hidden_gan != day_gan:
                        hidden_ten_god = self.calculator.get_ten_gods_relationship(day_gan, hidden_gan)
                        analysis[f"{pillar.pillar_type}支藏干_{hidden_gan}"] = hidden_ten_god
        
        return analysis
    
    def _analyze_special_patterns(self, chart: BaZiChart) -> List[str]:
        """分析特殊格局"""
        patterns = []
        
        # 检查四同类型格局
        gans = chart.all_gans
        zhis = chart.all_zhis
        
        # 检查全阳或全阴
        if self._check_all_yang_or_yin(chart):
            if all(self._is_yang(gan) for gan in gans) and all(self._is_yang(zhi) for zhi in zhis):
                patterns.append("四柱全阳")
            elif all(self._is_yin(gan) for gan in gans) and all(self._is_yin(zhi) for zhi in zhis):
                patterns.append("四柱全阴")
        
        # 检查木火通明格局
        if self._check_wood_fire_pattern(chart):
            patterns.append("木火通明")
        
        # 检查金水相涵格局
        if self._check_metal_water_pattern(chart):
            patterns.append("金水相涵")
        
        return patterns
    
    def _analyze_monthly(self, chart: BaZiChart) -> Optional[str]:
        """分析月令"""
        day_gan = chart.day_pillar.gan_zhi.gan.name
        month_zhi = chart.month_pillar.gan_zhi.zhi.name
        
        # 根据月支确定季节
        season = self._get_season_by_month(month_zhi)
        
        monthly_data = self.monthly_data.get("monthly_analysis", {})
        gan_data = monthly_data.get(day_gan, {})
        season_data = gan_data.get(season)
        
        if season_data:
            return f"{season_data['title']}: {season_data['analysis']}"
        
        return f"{day_gan}日生于{season}月，需要根据具体情况分析。"
    
    def _analyze_time(self, chart: BaZiChart) -> Optional[str]:
        """分析时辰"""
        day_combo = f"{chart.day_pillar.gan_zhi.name}"
        hour_combo = f"{chart.hour_pillar.gan_zhi.name}"
        time_key = f"{chart.day_pillar.gan_zhi.gan.name}日{chart.hour_pillar.gan_zhi.name}"
        
        time_data = self.time_data.get("time_analysis", {})
        specific_data = time_data.get(time_key)
        
        if specific_data:
            analysis = specific_data["analysis"]
            specific_combo = specific_data.get("specific_combinations", {}).get(f"{day_combo}日{hour_combo}时")
            if specific_combo:
                analysis += f" 具体组合：{specific_combo}"
            return analysis
        
        return f"{chart.day_pillar.gan_zhi.gan.name}日{chart.hour_pillar.gan_zhi.name}时，需要根据具体情况分析。"
    
    def _analyze_general_fortune(self, chart: BaZiChart, element_strength: ElementStrength) -> str:
        """分析总体运势"""
        analysis = []
        
        # 分析五行平衡
        total_strength = element_strength.total
        if total_strength > 0:
            wood_ratio = element_strength.wood / total_strength
            fire_ratio = element_strength.fire / total_strength
            earth_ratio = element_strength.earth / total_strength
            metal_ratio = element_strength.metal / total_strength
            water_ratio = element_strength.water / total_strength
            
            # 找出最强和最弱的五行
            element_ratios = {
                "木": wood_ratio,
                "火": fire_ratio,
                "土": earth_ratio,
                "金": metal_ratio,
                "水": water_ratio
            }
            
            strongest = max(element_ratios, key=element_ratios.get)
            weakest = min(element_ratios, key=element_ratios.get)
            
            analysis.append(f"五行以{strongest}最强，{weakest}最弱。")
            
            # 判断五行是否平衡
            if max(element_ratios.values()) - min(element_ratios.values()) < 0.3:
                analysis.append("五行相对平衡，命局较为稳定。")
            else:
                analysis.append("五行失衡，需要调理补充。")
        
        # 分析日主强弱
        day_gan_wuxing = chart.day_pillar.gan_zhi.gan.wu_xing.value
        day_strength = getattr(element_strength, day_gan_wuxing.lower(), 0)
        
        if day_strength / total_strength > 0.3:
            analysis.append("日主偏强，适合泄耗。")
        elif day_strength / total_strength < 0.15:
            analysis.append("日主偏弱，需要扶助。")
        else:
            analysis.append("日主强弱适中。")
        
        return " ".join(analysis)
    
    def _generate_recommendations(self, chart: BaZiChart, element_strength: ElementStrength) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 根据五行强弱给出建议
        total = element_strength.total
        if total > 0:
            element_ratios = {
                "木": element_strength.wood / total,
                "火": element_strength.fire / total,
                "土": element_strength.earth / total,
                "金": element_strength.metal / total,
                "水": element_strength.water / total
            }
            
            weakest = min(element_ratios, key=element_ratios.get)
            
            # 根据最弱五行给出建议
            element_advice = {
                "木": ["适合东方发展", "宜从事文教、出版、木材相关行业", "有利颜色：绿色"],
                "火": ["适合南方发展", "宜从事能源、电子、娱乐相关行业", "有利颜色：红色"],
                "土": ["适合中部发展", "宜从事房地产、农业、陶瓷相关行业", "有利颜色：黄色"],
                "金": ["适合西方发展", "宜从事金融、机械、金属相关行业", "有利颜色：白色"],
                "水": ["适合北方发展", "宜从事贸易、物流、水产相关行业", "有利颜色：黑色"]
            }
            
            if weakest in element_advice:
                recommendations.extend([f"补充{weakest}之不足：{advice}" for advice in element_advice[weakest]])
        
        return recommendations
    
    def _check_all_yang_or_yin(self, chart: BaZiChart) -> bool:
        """检查是否全阳或全阴"""
        return True  # 简化实现
    
    def _is_yang(self, char: str) -> bool:
        """判断是否为阳性"""
        yang_chars = ["甲", "丙", "戊", "庚", "壬", "子", "寅", "辰", "午", "申", "戌"]
        return char in yang_chars
    
    def _is_yin(self, char: str) -> bool:
        """判断是否为阴性"""
        return not self._is_yang(char)
    
    def _check_wood_fire_pattern(self, chart: BaZiChart) -> bool:
        """检查木火通明格局"""
        # 简化实现，检查是否有木火相生
        return True  # 需要更复杂的逻辑
    
    def _check_metal_water_pattern(self, chart: BaZiChart) -> bool:
        """检查金水相涵格局"""
        # 简化实现
        return True  # 需要更复杂的逻辑
    
    def _get_season_by_month(self, month_zhi: str) -> str:
        """根据月支确定季节"""
        season_map = {
            "寅": "春月", "卯": "春月", "辰": "春月",
            "巳": "夏月", "午": "夏月", "未": "夏月",
            "申": "秋月", "酉": "秋月", "戌": "秋月",
            "亥": "冬月", "子": "冬月", "丑": "冬月"
        }
        return season_map.get(month_zhi, "未知月份")
