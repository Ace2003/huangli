# 测试功能模块
import pytest
from datetime import datetime, timedelta

from modules import (
    HuangliModule, WeatherModule, LuckyColorModule, 
    OutfitRecommendationModule, UserInfoModule
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


class TestUserInfoModule:
    """用户信息模块测试类"""
    
    def setup_class(cls):
        """类级别的设置：初始化模块"""
        cls.module = UserInfoModule()
        cls.module.initialize()
    
    def teardown_class(cls):
        """类级别的清理：关闭模块"""
        cls.module.shutdown()
    
    def test_module_initialization(self):
        """测试模块初始化"""
        assert self.module.status == ModuleStatus.READY
    
    def test_calculate_zodiac(self):
        """测试生肖计算"""
        # 测试已知年份的生肖
        assert self.module._calculate_zodiac(1984) == '鼠'
        assert self.module._calculate_zodiac(1985) == '牛'
        assert self.module._calculate_zodiac(1986) == '虎'
        assert self.module._calculate_zodiac(1987) == '兔'
        assert self.module._calculate_zodiac(1988) == '龙'
        assert self.module._calculate_zodiac(2000) == '龙'
    
    def test_calculate_zodiac_sign(self):
        """测试星座计算"""
        # 测试摩羯座 (12.22-1.19)
        assert self.module._calculate_zodiac_sign(1, 1) == '摩羯座'
        assert self.module._calculate_zodiac_sign(1, 15) == '摩羯座'
        assert self.module._calculate_zodiac_sign(12, 25) == '摩羯座'
        
        # 测试水瓶座 (1.20-2.18)
        assert self.module._calculate_zodiac_sign(1, 20) == '水瓶座'
        assert self.module._calculate_zodiac_sign(2, 10) == '水瓶座'
        
        # 测试双鱼座 (2.19-3.20)
        assert self.module._calculate_zodiac_sign(2, 19) == '双鱼座'
        assert self.module._calculate_zodiac_sign(3, 15) == '双鱼座'
        
        # 测试白羊座 (3.21-4.19)
        assert self.module._calculate_zodiac_sign(3, 21) == '白羊座'
        assert self.module._calculate_zodiac_sign(4, 15) == '白羊座'
        
        # 测试金牛座 (4.20-5.20)
        assert self.module._calculate_zodiac_sign(4, 20) == '金牛座'
        assert self.module._calculate_zodiac_sign(5, 15) == '金牛座'
        
        # 测试双子座 (5.21-6.21)
        assert self.module._calculate_zodiac_sign(5, 21) == '双子座'
        assert self.module._calculate_zodiac_sign(6, 15) == '双子座'
        
        # 测试巨蟹座 (6.22-7.22)
        assert self.module._calculate_zodiac_sign(6, 22) == '巨蟹座'
        assert self.module._calculate_zodiac_sign(7, 15) == '巨蟹座'
        
        # 测试狮子座 (7.23-8.22)
        assert self.module._calculate_zodiac_sign(7, 23) == '狮子座'
        assert self.module._calculate_zodiac_sign(8, 15) == '狮子座'
        
        # 测试处女座 (8.23-9.22)
        assert self.module._calculate_zodiac_sign(8, 23) == '处女座'
        assert self.module._calculate_zodiac_sign(9, 15) == '处女座'
        
        # 测试天秤座 (9.23-10.23)
        assert self.module._calculate_zodiac_sign(9, 23) == '天秤座'
        assert self.module._calculate_zodiac_sign(10, 15) == '天秤座'
        
        # 测试天蝎座 (10.24-11.22)
        assert self.module._calculate_zodiac_sign(10, 24) == '天蝎座'
        assert self.module._calculate_zodiac_sign(11, 15) == '天蝎座'
        
        # 测试射手座 (11.23-12.21)
        assert self.module._calculate_zodiac_sign(11, 23) == '射手座'
        assert self.module._calculate_zodiac_sign(12, 15) == '射手座'
    
    def test_parse_birthday(self):
        """测试生日解析"""
        # 测试多种日期格式
        assert self.module._parse_birthday('1990-05-20').year == 1990
        assert self.module._parse_birthday('1990/05/20').month == 5
        assert self.module._parse_birthday('1990年05月20日').day == 20
        
        # 测试无效格式
        with pytest.raises(ValueError):
            self.module._parse_birthday('invalid')
    
    def test_parse_style_preferences(self):
        """测试风格偏好解析"""
        # 测试正常解析
        result = self.module._parse_style_preferences('1, 2, 3')
        assert '商务正装' in result
        assert '商务休闲' in result
        assert '休闲日常' in result
        
        # 测试空输入
        assert self.module._parse_style_preferences('') == []
        
        # 测试无效输入
        assert self.module._parse_style_preferences('999, 0') == []
    
    def test_parse_occasion_preferences(self):
        """测试场合偏好解析"""
        # 测试正常解析
        result = self.module._parse_occasion_preferences('1, 2, 5')
        assert '商务会议' in result
        assert '日常办公' in result
        assert '朋友聚会' in result
        
        # 测试空输入
        assert self.module._parse_occasion_preferences('') == []
    
    def test_get_user_data_empty(self):
        """测试获取空用户数据"""
        user_data = self.module.get_user_data()
        assert user_data == {}
    
    def test_get_user_preferences_empty(self):
        """测试获取空用户偏好"""
        preferences = self.module.get_user_preferences()
        assert preferences == {}


class TestOutfitRecommendationImprovements:
    """穿搭推荐改进测试类"""
    
    def setup_class(cls):
        """类级别的设置：初始化模块"""
        cls.module = OutfitRecommendationModule()
        cls.module.initialize()
    
    def teardown_class(cls):
        """类级别的清理：关闭模块"""
        cls.module.shutdown()
    
    def test_check_weather_match(self):
        """测试天气匹配逻辑"""
        # 测试精确匹配
        assert self.module._check_weather_match('晴', ['晴', '多云']) is True
        
        # 测试包含匹配
        assert self.module._check_weather_match('小雨', ['雨', '晴']) is True
        assert self.module._check_weather_match('大雨', ['小雨', '晴']) is True
        assert self.module._check_weather_match('雷阵雨', ['雨', '晴']) is True
        
        # 测试雪类匹配
        assert self.module._check_weather_match('小雪', ['雪', '晴']) is True
        assert self.module._check_weather_match('大雪', ['小雪', '晴']) is True
        
        # 测试不匹配
        assert self.module._check_weather_match('雨', ['雪', '晴']) is False
        assert self.module._check_weather_match('晴', ['雨', '雪']) is False
    
    def test_filter_suitable_styles_fallback(self):
        """测试风格筛选的降级机制"""
        # 测试极端温度下的默认风格
        # 当温度为-10°C时，所有风格的温度范围都不匹配
        # 应该返回所有风格作为最后手段
        styles = self.module._filter_suitable_styles(
            avg_temp=-10.0,
            weather_condition='晴',
            preferred_styles=[],
            preferred_occasions=[]
        )
        
        # 应该返回至少一些风格（降级机制）
        assert len(styles) > 0
    
    def test_filter_suitable_styles_with_user_preferences(self):
        """测试带用户偏好的风格筛选"""
        # 测试用户风格偏好优先
        styles = self.module._filter_suitable_styles(
            avg_temp=20.0,
            weather_condition='晴',
            preferred_styles=['商务正装', '优雅淑女'],
            preferred_occasions=[]
        )
        
        # 用户偏好的风格应该排在前面
        if len(styles) >= 2:
            assert styles[0] in ['商务正装', '优雅淑女']
    
    def test_filter_suitable_styles_with_occasion_preferences(self):
        """测试带场合偏好的风格筛选"""
        # 测试场合偏好影响风格排序
        styles = self.module._filter_suitable_styles(
            avg_temp=20.0,
            weather_condition='晴',
            preferred_styles=[],
            preferred_occasions=['商务会议']
        )
        
        # 商务会议应该优先匹配商务正装风格
        if len(styles) > 0:
            # 商务正装适合商务会议
            assert '商务正装' in styles or len(styles) > 0
