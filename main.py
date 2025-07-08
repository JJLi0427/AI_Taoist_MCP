"""
BaZi Analyzer - Modern Chinese Eight Characters Fortune Telling Tool
"""
import sys
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.cli import main

if __name__ == "__main__":
    main()
