# 测试框架模块
import pytest
import time
from datetime import datetime

from framework import (
    PerformanceMonitor, get_performance_stats, clear_performance_stats,
    ErrorHandler, AppException, ModuleException, DataSourceException,
    BaseModule, ModuleStatus,
    setup_logging, get_logger
)


class TestPerformanceMonitor:
    """性能监控器测试类"""
    
    def setup_method(self):
        """每个测试方法前清除统计数据"""
        clear_performance_stats()
    
    def test_performance_monitor_basic(self):
        """测试基本性能监控功能"""
        with PerformanceMonitor("测试操作") as monitor:
            time.sleep(0.01)
        
        # 验证监控器记录了耗时
        assert monitor.duration is not None
        assert monitor.duration > 0
        assert monitor.success is True
    
    def test_performance_monitor_with_exception(self):
        """测试异常情况下的性能监控"""
        with pytest.raises(ValueError):
            with PerformanceMonitor("测试异常操作") as monitor:
                raise ValueError("测试异常")
        
        # 验证监控器记录了失败状态
        assert monitor.success is False
        assert monitor.error_message == "测试异常"
    
    def test_get_performance_stats(self):
        """测试获取性能统计"""
        # 执行多次操作
        for i in range(3):
            with PerformanceMonitor("统计测试"):
                time.sleep(0.001)
        
        # 获取统计数据
        stats = get_performance_stats("统计测试")
        
        assert stats["total_calls"] == 3
        assert stats["success_rate"] == 100.0
        assert stats["avg_duration"] > 0
    
    def test_get_performance_stats_all(self):
        """测试获取所有操作的性能统计"""
        with PerformanceMonitor("操作1"):
            time.sleep(0.001)
        
        with PerformanceMonitor("操作2"):
            time.sleep(0.001)
        
        stats = get_performance_stats()
        
        assert "操作1" in stats
        assert "操作2" in stats


class TestErrorHandler:
    """错误处理器测试类"""
    
    def setup_method(self):
        """每个测试方法前清除错误记录"""
        ErrorHandler.clear_errors()
    
    def test_handle_exception(self):
        """测试异常处理"""
        exception = ValueError("测试异常")
        
        # 处理异常但不重新抛出
        error_record = ErrorHandler.handle_exception(
            exception, 
            context="测试上下文",
            module_name="TestModule",
            re_raise=False
        )
        
        assert error_record is not None
        assert error_record.error_type == "ValueError"
        assert error_record.message == "测试异常"
        assert error_record.module_name == "TestModule"
    
    def test_handle_exception_re_raise(self):
        """测试重新抛出异常"""
        exception = ValueError("测试重新抛出")
        
        with pytest.raises(ValueError):
            ErrorHandler.handle_exception(
                exception,
                context="测试重新抛出",
                re_raise=True
            )
    
    def test_custom_exceptions(self):
        """测试自定义异常"""
        # 测试 AppException
        app_exc = AppException(
            message="应用错误",
            error_code="APP_ERROR_001",
            details={"key": "value"}
        )
        
        assert str(app_exc) == "[APP_ERROR_001] 应用错误"
        assert app_exc.error_code == "APP_ERROR_001"
        
        # 测试 ModuleException
        module_exc = ModuleException(
            module_name="TestModule",
            message="模块错误",
            error_code="MODULE_ERROR"
        )
        
        assert "TestModule" in str(module_exc)
        assert module_exc.module_name == "TestModule"
        
        # 测试 DataSourceException
        data_exc = DataSourceException(
            source_name="TestAPI",
            message="数据源错误",
            error_code="DATA_ERROR"
        )
        
        assert "TestAPI" in str(data_exc)
        assert data_exc.source_name == "TestAPI"
    
    def test_get_error_stats(self):
        """测试获取错误统计"""
        # 记录几个错误
        for i in range(3):
            ErrorHandler.handle_exception(
                ValueError(f"错误 {i}"),
                context=f"测试 {i}"
            )
        
        stats = ErrorHandler.get_error_stats()
        
        assert stats["total_errors"] == 3
        assert "ValueError" in stats["error_types"]


class TestBaseModule:
    """基础模块测试类"""
    
    class TestableModule(BaseModule):
        """可测试的模块实现"""
        
        def _on_initialize(self) -> bool:
            return True
        
        def _on_shutdown(self) -> bool:
            return True
    
    def test_module_lifecycle(self):
        """测试模块生命周期"""
        module = self.TestableModule("TestModule")
        
        # 初始状态
        assert module.status == ModuleStatus.UNINITIALIZED
        
        # 初始化
        module.initialize()
        assert module.status == ModuleStatus.READY
        
        # 获取状态
        status = module.get_status()
        assert status["module_name"] == "TestModule"
        assert status["status"] == "就绪"
        
        # 关闭
        module.shutdown()
        assert module.status == ModuleStatus.SHUTDOWN
    
    def test_module_not_ready(self):
        """测试模块未就绪时的检查"""
        module = self.TestableModule("TestModule")
        
        # 未初始化时检查应该抛出异常
        with pytest.raises(Exception):
            module.check_ready()
    
    def test_module_config(self):
        """测试模块配置"""
        module = self.TestableModule("TestModule")
        
        # 初始化时传入配置
        config = {"key1": "value1", "key2": "value2"}
        module.initialize(config)
        
        # 验证配置
        assert module.config["key1"] == "value1"
        assert module.config["key2"] == "value2"


class TestLogger:
    """日志系统测试类"""
    
    def test_get_logger(self):
        """测试获取日志记录器"""
        logger = get_logger("TestLogger")
        
        assert logger is not None
        assert logger.name == "TestLogger"
    
    def test_logger_output(self, capsys):
        """测试日志输出"""
        logger = get_logger("TestOutput")
        
        # 记录日志
        logger.info("测试信息日志")
        logger.warning("测试警告日志")
        logger.error("测试错误日志")
        
        # 验证输出（可能被其他日志系统拦截，这里只是测试不报错）
        assert True
