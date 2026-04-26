# 测试功能模块
import pytest
from datetime import datetime, timedelta

from modules import (
    HuangliModule, WeatherModule, LuckyColorModule, OutfitRecommendationModule
)
from framework import ModuleStatus


class TestHuangliModule:
    """黄历模块测试类"""
    
    def setup_class(cls):
        """类级别的设置：初始化模块"""
        cls.module = HuangliModule()
        cls.module.initialize()
    
    def teardown_class(cls):
        """类级别的清理：关闭模块"""
        cls.module.shutdown()
    
    def test_module_initialization(self):
        """测试模块初始化"""
        assert self.module.status == ModuleStatus.READY
    
    def test_get_huangli_basic(self):
        """测试获取基本黄历信息"""
        today = datetime.now()
        huangli_data = self.module.get_huangli(today)
        
        # 验证返回的数据结构
        assert isinstance(huangli_data, dict)
        assert '公历日期' in huangli_data
        assert '农历' in huangli_data
        assert '生肖' in huangli_data
        assert '宜' in huangli_data
        assert '忌' in huangli_data
        assert '五行' in huangli_data
    
    def test_get_huangli_consistency(self):
        """测试同一天黄历数据的一致性"""
        today = datetime.now()
        
        # 多次获取同一天的数据应该相同
        data1 = self.module.get_huangli(today)
        data2 = self.module.get_huangli(today)
        
        assert data1 == data2
    
    def test_get_huangli_different_dates(self):
        """测试不同日期的黄历数据"""
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        data_today = self.module.get_huangli(today)
        data_tomorrow = self.module.get_huangli(tomorrow)
        
        # 不同日期的数据应该不同
        assert data_today['公历日期'] != data_tomorrow['公历日期']
    
    def test_get_lucky_direction(self):
        """测试获取幸运方位"""
        today = datetime.now()
        direction = self.module.get_lucky_direction(today)
        
        # 验证返回的是字符串
        assert isinstance(direction, str)
        assert len(direction) > 0
    
    def test_get_element(self):
        """测试获取五行属性"""
        today = datetime.now()
        element = self.module.get_element(today)
        
        # 验证返回的是五行之一
        assert element in ['金', '木', '水', '火', '土']


class TestWeatherModule:
    """天气模块测试类"""
    
    def setup_class(cls):
        """类级别的设置：初始化模块"""
        cls.module = WeatherModule()
        cls.module.initialize()
    
    def teardown_class(cls):
        """类级别的清理：关闭模块"""
        cls.module.shutdown()
    
    def test_module_initialization(self):
        """测试模块初始化"""
        assert self.module.status == ModuleStatus.READY
    
    def test_get_weather_basic(self):
        """测试获取基本天气信息"""
        weather_data = self.module.get_weather('北京')
        
        # 验证返回的数据结构
        assert isinstance(weather_data, dict)
        assert '城市' in weather_data
        assert '天气' in weather_data
        assert '温度' in weather_data
        assert '最低温度值' in weather_data
        assert '最高温度值' in weather_data
        assert '湿度' in weather_data
        assert '风向' in weather_data
    
    def test_get_weather_consistency(self):
        """测试同一城市同一天天气数据的一致性"""
        # 多次获取同一城市同一天的数据应该相同
        data1 = self.module.get_weather('上海')
        data2 = self.module.get_weather('上海')
        
        assert data1 == data2
    
    def test_get_temperature_range(self):
        """测试获取温度范围"""
        low, high = self.module.get_temperature_range('广州')
        
        # 验证温度范围合理
        assert isinstance(low, int)
        assert isinstance(high, int)
        assert low <= high
    
    def test_get_weather_condition(self):
        """测试获取天气状况"""
        condition = self.module.get_weather_condition('深圳')
        
        # 验证返回的是字符串
        assert isinstance(condition, str)
        assert len(condition) > 0
    
    def test_get_supported_cities(self):
        """测试获取支持的城市列表"""
        cities = self.module.get_supported_cities()
        
        # 验证返回的是列表且不为空
        assert isinstance(cities, list)
        assert len(cities) > 0
        assert '北京' in cities
        assert '上海' in cities


class TestLuckyColorModule:
    """幸运色模块测试类"""
    
    def setup_class(cls):
        """类级别的设置：初始化模块"""
        cls.module = LuckyColorModule()
        cls.module.initialize()
        
        # 创建测试用的黄历和天气数据
        cls.huangli_data = {
            '五行': '火',
            '公历日期': '2024年04月27日',
            '宜': '出行,聚会',
            '忌': '动土'
        }
        
        cls.weather_data = {
            '天气': '晴',
            '最低温度值': 15,
            '最高温度值': 25
        }
    
    def teardown_class(cls):
        """类级别的清理：关闭模块"""
        cls.module.shutdown()
    
    def test_module_initialization(self):
        """测试模块初始化"""
        assert self.module.status == ModuleStatus.READY
    
    def test_get_lucky_colors_basic(self):
        """测试获取基本幸运色"""
        lucky_colors = self.module.get_lucky_colors(self.huangli_data)
        
        # 验证返回的是列表且不为空
        assert isinstance(lucky_colors, list)
        assert len(lucky_colors) > 0
        
        # 验证每个颜色的结构
        for color in lucky_colors:
            assert '名称' in color
            assert 'Hex' in color
            assert 'RGB' in color
            assert '寓意' in color
    
    def test_get_lucky_colors_with_weather(self):
        """测试带天气数据的幸运色推荐"""
        lucky_colors = self.module.get_lucky_colors(
            self.huangli_data, 
            self.weather_data
        )
        
        # 验证返回的列表
        assert isinstance(lucky_colors, list)
        assert len(lucky_colors) > 0
        
        # 验证包含五行来源的颜色
        has_element_color = any(
            color.get('来源') == '五行' 
            for color in lucky_colors
        )
        assert has_element_color
    
    def test_get_color_by_element(self):
        """测试根据五行获取颜色"""
        # 测试每个五行
        for element in ['金', '木', '水', '火', '土']:
            colors = self.module.get_color_by_element(element)
            
            assert isinstance(colors, list)
            assert len(colors) > 0
            
            for color in colors:
                assert '名称' in color
                assert 'Hex' in color
                assert '寓意' in color
    
    def test_get_color_combinations(self):
        """测试获取颜色搭配方案"""
        primary_color = {
            '名称': '红色',
            'Hex': 'FF0000',
            'RGB': (255, 0, 0),
            '寓意': '热情、活力'
        }
        
        combinations = self.module.get_color_combinations(primary_color, count=3)
        
        # 验证返回的是列表
        assert isinstance(combinations, list)
        
        # 每个搭配方案应该包含主色调
        for combo in combinations:
            assert any(
                color.get('名称') == '红色' 
                for color in combo
            )


