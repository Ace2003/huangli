# 运势助手主入口
import logging
import logging.config
import os
from datetime import datetime
from pathlib import Path

from config import LOG_CONFIG, BASE_DIR
from framework import PerformanceMonitor, ErrorHandler, setup_logging
from modules import (
    HuangliModule, WeatherModule, LuckyColorModule, 
    OutfitRecommendationModule, UserInfoModule
)


def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        BASE_DIR / 'logs',
        BASE_DIR / 'data',
        BASE_DIR / 'cache'
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def display_welcome():
    """显示欢迎信息"""
    print("\n" + "="*60)
    print("           🌟 欢迎使用运势助手 🌟")
    print("="*60)
    print("\n本应用将根据您的个人信息、传统黄历、")
    print("今日天气和幸运色，为您推荐最佳穿搭方案！")
    print("\n请按照提示输入您的信息...")


def display_outfit_recommendation(outfit: dict, index: int):
    """显示单条穿搭推荐
    
    Args:
        outfit: 穿搭推荐字典
        index: 推荐序号
    """
    print(f"\n  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  【推荐方案 {index}】")
    print(f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # 风格信息
    style = outfit.get('风格', 'N/A')
    style_desc = outfit.get('风格描述', '')
    print(f"  📌 风格: {style}")
    if style_desc:
        print(f"     {style_desc}")
    
    # 颜色信息
    primary_color = outfit.get('主色', {})
    primary_name = primary_color.get('名称', 'N/A')
    primary_hex = primary_color.get('Hex', 'N/A')
    primary_meaning = primary_color.get('寓意', '')
    print(f"\n  🎨 主色调: {primary_name} (#{primary_hex})")
    if primary_meaning:
        print(f"     寓意: {primary_meaning}")
    
    # 配色信息
    matching_colors = outfit.get('配色', [])
    if matching_colors:
        color_names = [c.get('名称', 'N/A') for c in matching_colors]
        print(f"  🎨 配  色: {', '.join(color_names)}")
    
    # 服装单品
    clothing_items = outfit.get('服装单品', {})
    if clothing_items:
        print(f"\n  👔 服装单品:")
        for category, item in clothing_items.items():
            if item:  # 只显示非空的单品
                print(f"     • {category}: {item}")
    
    # 适合场合
    suitable_occasions = outfit.get('适合场合', [])
    if suitable_occasions:
        if isinstance(suitable_occasions, list):
            print(f"\n  👥 适合场合: {', '.join(suitable_occasions)}")
        else:
            print(f"\n  👥 适合场合: {suitable_occasions}")
    
    # 穿搭建议
    outfit_suggestion = outfit.get('穿搭建议', '')
    if outfit_suggestion:
        print(f"\n  💡 穿搭建议:")
        print(f"     {outfit_suggestion}")
    
    # 温度建议
    temp_advice = outfit.get('温度建议', '')
    if temp_advice:
        print(f"\n  🌡️ 温度提示: {temp_advice}")
    
    # 推荐指数
    score = outfit.get('推荐指数', 0)
    stars = '⭐' * int(round(score * 5))
    print(f"\n  📊 推荐指数: {score:.0%} ({stars})")


def main():
    # 确保目录存在
    ensure_directories()
    
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("启动运势助手...")
    
    try:
        # 显示欢迎信息
        display_welcome()
        
        # 初始化各模块
        with PerformanceMonitor("模块初始化"):
            user_info_module = UserInfoModule()
            huangli_module = HuangliModule()
            weather_module = WeatherModule()
            lucky_color_module = LuckyColorModule()
            outfit_module = OutfitRecommendationModule()
            
            # 调用初始化方法
            user_info_module.initialize()
            huangli_module.initialize()
            weather_module.initialize()
            lucky_color_module.initialize()
            outfit_module.initialize()
        
        # 收集用户信息
        with PerformanceMonitor("用户信息收集"):
            user_data = user_info_module.collect_user_info_interactive()
            logger.info(f"用户信息收集完成: {user_data.get('姓名', '未知')}")
        
        # 获取用户偏好和城市
        user_preferences = user_info_module.get_user_preferences()
        user_city = user_data.get('城市', '北京')
        user_name = user_data.get('姓名', '用户')
        
        # 获取当前日期
        today = datetime.now()
        logger.info(f"当前日期: {today.strftime('%Y-%m-%d')}")
        
        # 获取黄历信息
        with PerformanceMonitor("黄历数据获取"):
            huangli_data = huangli_module.get_huangli(today)
            logger.info(f"获取黄历信息成功")
        
        # 获取天气信息（使用用户选择的城市）
        with PerformanceMonitor("天气数据获取"):
            weather_data = weather_module.get_weather(user_city)
            logger.info(f"获取{user_city}天气信息成功: {weather_data.get('天气', 'N/A')}")
        
        # 获取幸运色（结合用户生肖等信息）
        with PerformanceMonitor("幸运色计算"):
            # 可以根据用户生肖调整幸运色，这里先使用基础版本
            lucky_colors = lucky_color_module.get_lucky_colors(huangli_data, weather_data)
            logger.info(f"今日幸运色: {', '.join([c['名称'] for c in lucky_colors])}")
        
        # 获取穿搭推荐（传入用户偏好）
        with PerformanceMonitor("穿搭推荐计算"):
            outfit_recommendations = outfit_module.get_recommendations(
                huangli_data, weather_data, lucky_colors, user_preferences
            )
            logger.info(f"生成穿搭推荐成功: {len(outfit_recommendations)} 套")
        
        # 输出最终结果
        print("\n" + "="*60)
        print(f"【{user_name}的专属运势 - {today.strftime('%Y年%m月%d日 %A')}】")
        print("="*60)
        
        # 显示用户个人信息摘要
        print("\n【个人信息】")
        print(f"  姓名: {user_data.get('姓名', 'N/A')}")
        print(f"  性别: {user_data.get('性别', 'N/A')}")
        print(f"  生肖: {user_data.get('生肖', 'N/A')}")
        print(f"  星座: {user_data.get('星座', 'N/A')}")
        print(f"  城市: {user_data.get('城市', 'N/A')}")
        
        # 黄历信息
        print("\n【今日黄历】")
        print(f"  农历: {huangli_data.get('农历', 'N/A')}")
        print(f"  干支: {huangli_data.get('干支', 'N/A')}")
        print(f"  五行: {huangli_data.get('五行', 'N/A')}")
        print(f"  宜: {huangli_data.get('宜', 'N/A')}")
        print(f"  忌: {huangli_data.get('忌', 'N/A')}")
        print(f"  冲煞: {huangli_data.get('冲煞', 'N/A')}")
        print(f"  幸运方位: {huangli_data.get('幸运方位', 'N/A')}")
        
        # 天气信息
        print("\n【今日天气】")
        print(f"  城市: {weather_data.get('城市', 'N/A')}")
        print(f"  天气: {weather_data.get('天气', 'N/A')}")
        print(f"  温度: {weather_data.get('温度', 'N/A')}")
        print(f"  湿度: {weather_data.get('湿度', 'N/A')}")
        print(f"  风向: {weather_data.get('风向', 'N/A')} {weather_data.get('风力', '')}")
        print(f"  紫外线: {weather_data.get('紫外线强度', 'N/A')}")
        print(f"  天气描述: {weather_data.get('天气描述', 'N/A')}")
        
        # 幸运色
        print("\n【今日幸运色】")
        for i, color in enumerate(lucky_colors[:5], 1):  # 只显示前5个
            name = color.get('名称', 'N/A')
            hex_color = color.get('Hex', 'N/A')
            meaning = color.get('寓意', '')
            source = color.get('来源', '')
            source_tag = f" [{source}]" if source else ""
            print(f"  {i}. {name} (#{hex_color}){source_tag}")
            if meaning:
                print(f"     寓意: {meaning}")
        
        # 穿搭推荐
        print("\n【穿搭推荐】")
        if outfit_recommendations:
            for i, outfit in enumerate(outfit_recommendations, 1):
                display_outfit_recommendation(outfit, i)
        else:
            print("  暂无穿搭推荐，请检查天气和温度设置。")
        
        print("\n" + "="*60)
        print("     🌟 祝您今天运势亨通，穿搭得体！ 🌟")
        print("="*60 + "\n")
        
        logger.info("运势助手运行完成")
        
    except Exception as e:
        ErrorHandler.handle_exception(e, "主程序运行")
        logger.error(f"程序运行出错: {str(e)}")
        print(f"\n程序运行出错: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
