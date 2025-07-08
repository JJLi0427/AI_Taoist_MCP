"""
Data loader for BaZi analysis system
"""
import json
import os
from typing import Dict, List, Any
from pathlib import Path

from core.models import TianGan, DiZhi, WuXing, YinYang


class DataLoader:
    """数据加载器类"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # 获取项目根目录下的data文件夹
            current_dir = Path(__file__).parent.parent.parent
            self.data_dir = current_dir / "data"
        else:
            self.data_dir = Path(data_dir)
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """加载JSON文件"""
        file_path = self.data_dir / filename
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_tiangan_data(self) -> List[TianGan]:
        """加载天干数据"""
        data = self.load_json("tiangan.json")
        tiangan_list = []
        
        for gan_data in data["gan_data"]:
            tiangan = TianGan(
                name=gan_data["name"],
                index=gan_data["index"],
                wu_xing=WuXing(gan_data["wu_xing"]),
                yin_yang=YinYang(gan_data["yin_yang"]),
                temperature=gan_data["temperature"]
            )
            tiangan_list.append(tiangan)
        
        return tiangan_list
    
    def load_dizhi_data(self) -> List[DiZhi]:
        """加载地支数据"""
        data = self.load_json("dizhi.json")
        dizhi_list = []
        
        for zhi_data in data["zhi_data"]:
            dizhi = DiZhi(
                name=zhi_data["name"],
                index=zhi_data["index"],
                wu_xing=WuXing(zhi_data["wu_xing"]),
                yin_yang=YinYang(zhi_data["yin_yang"]),
                time_range=zhi_data["time_range"],
                temperature=zhi_data["temperature"],
                hidden_stems=zhi_data["hidden_stems"]
            )
            dizhi_list.append(dizhi)
        
        return dizhi_list
    
    def load_ganzhi_data(self) -> Dict[str, Any]:
        """加载干支组合数据"""
        return self.load_json("ganzhi.json")
    
    def load_ten_gods_data(self) -> Dict[str, Any]:
        """加载十神数据"""
        return self.load_json("ten_gods.json")
    
    def load_xingxiu_data(self) -> Dict[str, Any]:
        """加载星宿数据"""
        return self.load_json("xingxiu.json")
    
    def load_jianchu_data(self) -> Dict[str, Any]:
        """加载建除数据"""
        return self.load_json("jianchu.json")


# 全局数据加载器实例
data_loader = DataLoader()

# 预加载基础数据
TIANGAN_LIST = data_loader.load_tiangan_data()
DIZHI_LIST = data_loader.load_dizhi_data()
GANZHI_DATA = data_loader.load_ganzhi_data()
TEN_GODS_DATA = data_loader.load_ten_gods_data()

# 创建查找字典
TIANGAN_DICT = {gan.name: gan for gan in TIANGAN_LIST}
DIZHI_DICT = {zhi.name: zhi for zhi in DIZHI_LIST}
GANZHI_60 = GANZHI_DATA["ganzhi_60"]
