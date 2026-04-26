# 性能监控模块
import time
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceRecord:
    """性能记录数据类"""
    operation: str
    start_time: float
    end_time: float = 0.0
    duration: float = 0.0
    success: bool = True
    error_message: str = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    def calculate_duration(self):
        """计算耗时"""
        self.duration = self.end_time - self.start_time
        return self.duration


class PerformanceMonitor:
    """性能监控器
    
    用于监控代码块的执行时间和性能指标
    
    使用示例:
        with PerformanceMonitor("数据获取") as monitor:
            # 执行代码
            data = fetch_data()
        print(f"耗时: {monitor.duration:.4f}秒")
    """
    
    # 全局性能统计
    _stats: Dict[str, List[PerformanceRecord]] = {}
    _lock = threading.Lock()
    
    def __init__(self, operation: str, log_on_exit: bool = True):
        """初始化性能监控器
        
        Args:
            operation: 操作名称，用于标识监控的代码块
            log_on_exit: 是否在退出时记录日志
        """
        self.operation = operation
        self.log_on_exit = log_on_exit
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.success = True
        self.error_message = None
    
    def __enter__(self):
        """进入上下文管理器"""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        
        # 检查是否有异常
        if exc_type is not None:
            self.success = False
            self.error_message = str(exc_val)
            logger.warning(f"操作 [{self.operation}] 执行失败: {self.error_message}")
        
        # 记录性能数据
        self._record_performance()
        
        # 记录日志
        if self.log_on_exit:
            status = "成功" if self.success else "失败"
            logger.info(f"操作 [{self.operation}] 执行{status}, 耗时: {self.duration:.4f}秒")
        
        # 不抑制异常
        return False
    
    def _record_performance(self):
        """记录性能数据到全局统计"""
        record = PerformanceRecord(
            operation=self.operation,
            start_time=self.start_time,
            end_time=self.end_time,
            duration=self.duration,
            success=self.success,
            error_message=self.error_message
        )
        
        with self._lock:
            if self.operation not in self._stats:
                self._stats[self.operation] = []
            self._stats[self.operation].append(record)


def get_performance_stats(operation: str = None) -> Dict:
    """获取性能统计数据
    
    Args:
        operation: 操作名称，如果为None则返回所有操作的统计
        
    Returns:
        包含性能统计信息的字典
    """
    with PerformanceMonitor._lock:
        if operation:
            if operation not in PerformanceMonitor._stats:
                return {"error": f"操作 '{operation}' 不存在"}
            records = PerformanceMonitor._stats[operation]
            return _calculate_stats(records)
        else:
            all_stats = {}
            for op, records in PerformanceMonitor._stats.items():
                all_stats[op] = _calculate_stats(records)
            return all_stats


def _calculate_stats(records: List[PerformanceRecord]) -> Dict:
    """计算性能统计数据
    
    Args:
        records: 性能记录列表
        
    Returns:
        包含统计信息的字典
    """
    if not records:
        return {
            "total_calls": 0,
            "success_rate": 0.0,
            "avg_duration": 0.0,
            "min_duration": 0.0,
            "max_duration": 0.0
        }
    
    durations = [r.duration for r in records]
    success_count = sum(1 for r in records if r.success)
    
    return {
        "total_calls": len(records),
        "success_rate": success_count / len(records) * 100,
        "avg_duration": sum(durations) / len(durations),
        "min_duration": min(durations),
        "max_duration": max(durations)
    }


def clear_performance_stats(operation: str = None):
    """清除性能统计数据
    
    Args:
        operation: 操作名称，如果为None则清除所有统计
    """
    with PerformanceMonitor._lock:
        if operation:
            if operation in PerformanceMonitor._stats:
                del PerformanceMonitor._stats[operation]
        else:
            PerformanceMonitor._stats.clear()
