# 模块接口定义
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional


class IModule(ABC):
    """模块基础接口
    
    所有模块都必须实现的基本方法
    """
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any] = None) -> bool:
        """初始化模块"""
        pass
    
    @abstractmethod
    def shutdown(self) -> bool:
        """关闭模块"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """获取模块状态"""
        pass


class IHuangliModule(IModule):
    """黄历模块接口"""
    
    @abstractmethod
    def get_huangli(self, date: datetime) -> Dict[str, Any]:
        """获取指定日期的黄历信息
        
        Args:
            date: 日期对象
            
        Returns:
            包含黄历信息的字典，例如：
            {
                '农历': '三月十八',
                '生肖': '龙',
                '宜': '嫁娶,祭祀,出行',
                '忌': '动土,安葬',
                '冲煞': '冲狗煞南',
                '五行': '土',
                '方位': '西南'
            }
        """
        pass
    
    @abstractmethod
    def get_lucky_direction(self, date: datetime) -> str:
        """获取指定日期的幸运方位
        
        Args:
            date: 日期对象
            
        Returns:
            幸运方位字符串，如"西南"
        """
        pass
    
    @abstractmethod
    def get_element(self, date: datetime) -> str:
        """获取指定日期的五行属性
        
        Args:
            date: 日期对象
            
        Returns:
            五行属性字符串，如"土"
        """
        pass


class IWeatherModule(IModule):
    """天气模块接口"""
    
    @abstractmethod
    def get_weather(self, city: str, date: datetime = None) -> Dict[str, Any]:
        """获取指定城市的天气信息
        
        Args:
            city: 城市名称
            date: 日期对象，默认为今天
            
        Returns:
            包含天气信息的字典，例如：
            {
                '城市': '北京',
                '日期': '2024-04-27',
                '天气': '晴',
                '温度': '15°C',
                '最高温度': '22°C',
                '最低温度': '8°C',
                '湿度': '45%',
                '风向': '东北风',
                '风力': '3级',
                '紫外线强度': '中等'
            }
        """
        pass
    
    @abstractmethod
    def get_temperature_range(self, city: str, date: datetime = None) -> tuple:
        """获取指定城市的温度范围
        
        Args:
            city: 城市名称
            date: 日期对象，默认为今天
            
        Returns:
            (最低温度, 最高温度) 元组
        """
        pass
    
    @abstractmethod
    def get_weather_condition(self, city: str, date: datetime = None) -> str:
        """获取指定城市的天气状况
        
        Args:
            city: 城市名称
            date: 日期对象，默认为今天
            
        Returns:
            天气状况字符串，如"晴"、"多云"、"小雨"等
        """
        pass
    
    @abstractmethod
    def get_supported_cities(self) -> List[str]:
        """获取支持的城市列表
        
        Returns:
            支持的城市名称列表
        """
        pass


class ILuckyColorModule(IModule):
    """幸运色模块接口"""
    
    @abstractmethod
    def get_lucky_colors(self, huangli_data: Dict[str, Any], 
                        weather_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """根据黄历和天气信息获取幸运色推荐
        
        Args:
            huangli_data: 黄历数据字典
            weather_data: 天气数据字典（可选）
            
        Returns:
            幸运色列表，每个颜色包含名称、Hex值和寓意，例如：
            [
                {
                    '名称': '红色',
                    'Hex': 'FF0000',
                    'RGB': (255, 0, 0),
                    '寓意': '吉祥、喜庆、活力',
                    '匹配度': 0.95
                }
            ]
        """
        pass
    
    @abstractmethod
    def get_color_by_element(self, element: str) -> Dict[str, Any]:
        """根据五行属性获取对应的幸运色
        
        Args:
            element: 五行属性（金、木、水、火、土）
            
        Returns:
            颜色信息字典
        """
        pass
    
    @abstractmethod
    def get_color_combinations(self, primary_color: Dict[str, Any],
                               count: int = 3) -> List[List[Dict[str, Any]]]:
        """获取颜色搭配方案
        
        Args:
            primary_color: 主色调
            count: 搭配方案数量
            
        Returns:
            颜色搭配方案列表，每个方案包含多个颜色
        """
        pass


class IOutfitRecommendationModule(IModule):
    """穿搭推荐模块接口"""
    
    @abstractmethod
    def get_recommendations(self, huangli_data: Dict[str, Any],
                           weather_data: Dict[str, Any],
                           lucky_colors: List[Dict[str, Any]],
                           user_preferences: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """获取穿搭推荐
        
        Args:
            huangli_data: 黄历数据
            weather_data: 天气数据
            lucky_colors: 幸运色列表
            user_preferences: 用户偏好（可选）
            
        Returns:
            穿搭推荐列表，例如：
            [
                {
                    '风格': '商务休闲',
                    '主色': {'名称': '深蓝色', 'Hex': '00008B'},
                    '配色': [
                        {'名称': '白色', 'Hex': 'FFFFFF'},
                        {'名称': '浅灰色', 'Hex': 'D3D3D3'}
                    ],
                    '适合场合': '办公室、会议',
                    '穿搭建议': '深蓝色西装外套搭配白色衬衫，灰色西裤',
                    '推荐指数': 0.92
                }
            ]
        """
        pass
    
    @abstractmethod
    def get_style_suggestions(self, weather_condition: str,
                             temperature_range: tuple) -> List[str]:
        """根据天气获取风格建议
        
        Args:
            weather_condition: 天气状况
            temperature_range: 温度范围(最低, 最高)
            
        Returns:
            适合的风格列表
        """
        pass
    
    @abstractmethod
    def get_occasion_recommendations(self, occasion: str,
                                     lucky_colors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """根据场合获取穿搭推荐
        
        Args:
            occasion: 场合名称
            lucky_colors: 幸运色列表
            
        Returns:
            穿搭推荐字典
        """
        pass
