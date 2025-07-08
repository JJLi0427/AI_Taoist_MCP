"""
简单示例：演示新八字分析系统的使用
"""
import sys
from pathlib import Path
from datetime import datetime

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from core.calculator import BaZiCalculator
    from analysis.analyzer import BaZiAnalyzer
    from utils.helpers import BaZiUtils
    
    def main():
        print("="*60)
        print("八字分析系统演示".center(54))
        print("="*60)
        
        # 创建分析器
        calculator = BaZiCalculator()
        analyzer = BaZiAnalyzer()
        
        # 示例：分析一个八字
        birth_time = datetime(1990, 5, 15, 14, 30)
        print(f"\n分析出生时间: {birth_time}")
        
        try:
            # 计算八字
            chart = calculator.calculate_bazi_from_datetime(birth_time, is_male=True)
            print(f"\n八字排盘:")
            print(f"年柱: {chart.year_pillar.gan_zhi.name}")
            print(f"月柱: {chart.month_pillar.gan_zhi.name}")
            print(f"日柱: {chart.day_pillar.gan_zhi.name}")
            print(f"时柱: {chart.hour_pillar.gan_zhi.name}")
            
            # 分析八字
            result = analyzer.analyze_chart(chart)
            
            print(f"\n五行力量分析:")
            strength = result.element_strength
            print(f"木: {strength.wood:.1f}")
            print(f"火: {strength.fire:.1f}")
            print(f"土: {strength.earth:.1f}")
            print(f"金: {strength.metal:.1f}")
            print(f"水: {strength.water:.1f}")
            
            if result.general_fortune:
                print(f"\n总体分析:")
                print(result.general_fortune)
            
            if result.recommendations:
                print(f"\n建议:")
                for i, rec in enumerate(result.recommendations[:3], 1):
                    print(f"{i}. {rec}")
            
            print("\n系统运行正常！")
            
        except Exception as e:
            print(f"分析过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保所有依赖包已正确安装：")
    print("pip install bidict lunar-python colorama pydantic click rich")
except Exception as e:
    print(f"运行时错误: {e}")
    import traceback
    traceback.print_exc()
