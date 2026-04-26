# 框架模块初始化
from .logger import setup_logging, get_logger
from .performance_monitor import PerformanceMonitor, get_performance_stats, clear_performance_stats
from .error_handler import ErrorHandler, AppException, ModuleException, DataSourceException
from .base_module import BaseModule, ModuleStatus
from .module_interface import IModule, IHuangliModule, IWeatherModule, ILuckyColorModule, IOutfitRecommendationModule

__all__ = [
    'setup_logging', 'get_logger',
    'PerformanceMonitor', 'get_performance_stats', 'clear_performance_stats',
    'ErrorHandler', 'AppException', 'ModuleException', 'DataSourceException',
    'BaseModule', 'ModuleStatus',
    'IModule', 'IHuangliModule', 'IWeatherModule', 'ILuckyColorModule', 'IOutfitRecommendationModule'
]
