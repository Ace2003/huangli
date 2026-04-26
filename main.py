# 运势助手主入口
import logging
import logging.config
import os
from datetime import datetime
from pathlib import Path

from config import LOG_CONFIG, BASE_DIR
from framework import PerformanceMonitor, ErrorHandler, setup_logging
from modules import HuangliModule, WeatherModule, LuckyColorModule, OutfitRecommendationModule


def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        BASE_DIR / 'logs',
        BASE_DIR / 'data',
        BASE_DIR / 'cache'
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def main():
    # 确保目录存在
    ensure_directories()
    
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("启动运势助手...")
    
    try:
        # 初始化各模块
        with PerformanceMonitor("模块初始化"):
            huangli_module = HuangliModule()
            weather_module = WeatherModule()
            lucky_color_module = LuckyColorModule()
            outfit_module = OutfitRecommendationModule()
            
            # 调用初始化方法
            huangli_module.initialize()
            weather_module.initialize()
            lucky_color_module.initialize()
            outfit_module.initialize()
        
        # 获取当前日期
        today = datetime.now()
        logger.info(f"当前日期: {today.strftime('%Y-%m-%d')}")
        
        # 获取黄历信息
        with PerformanceMonitor("黄历数据获取"):
            huangli_data = huangli_module.get_huangli(today)
            logger.info(f"获取黄历信息成功: {huangli_data.get('宜忌', 'N/A')}")
        
        # 获取天气信息
        with PerformanceMonitor("天气数据获取"):
            weather_data = weather_module.get_weather('北京')  # 默认城市
            logger.info(f"获取天气信息成功: {weather_data.get('天气', 'N/A')}")
        
        # 获取幸运色
        with PerformanceMonitor("幸运色计算"):
            lucky_colors = lucky_color_module.get_lucky_colors(huangli_data)
            logger.info(f"今日幸运色: {', '.join([c['名称'] for c in lucky_colors])}")
        
        # 获取穿搭推荐
        with PerformanceMonitor("穿搭推荐计算"):
            outfit_recommendations = outfit_module.get_recommendations(
                huangli_data, weather_data, lucky_colors
            )
            logger.info(f"生成穿搭推荐成功: {len(outfit_recommendations)} 套")
        
        # 输出结果
        print("\n" + "="*60)
        print(f"【运势助手 - {today.strftime('%Y年%m月%d日 %A')}】")
        print("="*60)
        
        print("\n【黄历信息】")
        print(f"  农历: {huangli_data.get('农历', 'N/A')}")
        print(f"  生肖: {huangli_data.get('生肖', 'N/A')}")
        print(f"  宜: {huangli_data.get('宜', 'N/A')}")
        print(f"  忌: {huangli_data.get('忌', 'N/A')}")
        print(f"  冲煞: {huangli_data.get('冲煞', 'N/A')}")
        
        print("\n【天气信息】")
        print(f"  城市: {weather_data.get('城市', 'N/A')}")
        print(f"  天气: {weather_data.get('天气', 'N/A')}")
        print(f"  温度: {weather_data.get('温度', 'N/A')}")
        print(f"  湿度: {weather_data.get('湿度', 'N/A')}")
        print(f"  风向: {weather_data.get('风向', 'N/A')}")
        
        print("\n【今日幸运色】")
        for color in lucky_colors:
            print(f"  ● {color['名称']} (#{color['Hex']}) - {color['寓意']}")
        
        print("\n【穿搭推荐】")
        for i, outfit in enumerate(outfit_recommendations, 1):
            print(f"\n  推荐方案 {i}:")
            print(f"    风格: {outfit.get('风格', 'N/A')}")
            print(f"    主色: {outfit.get('主色', {}).get('名称', 'N/A')}")
            print(f"    配色: {', '.join([c.get('名称', 'N/A') for c in outfit.get('配色', [])])}")
            print(f"    适合场合: {outfit.get('适合场合', 'N/A')}")
            print(f"    穿搭建议: {outfit.get('穿搭建议', 'N/A')}")
        
        print("\n" + "="*60)
        logger.info("运势助手运行完成")
        
    except Exception as e:
        ErrorHandler.handle_exception(e, "主程序运行")
        logger.error(f"程序运行出错: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
