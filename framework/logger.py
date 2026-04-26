# 日志系统模块
import logging
import logging.config
import os
from datetime import datetime
from pathlib import Path

from config import LOG_CONFIG, BASE_DIR


def setup_logging():
    """初始化日志系统"""
    # 确保日志目录存在
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 配置日志系统
    logging.config.dictConfig(LOG_CONFIG)
    
    # 记录启动日志
    logger = logging.getLogger(__name__)
    logger.info("日志系统初始化完成")


def get_logger(name: str = None) -> logging.Logger:
    """获取日志记录器
    
    Args:
        name: 日志记录器名称，通常使用 __name__
        
    Returns:
        配置好的日志记录器
    """
    return logging.getLogger(name or __name__)


class PerformanceLogger:
    """性能日志记录器"""
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.logger = get_logger(module_name)
    
    def log_operation(self, operation: str, start_time: float, end_time: float,
                      success: bool = True, details: str = None):
        """记录操作性能
        
        Args:
            operation: 操作名称
            start_time: 开始时间戳
            end_time: 结束时间戳
            success: 操作是否成功
            details: 详细信息
        """
        duration = end_time - start_time
        status = "成功" if success else "失败"
        log_msg = f"[{self.module_name}] 操作: {operation}, 耗时: {duration:.4f}秒, 状态: {status}"
        
        if details:
            log_msg += f", 详情: {details}"
        
        if success:
            self.logger.info(log_msg)
        else:
            self.logger.warning(log_msg)
