"""
MySQLScanner implementation for veri-ai-data-inventory
Uses dynamic configuration from ScanConfig, DatabaseConfig, EncodingConfig
Vietnamese UTF-8 support and PDPL compliance
"""
try:
    from .config import ScanConfig, DatabaseConfig, EncodingConfig
except ImportError:
    from config.constants import ScanConfig, DatabaseConfig, EncodingConfig

import pymysql
from typing import List, Any

class MySQLScanner:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = DatabaseConfig.MYSQL_DEFAULT_PORT):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            charset=EncodingConfig.MYSQL_CHARSET
        )

    def extract_sample_data(self, table_name: str, column_name: str, limit: int = ScanConfig.DEFAULT_SAMPLE_SIZE):
        """Extracts sample data from a table column using dynamic config."""
        query = f"SELECT {column_name} FROM {table_name} LIMIT %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (limit,))
            return [row[0] for row in cursor.fetchall()]

    def get_top_values(self, table_name: str, column_name: str, top_n: int = ScanConfig.TOP_VALUES_COUNT):
        """Gets top N values from a column using dynamic config."""
        query = f"SELECT {column_name}, COUNT(*) as freq FROM {table_name} GROUP BY {column_name} ORDER BY freq DESC LIMIT %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (top_n,))
            return cursor.fetchall()

    def close(self):
        self.connection.close()
