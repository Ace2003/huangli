# 错误处理模块
import traceback
import logging
from typing import Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


class AppException(Exception):
    """应用程序基础异常类
    
    所有自定义异常都应该继承自此类
    """
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        """初始化异常
        
        Args:
            message: 异常消息
            error_code: 错误代码
            details: 详细信息字典
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def __str__(self):
        return f"[{self.error_code}] {self.message}"


class ModuleException(AppException):
    """模块异常类
    
    用于模块内部错误
    """
    
    def __init__(self, module_name: str, message: str, error_code: str = "MODULE_ERROR", details: dict = None):
        """初始化模块异常
        
        Args:
            module_name: 模块名称
            message: 异常消息
            error_code: 错误代码
            details: 详细信息字典
        """
        full_message = f"[{module_name}] {message}"
        super().__init__(full_message, error_code, details)
        self.module_name = module_name


class DataSourceException(AppException):
    """数据源异常类
    
    用于数据源获取失败等情况
    """
    
    def __init__(self, source_name: str, message: str, error_code: str = "DATA_SOURCE_ERROR", details: dict = None):
        """初始化数据源异常
        
        Args:
            source_name: 数据源名称
            message: 异常消息
            error_code: 错误代码
            details: 详细信息字典
        """
        full_message = f"数据源 [{source_name}] 错误: {message}"
        super().__init__(full_message, error_code, details)
        self.source_name = source_name


class ConfigurationException(AppException):
    """配置异常类
    
    用于配置错误
    """
    
    def __init__(self, config_key: str, message: str, error_code: str = "CONFIG_ERROR", details: dict = None):
        """初始化配置异常
        
        Args:
            config_key: 配置键名
            message: 异常消息
            error_code: 错误代码
            details: 详细信息字典
        """
        full_message = f"配置 [{config_key}] 错误: {message}"
        super().__init__(full_message, error_code, details)
        self.config_key = config_key


@dataclass
class ErrorRecord:
    """错误记录数据类"""
    error_type: str
    message: str
    error_code: str
    timestamp: datetime
    traceback: str = ""
    module_name: str = None
    source_name: str = None
    handled: bool = False


class ErrorHandler:
    """错误处理器
    
    提供统一的错误处理机制
    """
    
    # 错误记录存储
    _error_records = []
    _max_records = 1000
    
    @classmethod
    def handle_exception(cls, exception: Exception, context: str = None, 
                        module_name: str = None, re_raise: bool = False) -> ErrorRecord:
        """处理异常
        
        Args:
            exception: 异常对象
            context: 上下文信息，描述异常发生的场景
            module_name: 模块名称
            re_raise: 是否重新抛出异常
            
        Returns:
            错误记录对象
        """
        # 获取异常详细信息
        error_type = type(exception).__name__
        message = str(exception)
        traceback_str = traceback.format_exc()
        
        # 确定错误代码
        if isinstance(exception, AppException):
            error_code = exception.error_code
        else:
            error_code = "UNEXPECTED_ERROR"
        
        # 创建错误记录
        error_record = ErrorRecord(
            error_type=error_type,
            message=message,
            error_code=error_code,
            timestamp=datetime.now(),
            traceback=traceback_str,
            module_name=module_name
        )
        
        # 记录错误
        cls._record_error(error_record)
        
        # 记录日志
        log_message = f"异常发生: {message}"
        if context:
            log_message = f"[{context}] {log_message}"
        
        logger.error(log_message)
        logger.debug(f"异常详情:\n{traceback_str}")
        
        # 重新抛出异常
        if re_raise:
            raise exception
        
        return error_record
    
    @classmethod
    def _record_error(cls, error_record: ErrorRecord):
        """记录错误到存储"""
        cls._error_records.append(error_record)
        
        # 限制记录数量
        if len(cls._error_records) > cls._max_records:
            cls._error_records = cls._error_records[-cls._max_records:]
    
    @classmethod
    def get_error_stats(cls) -> dict:
        """获取错误统计信息
        
        Returns:
            包含错误统计信息的字典
        """
        if not cls._error_records:
            return {
                "total_errors": 0,
                "error_types": {},
                "error_codes": {}
            }
        
        # 统计错误类型
        error_types = {}
        error_codes = {}
        
        for record in cls._error_records:
            # 统计错误类型
            if record.error_type not in error_types:
                error_types[record.error_type] = 0
            error_types[record.error_type] += 1
            
            # 统计错误代码
            if record.error_code not in error_codes:
                error_codes[record.error_code] = 0
            error_codes[record.error_code] += 1
        
        return {
            "total_errors": len(cls._error_records),
            "error_types": error_types,
            "error_codes": error_codes,
            "recent_errors": [
                {
                    "type": r.error_type,
                    "message": r.message,
                    "code": r.error_code,
                    "timestamp": r.timestamp.isoformat()
                }
                for r in cls._error_records[-5:]  # 最近5个错误
            ]
        }
    
    @classmethod
    def clear_errors(cls):
        """清除所有错误记录"""
        cls._error_records.clear()


def safe_execute(func: Callable, *args, default_return: Any = None, 
                 context: str = None, module_name: str = None, **kwargs) -> Any:
    """安全执行函数
    
    封装函数调用，捕获并处理所有异常
    
    Args:
        func: 要执行的函数
        *args: 位置参数
        default_return: 异常时返回的默认值
        context: 上下文信息
        module_name: 模块名称
        **kwargs: 关键字参数
        
    Returns:
        函数执行结果或默认值
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        ErrorHandler.handle_exception(e, context, module_name)
        return default_return