class TestOutfitRecommendationModule:
    """穿搭推荐模块测试类"""
    
    def setup_class(cls):
        """类级别的设置：初始化模块"""
        cls.module = OutfitRecommendationModule()
        cls.module.initialize()
        
        # 创建测试用数据
        cls.huangli_data = {
            '五行': '火',
            '公历日期': '2024年04月27日',
            '宜': '出行,聚会,宴会',
            '忌': '动土'
        }
        
        cls.weather_data = {
            '天气': '晴',
            '最低温度值': 18,
            '最高温度值': 26,
            '湿度': '50%'
        }
        
        cls.lucky_colors = [
            {
                '名称': '红色',
                'Hex': 'FF0000',
                'RGB': (255, 0, 0),
                '寓意': '热情、活力',
                '来源': '五行'
            },
            {
                '名称': '橙色',
                'Hex': 'FFA500',
                'RGB': (255, 165, 0),
                '寓意': '温暖、快乐',
                '来源': '五行'
            }
        ]
    
    def teardown_class(cls):
        """类级别的清理：关闭模块"""
        cls.module.shutdown()
    
    def test_module_initialization(self):
        """测试模块初始化"""
        assert self.module.status == ModuleStatus.READY
    
    def test_get_recommendations_basic(self):
        """测试获取基本穿搭推荐"""
        recommendations = self.module.get_recommendations(
            self.huangli_data,
            self.weather_data,
            self.lucky_colors
        )
        
        # 验证返回的是列表且不为空
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # 验证每个推荐的结构
        for recommendation in recommendations:
            assert '风格' in recommendation
            assert '主色' in recommendation
            assert '配色' in recommendation
            assert '服装单品' in recommendation
            assert '适合场合' in recommendation
            assert '穿搭建议' in recommendation
            assert '推荐指数' in recommendation
    
    def test_get_recommendations_with_preferences(self):
        """测试带用户偏好的穿搭推荐"""
        user_preferences = {
            '风格': ['商务休闲', '休闲日常'],
            '场合': ['日常办公']
        }
        
        recommendations = self.module.get_recommendations(
            self.huangli_data,
            self.weather_data,
            self.lucky_colors,
            user_preferences
        )
        
        # 验证返回的列表
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
    
    def test_get_style_suggestions(self):
        """测试获取风格建议"""
        styles = self.module.get_style_suggestions(
            weather_condition='晴',
            temperature_range=(18, 26)
        )
        
        # 验证返回的是列表
        assert isinstance(styles, list)
    
    def test_get_occasion_recommendations(self):
        """测试根据场合获取穿搭推荐"""
        recommendation = self.module.get_occasion_recommendations(
            occasion='商务会议',
            lucky_colors=self.lucky_colors
        )
        
        # 验证返回的是字典
        assert isinstance(recommendation, dict)
        assert '风格' in recommendation
        assert '场合' in recommendation
        assert '主色' in recommendation
    
    def test_recommendation_score_range(self):
        """测试推荐指数范围"""
        recommendations = self.module.get_recommendations(
            self.huangli_data,
            self.weather_data,
            self.lucky_colors
        )
        
        # 验证推荐指数在0-1之间
        for recommendation in recommendations:
            score = recommendation.get('推荐指数', 0)
            assert 0 <= score <= 1


class TestIntegration:
    """集成测试类"""
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        # 初始化所有模块
        huangli_module = HuangliModule()
        weather_module = WeatherModule()
        lucky_color_module = LuckyColorModule()
        outfit_module = OutfitRecommendationModule()
        
        huangli_module.initialize()
        weather_module.initialize()
        lucky_color_module.initialize()
        outfit_module.initialize()
        
        try:
            # 1. 获取黄历
            today = datetime.now()
            huangli_data = huangli_module.get_huangli(today)
            assert huangli_data is not None
            assert '五行' in huangli_data
            
            # 2. 获取天气
            weather_data = weather_module.get_weather('北京')
            assert weather_data is not None
            assert '天气' in weather_data
            
            # 3. 获取幸运色
            lucky_colors = lucky_color_module.get_lucky_colors(
                huangli_data, weather_data
            )
            assert lucky_colors is not None
            assert len(lucky_colors) > 0
            
            # 4. 获取穿搭推荐
            outfit_recommendations = outfit_module.get_recommendations(
                huangli_data, weather_data, lucky_colors
            )
            assert outfit_recommendations is not None
            assert len(outfit_recommendations) > 0
            
        finally:
            # 关闭所有模块
            huangli_module.shutdown()
            weather_module.shutdown()
            lucky_color_module.shutdown()
            outfit_module.shutdown()
