# 穿搭推荐模块
from datetime import datetime
from typing import Dict, Any, List, Optional
import random

from framework import BaseModule, ModuleStatus, PerformanceMonitor, ErrorHandler, ModuleException
from framework import IOutfitRecommendationModule


class OutfitRecommendationModule(BaseModule, IOutfitRecommendationModule):
    """穿搭推荐模块
    
    提供穿搭推荐功能
    """
    
    # 穿搭风格定义
    STYLES = {
        '商务正装': {
            '描述': '正式场合必备，彰显专业气质',
            '适合场合': ['商务会议', '正式宴请', '婚礼'],
            '温度范围': (10, 30),
            '天气偏好': ['晴', '多云', '阴']
        },
        '商务休闲': {
            '描述': '兼顾专业与舒适，适合日常办公',
            '适合场合': ['日常办公', '客户拜访', '商务午餐'],
            '温度范围': (15, 35),
            '天气偏好': ['晴', '多云', '阴']
        },
        '休闲日常': {
            '描述': '轻松舒适，适合日常生活',
            '适合场合': ['购物', '朋友聚会', '休闲娱乐'],
            '温度范围': (10, 35),
            '天气偏好': ['晴', '多云', '阴', '小雨']
        },
        '运动休闲': {
            '描述': '活力动感，适合运动健身',
            '适合场合': ['运动健身', '户外活动', '短途旅行'],
            '温度范围': (15, 35),
            '天气偏好': ['晴', '多云']
        },
        '优雅淑女': {
            '描述': '温柔优雅，彰显女性魅力',
            '适合场合': ['约会', '下午茶', '文艺活动'],
            '温度范围': (15, 30),
            '天气偏好': ['晴', '多云']
        },
        '街头潮流': {
            '描述': '时尚个性，彰显独特品味',
            '适合场合': ['街头拍照', '潮流活动', '朋友聚会'],
            '温度范围': (10, 30),
            '天气偏好': ['晴', '多云']
        }
    }
    
    # 服装单品定义
    CLOTHING_ITEMS = {
        '上装': {
            '商务正装': ['西装外套', '正装衬衫', '马甲'],
            '商务休闲': ['休闲西装', '针织衫', '休闲衬衫', 'POLO衫'],
            '休闲日常': ['T恤', '卫衣', '牛仔外套', '夹克'],
            '运动休闲': ['运动T恤', '运动卫衣', '速干衣'],
            '优雅淑女': ['连衣裙', '蕾丝上衣', '雪纺衫', '针织开衫'],
            '街头潮流': ['oversizeT恤', '潮牌卫衣', '牛仔外套', '棒球服']
        },
        '下装': {
            '商务正装': ['西裤', '西装裙'],
            '商务休闲': ['休闲西裤', '卡其裤', '直筒裙'],
            '休闲日常': ['牛仔裤', '休闲裤', '运动裤', '短裙'],
            '运动休闲': ['运动裤', '速干裤', '运动短裤'],
            '优雅淑女': ['半身裙', '阔腿裤', '直筒裙'],
            '街头潮流': ['工装裤', '牛仔裤', '运动裤', '短裙']
        },
        '外套': {
            '商务正装': ['大衣', '风衣', '西装外套'],
            '商务休闲': ['风衣', '夹克', '针织开衫'],
            '休闲日常': ['牛仔外套', '夹克', '卫衣外套', '风衣'],
            '运动休闲': ['运动外套', '冲锋衣'],
            '优雅淑女': ['风衣', '针织开衫', '小香风外套'],
            '街头潮流': ['棒球服', '牛仔外套', '冲锋衣', '夹克']
        },
        '配饰': {
            '商务正装': ['领带', '手表', '公文包', '皮鞋'],
            '商务休闲': ['手表', '皮带', '休闲包', '休闲鞋'],
            '休闲日常': ['帽子', '背包', '运动鞋', '帆布鞋'],
            '运动休闲': ['运动手环', '运动包', '运动鞋'],
            '优雅淑女': ['丝巾', '手提包', '高跟鞋', '项链'],
            '街头潮流': ['帽子', '背包', '运动鞋', '项链', '手链']
        }
    }
    
    # 温度对应的穿搭建议
    TEMPERATURE_GUIDE = {
        '极寒(<0°C)': {
            '建议': '注意保暖，多层穿搭',
            '必备': ['羽绒服', '厚毛衣', '围巾', '手套', '帽子', '保暖内衣']
        },
        '寒冷(0-10°C)': {
            '建议': '保暖为主，选择厚重面料',
            '必备': ['大衣', '毛衣', '围巾', '手套']
        },
        '凉爽(10-20°C)': {
            '建议': '灵活搭配，可穿外套',
            '必备': ['外套', '长袖上衣', '长裤']
        },
        '舒适(20-28°C)': {
            '建议': '舒适为主，单层即可',
            '必备': ['T恤', '衬衫', '长裤/长裙']
        },
        '炎热(>28°C)': {
            '建议': '清凉透气，选择浅色',
            '必备': ['短袖', '短裤/短裙', '凉鞋']
        }
    }
    
    def __init__(self):
        """初始化穿搭推荐模块"""
        super().__init__("OutfitRecommendationModule")
    
    def _on_initialize(self) -> bool:
        """执行具体初始化逻辑"""
        self.logger.info("穿搭推荐模块初始化完成")
        return True
    
    def _on_shutdown(self) -> bool:
        """执行具体关闭逻辑"""
        self.logger.info("穿搭推荐模块已关闭")
        return True
    
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
            穿搭推荐列表
        """
        start_time = datetime.now().timestamp()
        success = True
        
        try:
            self.check_ready()
            
            recommendations = []
            
            # 获取温度范围
            low_temp = weather_data.get('最低温度值', 20)
            high_temp = weather_data.get('最高温度值', 25)
            avg_temp = (low_temp + high_temp) / 2
            
            # 获取天气状况
            weather_condition = weather_data.get('天气', '晴')
            
            # 获取用户偏好（如果有）
            preferred_styles = user_preferences.get('风格', []) if user_preferences else []
            preferred_occasions = user_preferences.get('场合', []) if user_preferences else []
            
            # 筛选适合的风格
            suitable_styles = self._filter_suitable_styles(
                avg_temp, weather_condition, preferred_styles, preferred_occasions
            )
            
            # 为每个适合的风格生成推荐
            for style in suitable_styles[:3]:  # 最多返回3个推荐
                recommendation = self._generate_outfit_recommendation(
                    style, lucky_colors, weather_data, huangli_data
                )
                recommendations.append(recommendation)
            
            # 按推荐指数排序
            recommendations.sort(key=lambda x: x.get('推荐指数', 0), reverse=True)
            
            self.logger.info(f"成功生成穿搭推荐: {len(recommendations)} 套")
            return recommendations
            
        except Exception as e:
            success = False
            ErrorHandler.handle_exception(e, "生成穿搭推荐", self.module_name)
            raise ModuleException(
                self.module_name,
                f"生成穿搭推荐失败: {str(e)}",
                "OUTFIT_RECOMMENDATION_ERROR"
            )
        finally:
            end_time = datetime.now().timestamp()
            self._update_metrics(success, end_time - start_time)
    
    def _filter_suitable_styles(self, avg_temp: float, weather_condition: str,
                                preferred_styles: List[str], 
                                preferred_occasions: List[str]) -> List[str]:
        """筛选适合的风格
        
        Args:
            avg_temp: 平均温度
            weather_condition: 天气状况
            preferred_styles: 用户偏好的风格
            preferred_occasions: 用户偏好的场合
            
        Returns:
            适合的风格列表
        """
        suitable_styles = []
        
        # 第一阶段：严格匹配（温度和天气都匹配）
        for style_name, style_info in self.STYLES.items():
            # 检查温度范围
            min_temp, max_temp = style_info['温度范围']
            if not (min_temp <= avg_temp <= max_temp):
                continue
            
            # 检查天气偏好（使用更宽松的匹配）
            weather_match = self._check_weather_match(weather_condition, style_info['天气偏好'])
            if not weather_match:
                continue
            
            suitable_styles.append(style_name)
        
        # 第二阶段：如果没有严格匹配的风格，放宽天气条件
        if not suitable_styles:
            for style_name, style_info in self.STYLES.items():
                # 检查温度范围
                min_temp, max_temp = style_info['温度范围']
                if not (min_temp <= avg_temp <= max_temp):
                    continue
                
                # 不检查天气，只看温度
                suitable_styles.append(style_name)
        
        # 第三阶段：如果还是没有，返回所有风格（作为最后手段）
        if not suitable_styles:
            suitable_styles = list(self.STYLES.keys())
        
        # 如果用户有风格偏好，优先考虑
        if preferred_styles:
            # 将用户偏好的风格放在前面
            preferred_list = [s for s in preferred_styles if s in suitable_styles]
            other_list = [s for s in suitable_styles if s not in preferred_styles]
            suitable_styles = preferred_list + other_list
        
        # 如果用户有场合偏好，调整顺序
        if preferred_occasions:
            # 计算风格与场合的匹配度
            style_scores = {}
            for style in suitable_styles:
                score = 0
                style_occasions = self.STYLES[style]['适合场合']
                for occasion in preferred_occasions:
                    if occasion in style_occasions:
                        score += 1
                style_scores[style] = score
            
            # 按分数排序（分数高的在前）
            suitable_styles.sort(key=lambda s: style_scores.get(s, 0), reverse=True)
        
        return suitable_styles
    
    def _check_weather_match(self, weather_condition: str, preferred_weathers: List[str]) -> bool:
        """检查天气是否匹配
        
        Args:
            weather_condition: 实际天气状况
            preferred_weathers: 风格偏好的天气列表
            
        Returns:
            是否匹配
        """
        # 标准化天气条件
        weather_lower = weather_condition.lower()
        
        for pref in preferred_weathers:
            pref_lower = pref.lower()
            
            # 精确匹配
            if pref_lower == weather_lower:
                return True
            
            # 包含匹配
            if pref_lower in weather_lower or weather_lower in pref_lower:
                return True
            
            # 特殊处理：小雨/中雨/大雨/阵雨/雷阵雨 都属于雨类
            if '雨' in pref_lower and '雨' in weather_lower:
                return True
            
            # 雪类
            if '雪' in pref_lower and '雪' in weather_lower:
                return True
        
        return False
    
    def _generate_outfit_recommendation(self, style: str,
                                        lucky_colors: List[Dict[str, Any]],
                                        weather_data: Dict[str, Any],
                                        huangli_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成具体的穿搭推荐
        
        Args:
            style: 风格名称
            lucky_colors: 幸运色列表
            weather_data: 天气数据
            huangli_data: 黄历数据
            
        Returns:
            穿搭推荐字典
        """
        # 获取风格信息
        style_info = self.STYLES.get(style, {})
        
        # 获取幸运色作为主色调
        primary_color = lucky_colors[0] if lucky_colors else {'名称': '白色', 'Hex': 'FFFFFF'}
        
        # 选择配色
        matching_colors = []
        if len(lucky_colors) > 1:
            matching_colors = lucky_colors[1:3]  # 取前2-3个幸运色作为配色
        
        # 选择服装单品
        outfit_items = {}
        for category, styles in self.CLOTHING_ITEMS.items():
            if style in styles:
                items = styles[style]
                outfit_items[category] = random.choice(items) if items else ''
        
        # 生成穿搭建议
        outfit_suggestion = self._generate_outfit_suggestion(
            style, outfit_items, primary_color, matching_colors
        )
        
        # 计算推荐指数
        recommendation_score = self._calculate_recommendation_score(
            style, weather_data, huangli_data, lucky_colors
        )
        
        return {
            '风格': style,
            '风格描述': style_info.get('描述', ''),
            '主色': primary_color,
            '配色': matching_colors,
            '服装单品': outfit_items,
            '适合场合': style_info.get('适合场合', []),
            '穿搭建议': outfit_suggestion,
            '温度建议': self._get_temperature_advice(weather_data),
            '推荐指数': round(recommendation_score, 2)
        }
    
    def _generate_outfit_suggestion(self, style: str, outfit_items: Dict[str, str],
                                    primary_color: Dict[str, Any],
                                    matching_colors: List[Dict[str, Any]]) -> str:
        """生成穿搭建议文本
        
        Args:
            style: 风格名称
            outfit_items: 服装单品字典
            primary_color: 主色调
            matching_colors: 配色列表
            
        Returns:
            穿搭建议字符串
        """
        suggestions = []
        
        # 主色调建议
        primary_name = primary_color.get('名称', '')
        suggestions.append(f"选择{primary_name}作为主色调，{primary_color.get('寓意', '')}。")
        
        # 配色建议
        if matching_colors:
            color_names = [c.get('名称', '') for c in matching_colors]
            suggestions.append(f"可以搭配{', '.join(color_names)}作为配色。")
        
        # 服装搭配建议
        if outfit_items:
            items_list = []
            for category, item in outfit_items.items():
                if item:
                    items_list.append(f"{category}选择{item}")
            if items_list:
                suggestions.append(f"{', '.join(items_list)}。")
        
        return ' '.join(suggestions)
    
    def _get_temperature_advice(self, weather_data: Dict[str, Any]) -> str:
        """获取温度建议
        
        Args:
            weather_data: 天气数据
            
        Returns:
            温度建议字符串
        """
        low_temp = weather_data.get('最低温度值', 20)
        high_temp = weather_data.get('最高温度值', 25)
        avg_temp = (low_temp + high_temp) / 2
        
        if avg_temp < 0:
            return self.TEMPERATURE_GUIDE['极寒(<0°C)']['建议']
        elif avg_temp < 10:
            return self.TEMPERATURE_GUIDE['寒冷(0-10°C)']['建议']
        elif avg_temp < 20:
            return self.TEMPERATURE_GUIDE['凉爽(10-20°C)']['建议']
        elif avg_temp < 28:
            return self.TEMPERATURE_GUIDE['舒适(20-28°C)']['建议']
        else:
            return self.TEMPERATURE_GUIDE['炎热(>28°C)']['建议']
    
    def _calculate_recommendation_score(self, style: str,
                                        weather_data: Dict[str, Any],
                                        huangli_data: Dict[str, Any],
                                        lucky_colors: List[Dict[str, Any]]) -> float:
        """计算推荐指数
        
        Args:
            style: 风格名称
            weather_data: 天气数据
            huangli_data: 黄历数据
            lucky_colors: 幸运色列表
            
        Returns:
            推荐指数（0-1之间）
        """
        score = 0.7  # 基础分
        
        # 幸运色加分
        if lucky_colors:
            score += 0.1
        
        # 天气匹配加分
        style_info = self.STYLES.get(style, {})
        weather_condition = weather_data.get('天气', '晴')
        weather_preferences = style_info.get('天气偏好', [])
        if any(pref in weather_condition for pref in weather_preferences):
            score += 0.1
        
        # 宜事加分
        yi_activities = huangli_data.get('宜', '').split(',')
        suitable_occasions = style_info.get('适合场合', [])
        
        # 简单匹配：如果宜事包含出行、聚会等，加分
        yi_keywords = ['出行', '聚会', '宴会', '嫁娶', '开市']
        for activity in yi_activities:
            if any(keyword in activity for keyword in yi_keywords):
                score += 0.05
                break
        
        return min(score, 1.0)
    
    def get_style_suggestions(self, weather_condition: str,
                             temperature_range: tuple) -> List[str]:
        """根据天气获取风格建议
        
        Args:
            weather_condition: 天气状况
            temperature_range: 温度范围(最低, 最高)
            
        Returns:
            适合的风格列表
        """
        low_temp, high_temp = temperature_range
        avg_temp = (low_temp + high_temp) / 2
        
        suitable_styles = []
        for style_name, style_info in self.STYLES.items():
            min_temp, max_temp = style_info['温度范围']
            if min_temp <= avg_temp <= max_temp:
                weather_match = any(
                    pref in weather_condition 
                    for pref in style_info['天气偏好']
                )
                if weather_match:
                    suitable_styles.append(style_name)
        
        return suitable_styles
    
    def get_occasion_recommendations(self, occasion: str,
                                     lucky_colors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """根据场合获取穿搭推荐
        
        Args:
            occasion: 场合名称
            lucky_colors: 幸运色列表
            
        Returns:
            穿搭推荐字典
        """
        # 找到适合该场合的风格
        suitable_styles = []
        for style_name, style_info in self.STYLES.items():
            if occasion in style_info['适合场合']:
                suitable_styles.append(style_name)
        
        if not suitable_styles:
            # 如果没有找到，返回默认风格
            suitable_styles = ['休闲日常']
        
        # 选择第一个适合的风格
        selected_style = suitable_styles[0]
        
        return {
            '风格': selected_style,
            '场合': occasion,
            '主色': lucky_colors[0] if lucky_colors else {'名称': '白色', 'Hex': 'FFFFFF'},
            '配色': lucky_colors[1:3] if len(lucky_colors) > 1 else []
        }
