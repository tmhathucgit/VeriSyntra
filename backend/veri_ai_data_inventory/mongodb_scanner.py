"""
MongoDBScanner implementation for veri-ai-data-inventory
Uses dynamic configuration from DatabaseConfig, EncodingConfig, ScanConfig
Vietnamese UTF-8 support and PDPL compliance
"""
try:
    from .config import DatabaseConfig, EncodingConfig, ScanConfig
except ImportError:
    from config.constants import DatabaseConfig, EncodingConfig, ScanConfig

from pymongo import MongoClient
from typing import List, Any

class MongoDBScanner:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = DatabaseConfig.MONGODB_DEFAULT_PORT, auth_source: str = DatabaseConfig.MONGODB_DEFAULT_AUTH_SOURCE):
        self.client = MongoClient(
            host=host,
            port=port,
            username=user,
            password=password,
            authSource=auth_source,
            unicode_decode_error_handler=EncodingConfig.MONGODB_UNICODE_ERROR_HANDLER
        )
        self.db = self.client[database]

    def extract_sample_data(self, collection_name: str, field_name: str, limit: int = ScanConfig.DEFAULT_SAMPLE_SIZE) -> List[Any]:
        """Extracts sample data from a collection field using dynamic config."""
        cursor = self.db[collection_name].find({}, {field_name: 1}).limit(limit)
        return [doc.get(field_name) for doc in cursor]

    def get_top_values(self, collection_name: str, field_name: str, top_n: int = ScanConfig.TOP_VALUES_COUNT) -> List[Any]:
        """Gets top N values from a field using dynamic config."""
        pipeline = [
            {"$group": {"_id": f"${field_name}", "freq": {"$sum": 1}}},
            {"$sort": {"freq": -1}},
            {"$limit": top_n}
        ]
        return list(self.db[collection_name].aggregate(pipeline))

    def close(self):
        self.client.close()
