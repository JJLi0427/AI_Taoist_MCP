# 八字分析器 (BaZi Analyzer)

现代化的中国传统八字命理分析工具，采用Python开发，具有清晰的代码结构和现代化的数据管理方式。

## 项目特点

- 🏗️ **现代化架构**: 采用分层架构设计，代码结构清晰
- 📊 **结构化数据**: 使用JSON格式存储命理数据，便于维护和扩展
- 🎨 **美观界面**: 基于Rich库的彩色命令行界面
- 🔧 **类型安全**: 使用Pydantic进行数据验证和类型检查
- 📦 **标准打包**: 遵循现代Python包管理规范
- 🧪 **测试覆盖**: 包含完整的单元测试

## 功能特性

### 核心功能
- 八字排盘：根据出生时间自动计算四柱八字
- 五行分析：计算各五行力量分布和平衡情况
- 十神分析：分析各柱位的十神关系
- 格局识别：识别特殊命理格局
- 月令分析：基于《三命通会》的月令用神分析
- 时辰分析：详细的日时组合分析

### 数据管理
- JSON格式的结构化数据存储
- 分类管理：天干、地支、十神、月令、时辰等数据独立管理
- 易于扩展：可方便添加新的命理数据和分析规则

## 项目结构

```
bazi/
├── src/                    # 源代码目录
│   ├── core/              # 核心模块
│   │   ├── models.py      # 数据模型定义
│   │   └── calculator.py  # 八字计算引擎
│   ├── data/              # 数据加载模块
│   │   └── loader.py      # 数据加载器
│   ├── analysis/          # 分析模块
│   │   └── analyzer.py    # 分析引擎
│   ├── utils/             # 工具模块
│   │   └── helpers.py     # 辅助工具
│   └── cli.py             # 命令行接口
├── data/                  # 数据文件目录
│   ├── tiangan.json       # 天干数据
│   ├── dizhi.json         # 地支数据
│   ├── ganzhi.json        # 干支组合数据
│   ├── ten_gods.json      # 十神关系数据
│   ├── monthly_analysis.json  # 月令分析数据
│   ├── time_analysis.json     # 时辰分析数据
│   ├── xingxiu.json       # 星宿数据
│   └── jianchu.json       # 建除数据
├── tests/                 # 测试文件
└── docs/                  # 文档目录
```

## 安装方式

### 环境要求
- Python 3.8+
- pip 包管理器

### 安装依赖
```bash
# 克隆项目
git clone <repository-url>
cd bazi

# 安装依赖
pip install -r requirements.txt

# 或者使用开发环境安装
pip install -e .[dev]
```

### 依赖包说明
- `bidict`: 双向字典，用于干支映射
- `lunar-python`: 农历转换库
- `colorama`: 终端颜色支持
- `pydantic`: 数据验证和类型检查
- `click`: 命令行框架
- `rich`: 美化终端输出

## 使用方法

### 命令行使用

```bash
# 基本八字分析
python main.py analyze -y 1990 -m 5 -d 15 -h 14

# 详细分析（包含月令、时辰分析）
python main.py analyze -y 1990 -m 5 -d 15 -h 14 --detailed

# 女性八字分析
python main.py analyze -y 1990 -m 5 -d 15 -h 14 --female

# 显示帮助
python main.py help-usage
```

### 参数说明
- `-y, --year`: 出生年份（必需）
- `-m, --month`: 出生月份（必需）
- `-d, --day`: 出生日期（必需）
- `-h, --hour`: 出生小时（可选，默认12点）
- `--minute`: 出生分钟（可选，默认0分）
- `--male/--female`: 性别（可选，默认男性）
- `--timezone`: 时区偏移（可选，默认东八区）
- `--detailed, -v`: 显示详细分析

### 编程接口使用

```python
from datetime import datetime
from src.core.calculator import BaZiCalculator
from src.analysis.analyzer import BaZiAnalyzer

# 创建计算器和分析器
calculator = BaZiCalculator()
analyzer = BaZiAnalyzer()

# 计算八字
birth_time = datetime(1990, 5, 15, 14, 30)
chart = calculator.calculate_bazi_from_datetime(birth_time)

# 分析命盘
result = analyzer.analyze_chart(chart)

# 查看结果
print("八字:", [p.gan_zhi.name for p in chart.all_pillars])
print("五行分析:", result.element_strength)
print("总体运势:", result.general_fortune)
```

## 数据说明

### 命理数据来源
本项目的命理数据主要来源于：
- 《三命通会》- 明代万民英著，中国古代命理学经典
- 《千里命稿》- 现代命理学重要参考
- 《穷通宝鉴》- 月令用神分析的权威典籍

### 数据格式
所有命理数据均采用JSON格式存储，具有以下优点：
- 结构清晰，便于理解和维护
- 支持中文字符，保持传统命理术语
- 易于扩展，可方便添加新的分析维度
- 版本控制友好，便于跟踪数据变更

## 开发指南

### 添加新的命理数据
1. 在`data/`目录下创建相应的JSON文件
2. 在`src/data/loader.py`中添加加载方法
3. 在分析器中集成新的数据和分析逻辑

### 扩展分析功能
1. 在`src/analysis/analyzer.py`中添加新的分析方法
2. 更新`AnalysisResult`模型以包含新的分析结果
3. 在CLI中添加相应的显示逻辑

### 运行测试
```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行测试
pytest tests/

# 生成覆盖率报告
pytest --cov=src tests/
```

## 免责声明

本工具仅供娱乐和学术研究使用，不应作为人生重大决策的唯一依据。命理学属于传统文化范畴，其准确性和科学性存在争议，请理性对待分析结果。

## 联系方式

- 提交Issue: [GitHub Issues](项目GitHub地址/issues)
- 邮箱: your.email@example.com

---

*传承千年智慧，拥抱现代技术*
