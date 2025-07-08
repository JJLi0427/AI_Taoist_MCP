"""
Command line interface for BaZi analyzer
"""
import click
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from core.calculator import BaZiCalculator
from analysis.analyzer import BaZiAnalyzer
from utils.helpers import BaZiUtils, ColorUtils


console = Console()


@click.group()
def cli():
    """八字分析命令行工具"""
    pass


@cli.command()
@click.option('--year', '-y', type=int, required=True, help='出生年份')
@click.option('--month', '-m', type=int, required=True, help='出生月份')
@click.option('--day', '-d', type=int, required=True, help='出生日期')
@click.option('--hour', '-h', type=int, default=12, help='出生小时 (0-23)')
@click.option('--minute', type=int, default=0, help='出生分钟')
@click.option('--male/--female', default=True, help='性别 (默认男性)')
@click.option('--timezone', type=int, default=8, help='时区偏移 (默认东八区)')
@click.option('--detailed', '-v', is_flag=True, help='显示详细分析')
def analyze(year, month, day, hour, minute, male, timezone, detailed):
    """分析八字命盘"""
    try:
        # 创建出生时间
        birth_datetime = datetime(year, month, day, hour, minute)
        
        # 计算八字
        calculator = BaZiCalculator()
        chart = calculator.calculate_bazi_from_datetime(birth_datetime, male, timezone)
        
        # 分析八字
        analyzer = BaZiAnalyzer()
        result = analyzer.analyze_chart(chart)
        
        # 显示结果
        display_analysis_result(result, detailed)
        
    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")


def display_analysis_result(result, detailed=False):
    """显示分析结果"""
    chart = result.chart
    
    # 显示基本信息
    console.print(Panel.fit(
        f"性别: {'男' if chart.birth_info.get('is_male', True) else '女'}\n"
        f"阳历: {chart.birth_info.get('solar_date', '').split('T')[0]}\n"
        f"农历: {chart.birth_info.get('lunar_date', '')}",
        title="[bold blue]出生信息[/bold blue]"
    ))
    
    # 显示八字排盘
    display_chart(chart)
    
    # 显示五行分析
    display_element_analysis(result.element_strength)
    
    if detailed:
        # 显示十神分析
        display_ten_gods_analysis(result.ten_gods_analysis)
        
        # 显示特殊格局
        if result.special_patterns:
            console.print(Panel(
                "\n".join(result.special_patterns),
                title="[bold yellow]特殊格局[/bold yellow]"
            ))
        
        # 显示月令分析
        if result.monthly_analysis:
            console.print(Panel(
                result.monthly_analysis,
                title="[bold green]月令分析[/bold green]"
            ))
        
        # 显示时辰分析
        if result.time_analysis:
            console.print(Panel(
                result.time_analysis,
                title="[bold cyan]时辰分析[/bold cyan]"
            ))
    
    # 显示总体运势
    if result.general_fortune:
        console.print(Panel(
            result.general_fortune,
            title="[bold purple]总体运势[/bold purple]"
        ))
    
    # 显示建议
    if result.recommendations:
        console.print(Panel(
            "\n".join([f"• {rec}" for rec in result.recommendations]),
            title="[bold red]生活建议[/bold red]"
        ))


def display_chart(chart):
    """显示八字排盘"""
    table = Table(title="八字排盘")
    
    table.add_column("柱", style="cyan", no_wrap=True)
    table.add_column("天干", style="magenta")
    table.add_column("地支", style="green")
    table.add_column("纳音", style="yellow")
    
    for pillar in chart.all_pillars:
        gan = pillar.gan_zhi.gan.name
        zhi = pillar.gan_zhi.zhi.name
        
        # 简化的纳音计算（实际需要更复杂的算法）
        nayin = "待实现"
        
        table.add_row(
            f"{pillar.pillar_type}柱",
            gan,
            zhi,
            nayin
        )
    
    console.print(table)


def display_element_analysis(element_strength):
    """显示五行分析"""
    table = Table(title="五行力量分析")
    
    table.add_column("五行", style="cyan")
    table.add_column("力量", style="magenta")
    table.add_column("比例", style="green")
    
    total = element_strength.total
    elements = [
        ("木", element_strength.wood),
        ("火", element_strength.fire),
        ("土", element_strength.earth),
        ("金", element_strength.metal),
        ("水", element_strength.water)
    ]
    
    for name, strength in elements:
        ratio = f"{strength/total*100:.1f}%" if total > 0 else "0%"
        table.add_row(name, f"{strength:.1f}", ratio)
    
    console.print(table)


def display_ten_gods_analysis(ten_gods_analysis):
    """显示十神分析"""
    if not ten_gods_analysis:
        return
        
    table = Table(title="十神分析")
    table.add_column("位置", style="cyan")
    table.add_column("十神", style="magenta")
    
    for position, ten_god in ten_gods_analysis.items():
        table.add_row(position, ten_god)
    
    console.print(table)


@cli.command()
def help_usage():
    """显示使用帮助"""
    help_text = """
八字分析工具使用说明:

1. 基本分析:
   bazi analyze -y 1990 -m 5 -d 15 -h 14

2. 详细分析:
   bazi analyze -y 1990 -m 5 -d 15 -h 14 --detailed

3. 女性八字:
   bazi analyze -y 1990 -m 5 -d 15 -h 14 --female

参数说明:
  -y, --year     出生年份 (必需)
  -m, --month    出生月份 (必需)  
  -d, --day      出生日期 (必需)
  -h, --hour     出生小时 (可选, 默认12点)
  --minute       出生分钟 (可选, 默认0分)
  --male/--female 性别 (可选, 默认男性)
  --timezone     时区 (可选, 默认东八区)
  --detailed, -v 显示详细分析
    """
    
    console.print(Panel(help_text, title="[bold blue]使用帮助[/bold blue]"))


def main():
    """主函数"""
    cli()


if __name__ == '__main__':
    main()
