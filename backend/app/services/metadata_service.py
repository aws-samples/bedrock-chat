from typing import List, Dict, Optional
from app.repositories.models.bot_metadata import BotMetadata, MetadataConfig
from app.repositories.metadata_repository import MetadataRepository
from .metadata_validator import MetadataValidator, ValidationError
import asyncio
from functools import partial

class MetadataService:
    def __init__(self):
        self.repository = MetadataRepository()
        self._validator = None
        self._config = None
        
    async def get_validator(self) -> MetadataValidator:
        """Gets or creates a metadata validator with current config"""
        if not self._validator or not self._config:
            self._config = await self.repository.get_config()
            self._validator = MetadataValidator(config=self._config)
        return self._validator
        
    async def update_config(self, config: MetadataConfig):
        """Updates the metadata configuration"""
        await self.repository.save_config(config)
        self._config = config
        self._validator = MetadataValidator(config=config)
        
    async def get_bot_metadata(self, bot_id: str) -> BotMetadata:
        """Retrieves metadata for a specific bot"""
        return await self.repository.get_bot_metadata(bot_id)
        
    async def update_bot_metadata(self, bot_id: str, metadata: BotMetadata):
        """Updates metadata for a specific bot"""
        # Validate metadata before saving
        validator = await self.get_validator()
        await validator.validate(metadata)
        
        # Save validated metadata
        await self.repository.save_bot_metadata(bot_id, metadata)
        
    async def search_bots(self, query: Dict, limit: int = 50, last_evaluated_key: Optional[Dict] = None) -> Dict:
        """Searches for bots based on metadata criteria with pagination"""
        return await self.repository.search_metadata(query, limit, last_evaluated_key)
        
    async def get_hierarchy_values(self) -> List[Dict]:
        """Gets all hierarchy values"""
        return await self.repository.get_metadata_values('hierarchy')
        
    async def get_tag_values(self) -> List[Dict]:
        """Gets all tag values"""
        return await self.repository.get_metadata_values('tag')
        
    async def add_hierarchy_value(self, value: Dict):
        """Adds a new hierarchy value"""
        await self.repository.save_metadata_value('hierarchy', value)
        
    async def add_tag_value(self, value: Dict):
        """Adds a new tag value"""
        await self.repository.save_metadata_value('tag', value)
        
    async def delete_hierarchy_value(self, value_id: str):
        """Deletes a hierarchy value"""
        await self.repository.delete_metadata_value('hierarchy', value_id)
        
    async def delete_tag_value(self, value_id: str):
        """Deletes a tag value"""
        await self.repository.delete_metadata_value('tag', value_id)
        
    async def get_metadata_stats(self) -> Dict:
        """Gets statistics about metadata usage using pagination"""
        # Get all bots metadata using proper async pattern with pagination
        loop = asyncio.get_running_loop()
        
        stats = {
            'total_bots': 0,
            'hierarchy_usage': {},
            'tag_usage': {},
            'attribute_usage': {}
        }
        
        last_evaluated_key = None
        
        # Process bots in batches of 50 to avoid memory issues
        while True:
            def scan_table(last_key=None):
                params = {'Limit': 50}
                if last_key:
                    params['ExclusiveStartKey'] = last_key
                return self.repository.bot_metadata_table.scan(**params)
                
            response = await loop.run_in_executor(None, partial(scan_table, last_evaluated_key))
            bots = response.get('Items', [])
            
            # Update total bot count
            stats['total_bots'] += len(bots)
            
            # Process this batch of bots
            for bot in bots:
                # Hierarchy stats
                for h in bot.get('hierarchy', []):
                    level = h.get('level')
                    stats['hierarchy_usage'][level] = stats['hierarchy_usage'].get(level, 0) + 1
                    
                # Tag stats
                for t in bot.get('tags', []):
                    category = t.get('category')
                    stats['tag_usage'][category] = stats['tag_usage'].get(category, 0) + 1
                    
                # Attribute stats
                for a in bot.get('attributes', []):
                    key = a.get('key')
                    stats['attribute_usage'][key] = stats['attribute_usage'].get(key, 0) + 1
            
            # Check if there are more items to fetch
            last_evaluated_key = response.get('LastEvaluatedKey')
            if not last_evaluated_key:
                break
                
        return stats 