# 天气模块
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import random

from framework import BaseModule, ModuleStatus, PerformanceMonitor, ErrorHandler, ModuleException
from framework import IWeatherModule


class WeatherModule(BaseModule, IWeatherModule):
    """天气模块
    
    提供天气信息查询功能
    """
    
    # 支持的城市列表
    SUPPORTED_CITIES = [
        '北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '武汉',
        '西安', '重庆', '天津', '苏州', '长沙', '郑州', '东莞', '青岛',
        '沈阳', '宁波', '昆明', '大连', '厦门', '济南', '哈尔滨', '福州'
    ]
    
    # 天气状况列表
    WEATHER_CONDITIONS = [
        '晴', '多云', '阴', '小雨', '中雨', '大雨', '阵雨', '雷阵雨',
        '小雪', '中雪', '大雪', '雨夹雪', '雾', '霾', '沙尘暴'
    ]
    
    # 风向列表
    WIND_DIRECTIONS = [
        '北风', '东北风', '东风', '东南风', '南风', '西南风', '西风', '西北风'
    ]
    
    # 风力等级
    WIND_FORCES = ['1级', '2级', '3级', '4级', '5级', '6级']
    
    # 紫外线强度
    UV_INTENSITIES = ['弱', '中等', '强', '很强', '极强']
    
    def __init__(self):
        """初始化天气模块"""
        super().__init__("WeatherModule")
        self._weather_cache = {}
        self._cache_expire = timedelta(hours=1)
    
    def _on_initialize(self) -> bool:
        """执行具体初始化逻辑"""
        self.logger.info("天气模块初始化完成")
        return True
    
    def _on_shutdown(self) -> bool:
        """执行具体关闭逻辑"""
        self._weather_cache.clear()
        self.logger.info("天气模块已关闭")
        return True
    
    def get_weather(self, city: str, date: datetime = None) -> Dict[str, Any]:
        """获取指定城市的天气信息
        
        Args:
            city: 城市名称
            date: 日期对象，默认为今天
            
        Returns:
            包含天气信息的字典
        """
        start_time = datetime.now().timestamp()
        success = True
        
        try:
            self.check_ready()
            
            # 验证城市
            if city not in self.SUPPORTED_CITIES:
                raise ModuleException(
                    self.module_name,
                    f"不支持的城市: {city}",
                    "UNSUPPORTED_CITY"
                )
            
            # 默认使用今天
            if date is None:
                date = datetime.now()
            
            # 检查缓存
            cache_key = f"{city}_{date.strftime('%Y-%m-%d')}"
            if cache_key in self._weather_cache:
                cached_data, cached_time = self._weather_cache[cache_key]
                if datetime.now() - cached_time < self._cache_expire:
                    self.logger.debug(f"从缓存获取天气数据: {city} {date.strftime('%Y-%m-%d')}")
                    return cached_data
            
            # 模拟生成天气数据
            weather_data = self._generate_weather_data(city, date)
            
            # 缓存结果
            self._weather_cache[cache_key] = (weather_data, datetime.now())
            
            self.logger.info(f"成功获取天气数据: {city} {date.strftime('%Y-%m-%d')}")
            return weather_data
            
        except Exception as e:
            success = False
            ErrorHandler.handle_exception(e, f"获取{city}天气数据", self.module_name)
            if isinstance(e, ModuleException):
                raise
            raise ModuleException(
                self.module_name,
                f"获取天气数据失败: {str(e)}",
                "WEATHER_FETCH_ERROR"
            )
        finally:
            end_time = datetime.now().timestamp()
            self._update_metrics(success, end_time - start_time)
    
    def _generate_weather_data(self, city: str, date: datetime) -> Dict[str, Any]:
        """生成模拟天气数据
        
        Args:
            city: 城市名称
            date: 日期对象
            
        Returns:
            天气信息字典
        """
        # 使用日期和城市作为随机种子，确保同一天同一城市天气相同
        seed = hash(f"{city}_{date.strftime('%Y-%m-%d')}")
        random.seed(seed)
        
        # 确定季节影响温度
        month = date.month
        if month in [12, 1, 2]:  # 冬季
            base_temp = random.randint(-5, 10)
        elif month in [3, 4, 5]:  # 春季
            base_temp = random.randint(10, 25)
        elif month in [6, 7, 8]:  # 夏季
            base_temp = random.randint(25, 38)
        else:  # 秋季
            base_temp = random.randint(10, 25)
        
        # 随机调整
        high_temp = base_temp + random.randint(0, 8)
        low_temp = base_temp - random.randint(3, 10)
        
        # 随机选择天气状况
        if high_temp > 30:
            # 夏天更容易晴天
            weather_choices = ['晴', '多云', '阴', '雷阵雨']
        elif low_temp < 0:
            # 冬天可能下雪
            weather_choices = ['晴', '多云', '阴', '小雪', '中雪']
        else:
            weather_choices = ['晴', '多云', '阴', '小雨', '阵雨']
        
        weather_condition = random.choice(weather_choices)
        
        # 随机选择风向和风力
        wind_direction = random.choice(self.WIND_DIRECTIONS)
        wind_force = random.choice(self.WIND_FORCES)
        
        # 计算湿度
        if '雨' in weather_condition or '雪' in weather_condition:
            humidity = random.randint(70, 95)
        else:
            humidity = random.randint(30, 65)
        
        # 计算紫外线强度
        if weather_condition == '晴' and high_temp > 25:
            uv_intensity = random.choice(['强', '很强', '极强'])
        elif weather_condition in ['多云', '阴']:
            uv_intensity = random.choice(['弱', '中等'])
        else:
            uv_intensity = '弱'
        
        return {
            '城市': city,
            '日期': date.strftime('%Y年%m月%d日'),
            '星期': self._get_weekday_name(date.weekday()),
            '天气': weather_condition,
            '温度': f"{low_temp}°C ~ {high_temp}°C",
            '最低温度': f"{low_temp}°C",
            '最高温度': f"{high_temp}°C",
            '最低温度值': low_temp,
            '最高温度值': high_temp,
            '湿度': f"{humidity}%",
            '风向': wind_direction,
            '风力': wind_force,
            '紫外线强度': uv_intensity,
            '天气描述': self._get_weather_description(weather_condition)
        }
    
    def _get_weekday_name(self, weekday: int) -> str:
        """获取星期名称"""
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        return weekdays[weekday]
    
    def _get_weather_description(self, weather: str) -> str:
        """获取天气描述"""
        descriptions = {
            '晴': '阳光明媚，适合户外活动',
            '多云': '云层较厚，但仍有阳光',
            '阴': '阴天，可能有小雨',
            '小雨': '有小雨，外出请带伞',
            '中雨': '雨量中等，注意出行安全',
            '大雨': '雨量较大，尽量减少外出',
            '阵雨': '间歇性降雨，时晴时雨',
            '雷阵雨': '伴有雷电的阵雨，注意避雷',
            '小雪': '有小雪，注意保暖',
            '中雪': '有中雪，道路可能结冰',
            '大雪': '有大雪，出行请注意安全',
            '雨夹雪': '雨夹雪天气，注意保暖防滑',
            '雾': '有雾，能见度低，注意交通安全',
            '霾': '有霾，空气质量较差，尽量减少户外活动',
            '沙尘暴': '有沙尘暴，尽量不要外出'
        }
        return descriptions.get(weather, '天气状况一般')
    
    def get_temperature_range(self, city: str, date: datetime = None) -> tuple:
        """获取指定城市的温度范围
        
        Args:
            city: 城市名称
            date: 日期对象，默认为今天
            
        Returns:
            (最低温度, 最高温度) 元组
        """
        weather_data = self.get_weather(city, date)
        return (weather_data.get('最低温度值', 0), weather_data.get('最高温度值', 0))
    
    def get_weather_condition(self, city: str, date: datetime = None) -> str:
        """获取指定城市的天气状况
        
        Args:
            city: 城市名称
            date: 日期对象，默认为今天
            
        Returns:
            天气状况字符串
        """
        weather_data = self.get_weather(city, date)
        return weather_data.get('天气', '未知')
    
    def get_supported_cities(self) -> List[str]:
        """获取支持的城市列表
        
        Returns:
            支持的城市名称列表
        """
        return self.SUPPORTED_CITIES.copy()
