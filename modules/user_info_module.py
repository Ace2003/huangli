# 用户信息模块
from datetime import datetime
from typing import Dict, Any, Optional
import re

from framework import BaseModule, ModuleStatus, PerformanceMonitor, ErrorHandler, ModuleException


class UserInfoModule(BaseModule):
    """用户信息模块
    
    处理用户个人信息的收集、验证和存储
    """
    
    # 姓名验证正则表达式
    # 支持：
    # - 中文姓名：2-20个中文字符
    # - 英文姓名：2-50个英文字母，支持空格和连字符
    # - 中英文混合：至少包含2个有效字符
    NAME_PATTERN = re.compile(
        r'^[\u4e00-\u9fa5]{2,20}$|'  # 纯中文
        r'^[a-zA-Z]+(?:[ -][a-zA-Z]+){0,10}$|'  # 英文，支持空格和连字符
        r'^[\u4e00-\u9fa5a-zA-Z]{2,30}$'  # 中英文混合
    )
    
    # 禁止的姓名模式
    INVALID_NAME_PATTERNS = [
        re.compile(r'^\d+$'),  # 纯数字
        re.compile(r'^[_\-!@#$%^&*()+=,.?;:{}[\]\\|`~]+$'),  # 纯特殊字符
        re.compile(r'^[a-zA-Z]$'),  # 单个英文字母
        re.compile(r'^[\u4e00-\u9fa5]$'),  # 单个中文字
    ]
    
    # 生肖对应关系（年份 % 12）
    ZODIAC_MAP = {
        0: '猴', 1: '鸡', 2: '狗', 3: '猪', 4: '鼠', 5: '牛',
        6: '虎', 7: '兔', 8: '龙', 9: '蛇', 10: '马', 11: '羊'
    }
    
    # 星座对应关系 (月份, 开始日期, 星座名称)
    # 使用边界日期法：每个星座从特定日期开始
    ZODIAC_SIGNS = [
        (1, 20, '水瓶座'),
        (2, 19, '双鱼座'),
        (3, 21, '白羊座'),
        (4, 20, '金牛座'),
        (5, 21, '双子座'),
        (6, 22, '巨蟹座'),
        (7, 23, '狮子座'),
        (8, 23, '处女座'),
        (9, 23, '天秤座'),
        (10, 24, '天蝎座'),
        (11, 23, '射手座'),
        (12, 22, '摩羯座'),
    ]
    
    def __init__(self):
        """初始化用户信息模块"""
        super().__init__("UserInfoModule")
        self._user_data = {}
    
    def _on_initialize(self) -> bool:
        """执行具体初始化逻辑"""
        self.logger.info("用户信息模块初始化完成")
        return True
    
    def _on_shutdown(self) -> bool:
        """执行具体关闭逻辑"""
        self._user_data.clear()
        self.logger.info("用户信息模块已关闭")
        return True
    
    def collect_user_info_interactive(self) -> Dict[str, Any]:
        """交互式收集用户信息
        
        Returns:
            用户信息字典
        """
        start_time = datetime.now().timestamp()
        success = True
        
        try:
            self.check_ready()
            
            print("\n" + "="*60)
            print("【请输入您的个人信息】")
            print("="*60)
            
            user_data = {}
            
            # 1. 姓名
            print("\n【姓名输入规则】")
            print("• 中文姓名：2-20个中文字符（如：张三、欧阳娜娜）")
            print("• 英文姓名：2个以上英文字母，支持空格和连字符（如：John Smith、Mary-Ann）")
            print("• 中英文混合：至少2个有效字符（如：李John）")
            print("• 不能是纯数字、纯特殊字符或单个字符")
            
            while True:
                name = input("\n请输入您的姓名：").strip()
                
                # 验证姓名
                is_valid, error_msg = self._validate_name(name)
                
                if is_valid:
                    user_data['姓名'] = name
                    self.logger.info(f"姓名验证通过: {name}")
                    break
                else:
                    print(f"❌ 姓名无效：{error_msg}")
                    print("请重新输入符合规则的姓名。")
            
            # 2. 性别
            while True:
                gender = input("请输入您的性别（男/女）：").strip()
                if gender in ['男', '女']:
                    user_data['性别'] = gender
                    break
                print("请输入有效的性别（男或女）。")
            
            # 3. 生日
            while True:
                birthday_str = input("请输入您的生日（格式：YYYY-MM-DD，如1990-05-20）：").strip()
                try:
                    birthday = self._parse_birthday(birthday_str)
                    user_data['生日'] = birthday
                    user_data['生日字符串'] = birthday_str
                    
                    # 计算生肖和星座
                    user_data['生肖'] = self._calculate_zodiac(birthday.year)
                    user_data['星座'] = self._calculate_zodiac_sign(birthday.month, birthday.day)
                    
                    # 计算年龄
                    today = datetime.now()
                    age = today.year - birthday.year
                    if (today.month, today.day) < (birthday.month, birthday.day):
                        age -= 1
                    user_data['年龄'] = age
                    
                    break
                except ValueError as e:
                    print(f"输入错误：{e}，请重新输入。")
            
            # 4. 选择城市
            print("\n【请选择您所在的城市】")
            print("可用城市：北京、上海、广州、深圳、杭州、南京、成都、武汉、西安、重庆...")
            print("（输入城市名称或序号，输入'help'查看完整列表）")
            
            while True:
                city_input = input("\n请输入城市名称或序号：").strip()
                
                if city_input.lower() == 'help':
                    self._show_supported_cities()
                    continue
                
                city = self._parse_city_input(city_input)
                if city:
                    user_data['城市'] = city
                    break
                print(f"未找到城市 '{city_input}'，请重新输入或输入'help'查看可用城市。")
            
            # 5. 风格偏好（可选）
            print("\n【可选：请选择您喜欢的穿搭风格（可多选，用逗号分隔）】")
            print("1. 商务正装  2. 商务休闲  3. 休闲日常  4. 运动休闲  5. 优雅淑女  6. 街头潮流")
            style_input = input("请输入风格序号（直接回车跳过）：").strip()
            
            if style_input:
                style_preferences = self._parse_style_preferences(style_input)
                user_data['风格偏好'] = style_preferences
            else:
                user_data['风格偏好'] = []
            
            # 6. 场合偏好（可选）
            print("\n【可选：请选择您今天的主要场合（可多选，用逗号分隔）】")
            print("1. 商务会议  2. 日常办公  3. 客户拜访  4. 购物  5. 朋友聚会")
            print("6. 运动健身  7. 户外活动  8. 约会  9. 正式宴请  10. 婚礼")
            occasion_input = input("请输入场合序号（直接回车跳过）：").strip()
            
            if occasion_input:
                occasion_preferences = self._parse_occasion_preferences(occasion_input)
                user_data['场合偏好'] = occasion_preferences
            else:
                user_data['场合偏好'] = []
            
            # 保存用户数据
            self._user_data = user_data
            
            # 显示收集到的信息
            self._display_user_info(user_data)
            
            self.logger.info(f"成功收集用户信息: {user_data.get('姓名', '未知')}")
            return user_data
            
        except Exception as e:
            success = False
            ErrorHandler.handle_exception(e, "收集用户信息", self.module_name)
            raise ModuleException(
                self.module_name,
                f"收集用户信息失败: {str(e)}",
                "USER_INFO_COLLECT_ERROR"
            )
        finally:
            end_time = datetime.now().timestamp()
            self._update_metrics(success, end_time - start_time)
    
    def _parse_birthday(self, birthday_str: str) -> datetime:
        """解析生日字符串
        
        Args:
            birthday_str: 生日字符串，格式 YYYY-MM-DD
            
        Returns:
            datetime 对象
        """
        # 支持多种格式
        formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y年%m月%d日']
        
        for fmt in formats:
            try:
                return datetime.strptime(birthday_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"日期格式不正确，请使用 YYYY-MM-DD 格式")
    
    def _calculate_zodiac(self, year: int) -> str:
        """计算生肖
        
        Args:
            year: 年份
            
        Returns:
            生肖名称
        """
        return self.ZODIAC_MAP[year % 12]
    
    def _calculate_zodiac_sign(self, month: int, day: int) -> str:
        """计算星座
        
        标准星座日期：
        - 摩羯座: 12月22日 - 1月19日
        - 水瓶座: 1月20日 - 2月18日
        - 双鱼座: 2月19日 - 3月20日
        - 白羊座: 3月21日 - 4月19日
        - 金牛座: 4月20日 - 5月20日
        - 双子座: 5月21日 - 6月21日
        - 巨蟹座: 6月22日 - 7月22日
        - 狮子座: 7月23日 - 8月22日
        - 处女座: 8月23日 - 9月22日
        - 天秤座: 9月23日 - 10月23日
        - 天蝎座: 10月24日 - 11月22日
        - 射手座: 11月23日 - 12月21日
        
        Args:
            month: 月份
            day: 日期
            
        Returns:
            星座名称
        """
        # 使用边界日期法，从后往前检查更容易处理
        # 每个元组: (开始月份, 开始日期, 星座名称)
        zodiac_boundaries = [
            (12, 22, '摩羯座'),
            (11, 23, '射手座'),
            (10, 24, '天蝎座'),
            (9, 23, '天秤座'),
            (8, 23, '处女座'),
            (7, 23, '狮子座'),
            (6, 22, '巨蟹座'),
            (5, 21, '双子座'),
            (4, 20, '金牛座'),
            (3, 21, '白羊座'),
            (2, 19, '双鱼座'),
            (1, 20, '水瓶座'),
        ]
        
        # 从后往前检查，找到第一个满足条件的星座
        for start_month, start_day, sign_name in zodiac_boundaries:
            if (month > start_month) or (month == start_month and day >= start_day):
                return sign_name
        
        # 如果都不满足，说明是1月1日-1月19日，属于摩羯座
        return '摩羯座'
    
    def _validate_name(self, name: str) -> tuple:
        """验证姓名是否有效
        
        Args:
            name: 姓名字符串
            
        Returns:
            (是否有效, 错误信息) 元组
        """
        # 检查空值
        if not name or name.strip() == '':
            return False, "姓名不能为空"
        
        name = name.strip()
        
        # 检查长度
        if len(name) < 2:
            return False, "姓名至少需要2个字符"
        
        if len(name) > 50:
            return False, "姓名不能超过50个字符"
        
        # 检查禁止的模式
        for pattern in self.INVALID_NAME_PATTERNS:
            if pattern.match(name):
                if re.match(r'^\d+$', name):
                    return False, "姓名不能是纯数字"
                elif re.match(r'^[_\-!@#$%^&*()+=,.?;:{}[\]\\|`~]+$', name):
                    return False, "姓名不能是纯特殊字符"
                elif len(name) == 1:
                    return False, "姓名至少需要2个字符"
        
        # 检查是否符合姓名格式
        if self.NAME_PATTERN.match(name):
            return True, "验证通过"
        
        # 额外的验证逻辑
        # 统计有效字符数量
        chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', name))
        english_chars = len(re.findall(r'[a-zA-Z]', name))
        
        # 检查是否包含至少2个有效字符（中文或英文）
        if chinese_chars + english_chars < 2:
            return False, "姓名需要至少包含2个中文字符或英文字母"
        
        # 检查是否包含过多无效字符
        invalid_chars = len(name) - chinese_chars - english_chars - name.count(' ') - name.count('-')
        if invalid_chars > 0:
            return False, "姓名只能包含中文字符、英文字母、空格和连字符"
        
        # 允许通过（兜底）
        return True, "验证通过"
    
    def _show_supported_cities(self):
        """显示支持的城市列表"""
        from modules.weather_module import WeatherModule
        
        # 创建临时天气模块获取支持的城市
        temp_weather = WeatherModule()
        temp_weather.initialize()
        cities = temp_weather.get_supported_cities()
        temp_weather.shutdown()
        
        print("\n【支持的城市列表】")
        for i, city in enumerate(cities, 1):
            print(f"{i:2d}. {city}", end='  ')
            if i % 5 == 0:
                print()
        print()
    
    def _parse_city_input(self, city_input: str) -> Optional[str]:
        """解析城市输入
        
        Args:
            city_input: 用户输入的城市名称或序号
            
        Returns:
            城市名称，如果无效则返回 None
        """
        from modules.weather_module import WeatherModule
        
        # 创建临时天气模块获取支持的城市
        temp_weather = WeatherModule()
        temp_weather.initialize()
        cities = temp_weather.get_supported_cities()
        temp_weather.shutdown()
        
        # 尝试作为序号解析
        if city_input.isdigit():
            index = int(city_input) - 1
            if 0 <= index < len(cities):
                return cities[index]
        
        # 尝试作为城市名称（支持模糊匹配）
        city_input_lower = city_input.lower()
        for city in cities:
            if city_input_lower in city.lower() or city.lower() in city_input_lower:
                return city
        
        return None
    
    def _parse_style_preferences(self, style_input: str) -> list:
        """解析风格偏好输入
        
        Args:
            style_input: 用户输入的风格序号，用逗号分隔
            
        Returns:
            风格名称列表
        """
        style_map = {
            '1': '商务正装',
            '2': '商务休闲',
            '3': '休闲日常',
            '4': '运动休闲',
            '5': '优雅淑女',
            '6': '街头潮流'
        }
        
        preferences = []
        for item in style_input.split(','):
            item = item.strip()
            if item in style_map:
                preferences.append(style_map[item])
        
        return preferences
    
    def _parse_occasion_preferences(self, occasion_input: str) -> list:
        """解析场合偏好输入
        
        Args:
            occasion_input: 用户输入的场合序号，用逗号分隔
            
        Returns:
            场合名称列表
        """
        occasion_map = {
            '1': '商务会议',
            '2': '日常办公',
            '3': '客户拜访',
            '4': '购物',
            '5': '朋友聚会',
            '6': '运动健身',
            '7': '户外活动',
            '8': '约会',
            '9': '正式宴请',
            '10': '婚礼'
        }
        
        preferences = []
        for item in occasion_input.split(','):
            item = item.strip()
            if item in occasion_map:
                preferences.append(occasion_map[item])
        
        return preferences
    
    def _display_user_info(self, user_data: Dict[str, Any]):
        """显示收集到的用户信息
        
        Args:
            user_data: 用户信息字典
        """
        print("\n" + "="*60)
        print("【您的个人信息】")
        print("="*60)
        print(f"  姓名: {user_data.get('姓名', 'N/A')}")
        print(f"  性别: {user_data.get('性别', 'N/A')}")
        print(f"  生日: {user_data.get('生日字符串', 'N/A')}")
        print(f"  生肖: {user_data.get('生肖', 'N/A')}")
        print(f"  星座: {user_data.get('星座', 'N/A')}")
        print(f"  年龄: {user_data.get('年龄', 'N/A')} 岁")
        print(f"  城市: {user_data.get('城市', 'N/A')}")
        
        if user_data.get('风格偏好'):
            print(f"  风格偏好: {', '.join(user_data['风格偏好'])}")
        
        if user_data.get('场合偏好'):
            print(f"  场合偏好: {', '.join(user_data['场合偏好'])}")
        
        print("="*60)
    
    def get_user_data(self) -> Dict[str, Any]:
        """获取用户数据
        
        Returns:
            用户信息字典
        """
        return self._user_data.copy()
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """获取用户偏好（用于穿搭推荐）
        
        Returns:
            用户偏好字典
        """
        preferences = {}
        
        if self._user_data.get('风格偏好'):
            preferences['风格'] = self._user_data['风格偏好']
        
        if self._user_data.get('场合偏好'):
            preferences['场合'] = self._user_data['场合偏好']
        
        # 根据性别调整推荐
        if self._user_data.get('性别') == '女':
            # 女性用户优先考虑优雅淑女风格
            if '风格' not in preferences:
                preferences['风格'] = ['优雅淑女', '休闲日常']
        
        return preferences
