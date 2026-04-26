# 黄历模块
from datetime import datetime
from typing import Dict, Any, Optional
import random

from framework import BaseModule, ModuleStatus, PerformanceMonitor, ErrorHandler, ModuleException
from framework import IHuangliModule


class HuangliModule(BaseModule, IHuangliModule):
    """黄历模块
    
    提供传统黄历信息查询功能
    """
    
    # 农历月份名称
    LUNAR_MONTHS = [
        '正月', '二月', '三月', '四月', '五月', '六月',
        '七月', '八月', '九月', '十月', '冬月', '腊月'
    ]
    
    # 农历日期名称
    LUNAR_DAYS = [
        '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
        '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
        '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'
    ]
    
    # 十二生肖
    ZODIAC = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
    
    # 五行属性
    ELEMENTS = ['金', '木', '水', '火', '土']
    
    # 干支
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 宜事列表
    YI_ACTIVITIES = [
        '嫁娶', '祭祀', '出行', '祈福', '求嗣', '开光', '入宅', '安床',
        '修造', '动土', '上梁', '竖柱', '开市', '立券', '纳财', '栽种',
        '纳畜', '拆卸', '破土', '启钻', '安葬'
    ]
    
    # 忌事列表
    JI_ACTIVITIES = [
        '嫁娶', '祭祀', '出行', '祈福', '求嗣', '开光', '入宅', '安床',
        '修造', '动土', '上梁', '竖柱', '开市', '立券', '纳财', '栽种',
        '纳畜', '拆卸', '破土', '启钻', '安葬'
    ]
    
    # 冲煞对应
    CHONG_SHA = [
        '冲鼠煞北', '冲牛煞西', '冲虎煞南', '冲兔煞东',
        '冲龙煞北', '冲蛇煞西', '冲马煞南', '冲羊煞东',
        '冲猴煞北', '冲鸡煞西', '冲狗煞南', '冲猪煞东'
    ]
    
    # 方位
    DIRECTIONS = ['东北', '正东', '东南', '正南', '西南', '正西', '西北', '正北']
    
    def __init__(self):
        """初始化黄历模块"""
        super().__init__("HuangliModule")
        self._data_cache = {}
    
    def _on_initialize(self) -> bool:
        """执行具体初始化逻辑"""
        self.logger.info("黄历模块初始化完成")
        return True
    
    def _on_shutdown(self) -> bool:
        """执行具体关闭逻辑"""
        self._data_cache.clear()
        self.logger.info("黄历模块已关闭")
        return True
    
    def get_huangli(self, date: datetime) -> Dict[str, Any]:
        """获取指定日期的黄历信息
        
        Args:
            date: 日期对象
            
        Returns:
            包含黄历信息的字典
        """
        start_time = datetime.now().timestamp()
        success = True
        
        try:
            self.check_ready()
            
            # 检查缓存
            date_key = date.strftime('%Y-%m-%d')
            if date_key in self._data_cache:
                self.logger.debug(f"从缓存获取黄历数据: {date_key}")
                return self._data_cache[date_key]
            
            # 计算黄历信息
            huangli_data = self._calculate_huangli(date)
            
            # 缓存结果
            self._data_cache[date_key] = huangli_data
            
            self.logger.info(f"成功获取黄历数据: {date_key}")
            return huangli_data
            
        except Exception as e:
            success = False
            ErrorHandler.handle_exception(e, "获取黄历数据", self.module_name)
            raise ModuleException(
                self.module_name,
                f"获取黄历数据失败: {str(e)}",
                "HUANGLI_FETCH_ERROR"
            )
        finally:
            end_time = datetime.now().timestamp()
            self._update_metrics(success, end_time - start_time)
    
    def _calculate_huangli(self, date: datetime) -> Dict[str, Any]:
        """计算黄历信息
        
        Args:
            date: 日期对象
            
        Returns:
            黄历信息字典
        """
        # 计算农历日期（简化版，实际应该使用真实的农历算法）
        lunar_month = self.LUNAR_MONTHS[(date.month - 1) % 12]
        lunar_day = self.LUNAR_DAYS[(date.day - 1) % 30]
        
        # 计算生肖
        year_index = (date.year - 1900) % 12
        zodiac = self.ZODIAC[year_index]
        
        # 计算干支
        tiangan_index = (date.year - 4) % 10
        dizhi_index = (date.year - 4) % 12
        ganzhi = f"{self.TIANGAN[tiangan_index]}{self.DIZHI[dizhi_index]}"
        
        # 计算五行
        element_index = (date.year + date.month + date.day) % 5
        element = self.ELEMENTS[element_index]
        
        # 随机选择宜事（实际应该基于传统算法）
        random.seed(date.year * 10000 + date.month * 100 + date.day)
        yi_count = random.randint(3, 6)
        yi_activities = random.sample(self.YI_ACTIVITIES, yi_count)
        
        # 随机选择忌事
        ji_count = random.randint(2, 5)
        available_ji = [a for a in self.JI_ACTIVITIES if a not in yi_activities]
        if len(available_ji) < ji_count:
            available_ji = self.JI_ACTIVITIES
        ji_activities = random.sample(available_ji, ji_count)
        
        # 计算冲煞
        chong_index = (date.day + dizhi_index) % 12
        chong_sha = self.CHONG_SHA[chong_index]
        
        # 计算幸运方位
        direction_index = (date.year + date.month + date.day) % 8
        lucky_direction = self.DIRECTIONS[direction_index]
        
        return {
            '公历日期': date.strftime('%Y年%m月%d日'),
            '星期': self._get_weekday_name(date.weekday()),
            '农历': f"{lunar_month}{lunar_day}",
            '干支': ganzhi,
            '生肖': zodiac,
            '五行': element,
            '宜': ','.join(yi_activities),
            '忌': ','.join(ji_activities),
            '冲煞': chong_sha,
            '幸运方位': lucky_direction,
            '幸运数字': self._get_lucky_number(date),
            '吉神宜趋': self._get_jishen(date),
            '凶神宜忌': self._get_xiongshen(date)
        }
    
    def _get_weekday_name(self, weekday: int) -> str:
        """获取星期名称
        
        Args:
            weekday: 星期索引（0=周一，6=周日）
            
        Returns:
            星期名称
        """
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        return weekdays[weekday]
    
    def _get_lucky_number(self, date: datetime) -> int:
        """获取幸运数字
        
        Args:
            date: 日期对象
            
        Returns:
            幸运数字
        """
        return (date.year + date.month + date.day) % 9 + 1
    
    def _get_jishen(self, date: datetime) -> str:
        """获取吉神宜趋
        
        Args:
            date: 日期对象
            
        Returns:
            吉神宜趋字符串
        """
        jishen_list = ['母仓', '时阳', '生气', '天仓', '不将', '玉宇']
        random.seed(date.year * 100 + date.month)
        return ','.join(random.sample(jishen_list, 3))
    
    def _get_xiongshen(self, date: datetime) -> str:
        """获取凶神宜忌
        
        Args:
            date: 日期对象
            
        Returns:
            凶神宜忌字符串
        """
        xiongshen_list = ['天火', '天吏', '五虚', '往亡', '天刑']
        random.seed(date.year * 100 + date.month + 1000)
        return ','.join(random.sample(xiongshen_list, 2))
    
    def get_lucky_direction(self, date: datetime) -> str:
        """获取指定日期的幸运方位
        
        Args:
            date: 日期对象
            
        Returns:
            幸运方位字符串
        """
        huangli_data = self.get_huangli(date)
        return huangli_data.get('幸运方位', '未知')
    
    def get_element(self, date: datetime) -> str:
        """获取指定日期的五行属性
        
        Args:
            date: 日期对象
            
        Returns:
            五行属性字符串
        """
        huangli_data = self.get_huangli(date)
        return huangli_data.get('五行', '未知')
