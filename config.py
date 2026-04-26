# 运势助手配置文件
import os
from pathlib import Path

# 项目基础路径
BASE_DIR = Path(__file__).parent.absolute()

# 日志配置
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'app.log'),
            'formatter': 'detailed',
            'mode': 'a'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

# 天气API配置
WEATHER_API = {
    'default_city': '北京',
    'timeout': 10,
    'retry_times': 3
}

# 黄历配置
HUANGLI_CONFIG = {
    'data_source': 'local',  # local, remote
    'cache_enabled': True,
    'cache_expire_hours': 24
}

# 穿搭推荐配置
OUTFIT_CONFIG = {
    'recommendation_count': 3,
    'consider_weather': True,
    'consider_lucky_color': True
}
