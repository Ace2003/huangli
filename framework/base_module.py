# 基础模块类
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional

from .performance_monitor import PerformanceMonitor
from .error_handler import ErrorHandler, ModuleException


class ModuleStatus(Enum):
    """模块状态枚举"""
    UNINITIALIZED = "未初始化"
    INITIALIZING = "初始化中"
    READY = "就绪"
    RUNNING = "运行中"
    ERROR = "错误"
    SHUTDOWN = "已关闭"


class BaseModule(ABC):
    """基础模块类
    
    所有功能模块的基类，提供统一的生命周期管理和性能监控
    """
    
    def __init__(self, module_name: str):
        """初始化基础模块
        
        Args:
            module_name: 模块名称
        """
        self.module_name = module_name
        self.status = ModuleStatus.UNINITIALIZED
        self.logger = logging.getLogger(module_name)
        self._config = {}
        self._metrics = {
            "total_calls": 0,
            "success_calls": 0,
            "failed_calls": 0,
            "total_duration": 0.0,
            "last_updated": None
        }
    
    @property
    def config(self) -> Dict[str, Any]:
        """获取模块配置"""
        return self._config.copy()
    
    def initialize(self, config: Dict[str, Any] = None) -> bool:
        """初始化模块
        
        Args:
            config: 模块配置字典
            
        Returns:
            初始化是否成功
        """
        self.logger.info(f"开始初始化模块: {self.module_name}")
        self.status = ModuleStatus.INITIALIZING
        
        try:
            # 合并配置
            if config:
                self._config.update(config)
            
            # 执行具体初始化
            with PerformanceMonitor(f"{self.module_name}.初始化"):
                success = self._on_initialize()
            
            if success:
                self.status = ModuleStatus.READY
                self.logger.info(f"模块 {self.module_name} 初始化成功")
                return True
            else:
                self.status = ModuleStatus.ERROR
                self.logger.error(f"模块 {self.module_name} 初始化失败")
                return False
                
        except Exception as e:
            self.status = ModuleStatus.ERROR
            ErrorHandler.handle_exception(e, f"模块 {self.module_name} 初始化", self.module_name)
            return False
    
    @abstractmethod
    def _on_initialize(self) -> bool:
        """执行具体的初始化逻辑
        
        子类必须实现此方法
        """
        pass
    
    def shutdown(self) -> bool:
        """关闭模块
        
        Returns:
            关闭是否成功
        """
        self.logger.info(f"开始关闭模块: {self.module_name}")
        
        try:
            with PerformanceMonitor(f"{self.module_name}.关闭"):
                success = self._on_shutdown()
            
            if success:
                self.status = ModuleStatus.SHUTDOWN
                self.logger.info(f"模块 {self.module_name} 已成功关闭")
                return True
            else:
                self.logger.warning(f"模块 {self.module_name} 关闭过程中出现问题")
                return False
                
        except Exception as e:
            ErrorHandler.handle_exception(e, f"模块 {self.module_name} 关闭", self.module_name)
            return False
    
    @abstractmethod
    def _on_shutdown(self) -> bool:
        """执行具体的关闭逻辑
        
        子类必须实现此方法
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """获取模块状态信息
        
        Returns:
            包含模块状态信息的字典
        """
        return {
            "module_name": self.module_name,
            "status": self.status.value,
            "total_calls": self._metrics["total_calls"],
            "success_rate": (self._metrics["success_calls"] / self._metrics["total_calls"] * 100) 
                           if self._metrics["total_calls"] > 0 else 0.0,
            "avg_duration": (self._metrics["total_duration"] / self._metrics["total_calls"]) 
                          if self._metrics["total_calls"] > 0 else 0.0,
            "last_updated": self._metrics["last_updated"].isoformat() 
                          if self._metrics["last_updated"] else None
        }
    
    def _update_metrics(self, success: bool, duration: float):
        """更新模块指标
        
        Args:
            success: 操作是否成功
            duration: 操作耗时
        """
        self._metrics["total_calls"] += 1
        if success:
            self._metrics["success_calls"] += 1
        else:
            self._metrics["failed_calls"] += 1
        self._metrics["total_duration"] += duration
        self._metrics["last_updated"] = datetime.now()
    
    def check_ready(self) -> bool:
        """检查模块是否就绪
        
        Returns:
            模块是否处于就绪状态
        """
        if self.status != ModuleStatus.READY:
            raise ModuleException(
                self.module_name,
                f"模块状态异常: 当前状态为 {self.status.value}，需要为 {ModuleStatus.READY.value}",
                "MODULE_NOT_READY"
            )
        return True
    
    def validate_config(self, required_keys: list) -> bool:
        """验证配置是否包含必需的键
        
        Args:
            required_keys: 必需的配置键列表
            
        Returns:
            配置是否有效
        """
        for key in required_keys:
            if key not in self._config:
                raise ModuleException(
                    self.module_name,
                    f"缺少必需的配置项: {key}",
                    "MISSING_CONFIG"
                )
        return True
