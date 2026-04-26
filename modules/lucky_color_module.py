# 幸运色模块
from datetime import datetime
from typing import Dict, Any, List, Optional
import random

from framework import BaseModule, ModuleStatus, PerformanceMonitor, ErrorHandler, ModuleException
from framework import ILuckyColorModule


class LuckyColorModule(BaseModule, ILuckyColorModule):
    """幸运色模块
    
    提供幸运色推荐功能
    """
    
    # 五行对应颜色
    ELEMENT_COLORS = {
        '金': [
            {'名称': '白色', 'Hex': 'FFFFFF', 'RGB': (255, 255, 255), '寓意': '纯洁、高贵、清新'},
            {'名称': '金色', 'Hex': 'FFD700', 'RGB': (255, 215, 0), '寓意': '财富、尊贵、荣耀'},
            {'名称': '银色', 'Hex': 'C0C0C0', 'RGB': (192, 192, 192), '寓意': '优雅、冷静、稳重'}
        ],
        '木': [
            {'名称': '绿色', 'Hex': '008000', 'RGB': (0, 128, 0), '寓意': '生机、希望、自然'},
            {'名称': '青色', 'Hex': '00FFFF', 'RGB': (0, 255, 255), '寓意': '清新、活力、希望'},
            {'名称': '翠绿色', 'Hex': '00A86B', 'RGB': (0, 168, 107), '寓意': '生命力、成长、繁荣'}
        ],
        '水': [
            {'名称': '黑色', 'Hex': '000000', 'RGB': (0, 0, 0), '寓意': '神秘、稳重、力量'},
            {'名称': '蓝色', 'Hex': '0000FF', 'RGB': (0, 0, 255), '寓意': '智慧、冷静、信任'},
            {'名称': '深蓝色', 'Hex': '00008B', 'RGB': (0, 0, 139), '寓意': '专业、稳重、可靠'}
        ],
        '火': [
            {'名称': '红色', 'Hex': 'FF0000', 'RGB': (255, 0, 0), '寓意': '热情、活力、吉祥'},
            {'名称': '橙色', 'Hex': 'FFA500', 'RGB': (255, 165, 0), '寓意': '温暖、快乐、创意'},
            {'名称': '紫色', 'Hex': '800080', 'RGB': (128, 0, 128), '寓意': '高贵、神秘、优雅'}
        ],
        '土': [
            {'名称': '黄色', 'Hex': 'FFFF00', 'RGB': (255, 255, 0), '寓意': '温暖、阳光、快乐'},
            {'名称': '棕色', 'Hex': 'A52A2A', 'RGB': (165, 42, 42), '寓意': '稳重、踏实、可靠'},
            {'名称': '土黄色', 'Hex': 'E6C88B', 'RGB': (230, 200, 139), '寓意': '温暖、亲和、自然'}
        ]
    }
    
    # 天气对应颜色
    WEATHER_COLORS = {
        '晴': [
            {'名称': '天蓝色', 'Hex': '87CEEB', 'RGB': (135, 206, 235), '寓意': '清新、开阔'},
            {'名称': '淡黄色', 'Hex': 'FFFFE0', 'RGB': (255, 255, 224), '寓意': '温暖、明亮'}
        ],
        '多云': [
            {'名称': '浅灰色', 'Hex': 'D3D3D3', 'RGB': (211, 211, 211), '寓意': '柔和、平静'},
            {'名称': '淡蓝色', 'Hex': 'ADD8E6', 'RGB': (173, 216, 230), '寓意': '清新、舒适'}
        ],
        '阴': [
            {'名称': '深灰色', 'Hex': '808080', 'RGB': (128, 128, 128), '寓意': '稳重、内敛'},
            {'名称': '米白色', 'Hex': 'F5F5DC', 'RGB': (245, 245, 220), '寓意': '柔和、温暖'}
        ],
        '雨': [
            {'名称': '深蓝色', 'Hex': '00008B', 'RGB': (0, 0, 139), '寓意': '专业、稳重'},
            {'名称': '黑色', 'Hex': '000000', 'RGB': (0, 0, 0), '寓意': '神秘、稳重'}
        ],
        '雪': [
            {'名称': '白色', 'Hex': 'FFFFFF', 'RGB': (255, 255, 255), '寓意': '纯洁、高贵'},
            {'名称': '浅蓝色', 'Hex': 'E0F7FA', 'RGB': (224, 247, 250), '寓意': '清新、凉爽'}
        ]
    }
    
    # 季节对应颜色
    SEASON_COLORS = {
        '春季': [
            {'名称': '粉红色', 'Hex': 'FFC0CB', 'RGB': (255, 192, 203), '寓意': '浪漫、温柔'},
            {'名称': '嫩绿色', 'Hex': '90EE90', 'RGB': (144, 238, 144), '寓意': '生机、活力'},
            {'名称': '鹅黄色', 'Hex': 'FFFACD', 'RGB': (255, 250, 205), '寓意': '温暖、希望'}
        ],
        '夏季': [
            {'名称': '天蓝色', 'Hex': '87CEEB', 'RGB': (135, 206, 235), '寓意': '清新、凉爽'},
            {'名称': '白色', 'Hex': 'FFFFFF', 'RGB': (255, 255, 255), '寓意': '纯洁、清爽'},
            {'名称': '浅绿色', 'Hex': '98FB98', 'RGB': (152, 251, 152), '寓意': '清新、自然'}
        ],
        '秋季': [
            {'名称': '橙色', 'Hex': 'FFA500', 'RGB': (255, 165, 0), '寓意': '温暖、丰收'},
            {'名称': '棕色', 'Hex': 'A52A2A', 'RGB': (165, 42, 42), '寓意': '稳重、成熟'},
            {'名称': '卡其色', 'Hex': 'C3B091', 'RGB': (195, 176, 145), '寓意': '自然、优雅'}
        ],
        '冬季': [
            {'名称': '黑色', 'Hex': '000000', 'RGB': (0, 0, 0), '寓意': '稳重、神秘'},
            {'名称': '深灰色', 'Hex': '696969', 'RGB': (105, 105, 105), '寓意': '内敛、稳重'},
            {'名称': '酒红色', 'Hex': '8B0000', 'RGB': (139, 0, 0), '寓意': '高贵、热情'}
        ]
    }
    
    def __init__(self):
        """初始化幸运色模块"""
        super().__init__("LuckyColorModule")
    
    def _on_initialize(self) -> bool:
        """执行具体初始化逻辑"""
        self.logger.info("幸运色模块初始化完成")
        return True
    
    def _on_shutdown(self) -> bool:
        """执行具体关闭逻辑"""
        self.logger.info("幸运色模块已关闭")
        return True
    
    def get_lucky_colors(self, huangli_data: Dict[str, Any], 
                        weather_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """根据黄历和天气信息获取幸运色推荐
        
        Args:
            huangli_data: 黄历数据字典
            weather_data: 天气数据字典（可选）
            
        Returns:
            幸运色列表
        """
        start_time = datetime.now().timestamp()
        success = True
        
        try:
            self.check_ready()
            
            lucky_colors = []
            
            # 1. 基于五行的幸运色
            element = huangli_data.get('五行', '土')
            element_colors = self.get_color_by_element(element)
            if element_colors:
                for color in element_colors:
                    color_copy = color.copy()
                    color_copy['来源'] = '五行'
                    color_copy['匹配度'] = 0.9
                    lucky_colors.append(color_copy)
            
            # 2. 基于天气的颜色（如果有天气数据）
            if weather_data:
                weather_colors = self._get_colors_by_weather(weather_data)
                for color in weather_colors:
                    color_copy = color.copy()
                    color_copy['来源'] = '天气'
                    color_copy['匹配度'] = 0.7
                    lucky_colors.append(color_copy)
            
            # 3. 基于季节的颜色
            season_colors = self._get_colors_by_season(huangli_data.get('公历日期', ''))
            for color in season_colors:
                color_copy = color.copy()
                color_copy['来源'] = '季节'
                color_copy['匹配度'] = 0.6
                lucky_colors.append(color_copy)
            
            # 去重（基于颜色名称）
            seen_names = set()
            unique_colors = []
            for color in lucky_colors:
                name = color.get('名称', '')
                if name not in seen_names:
                    seen_names.add(name)
                    unique_colors.append(color)
            
            # 按匹配度排序
            unique_colors.sort(key=lambda x: x.get('匹配度', 0), reverse=True)
            
            self.logger.info(f"成功生成幸运色推荐: {len(unique_colors)} 种颜色")
            return unique_colors
            
        except Exception as e:
            success = False
            ErrorHandler.handle_exception(e, "获取幸运色推荐", self.module_name)
            raise ModuleException(
                self.module_name,
                f"获取幸运色推荐失败: {str(e)}",
                "LUCKY_COLOR_ERROR"
            )
        finally:
            end_time = datetime.now().timestamp()
            self._update_metrics(success, end_time - start_time)
    
    def get_color_by_element(self, element: str) -> List[Dict[str, Any]]:
        """根据五行属性获取对应的幸运色
        
        Args:
            element: 五行属性（金、木、水、火、土）
            
        Returns:
            颜色信息列表
        """
        return self.ELEMENT_COLORS.get(element, self.ELEMENT_COLORS['土'])
    
    def _get_colors_by_weather(self, weather_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """根据天气获取颜色推荐
        
        Args:
            weather_data: 天气数据字典
            
        Returns:
            颜色信息列表
        """
        weather_condition = weather_data.get('天气', '晴')
        
        # 根据天气关键词匹配
        for key, colors in self.WEATHER_COLORS.items():
            if key in weather_condition:
                return colors
        
        return self.WEATHER_COLORS['晴']
    
    def _get_colors_by_season(self, date_str: str) -> List[Dict[str, Any]]:
        """根据日期获取季节颜色
        
        Args:
            date_str: 日期字符串，格式为"YYYY年MM月DD日"
            
        Returns:
            颜色信息列表
        """
        try:
            # 解析月份
            month_part = date_str.split('年')[1].split('月')[0]
            month = int(month_part)
            
            if month in [3, 4, 5]:
                return self.SEASON_COLORS['春季']
            elif month in [6, 7, 8]:
                return self.SEASON_COLORS['夏季']
            elif month in [9, 10, 11]:
                return self.SEASON_COLORS['秋季']
            else:
                return self.SEASON_COLORS['冬季']
        except:
            # 解析失败，返回默认
            return self.SEASON_COLORS['春季']
    
    def get_color_combinations(self, primary_color: Dict[str, Any],
                               count: int = 3) -> List[List[Dict[str, Any]]]:
        """获取颜色搭配方案
        
        Args:
            primary_color: 主色调
            count: 搭配方案数量
            
        Returns:
            颜色搭配方案列表，每个方案包含多个颜色
        """
        # 基础配色规则
        # 1. 同色系搭配：相近色调
        # 2. 对比色搭配：互补色调
        # 3. 中性色搭配：黑白灰
        
        combinations = []
        
        # 获取所有可用颜色
        all_colors = []
        for colors in self.ELEMENT_COLORS.values():
            all_colors.extend(colors)
        for colors in self.SEASON_COLORS.values():
            all_colors.extend(colors)
        
        # 去重
        seen = set()
        unique_colors = []
        for color in all_colors:
            name = color.get('名称', '')
            if name not in seen and name != primary_color.get('名称', ''):
                seen.add(name)
                unique_colors.append(color)
        
        # 生成搭配方案
        for i in range(min(count, len(unique_colors) // 2)):
            # 随机选择2-3种配色
            combo = [primary_color]
            combo.extend(random.sample(unique_colors, min(2, len(unique_colors))))
            combinations.append(combo)
        
        return combinations
