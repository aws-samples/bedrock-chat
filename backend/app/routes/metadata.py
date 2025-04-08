from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, List, Optional
from pydantic import BaseModel, Json

from ..repositories.models.bot_metadata import BotMetadata, MetadataConfig, HierarchyMetadata, TagMetadata, AttributeMetadata
from ..services.metadata_service import MetadataService
from app.dependencies import get_current_user

router = APIRouter(prefix="/metadata", tags=["metadata"])
metadata_service = MetadataService()

# Request/Response models
class MetadataResponse(BaseModel):
    success: bool
    data: Optional[Dict] = None
    message: Optional[str] = None
    
class PaginatedResponse(MetadataResponse):
    last_evaluated_key: Optional[Dict] = None

# Config endpoints
@router.get("/config", response_model=MetadataResponse)
async def get_config(user=Depends(get_current_user)):
    """Get the metadata configuration"""
    try:
        config = await metadata_service.repository.get_config()
        return MetadataResponse(success=True, data=config.model_dump())
    except Exception as e:
        return MetadataResponse(success=False, message=str(e))

@router.post("/config", response_model=MetadataResponse)
async def update_config(config: MetadataConfig, user=Depends(get_current_user)):
    """Update the metadata configuration"""
    try:
        await metadata_service.update_config(config)
        return MetadataResponse(success=True, message="Config updated successfully")
    except Exception as e:
        return MetadataResponse(success=False, message=str(e))

# Bot Metadata endpoints
@router.get("/bot/{bot_id}", response_model=MetadataResponse)
async def get_bot_metadata(bot_id: str, user=Depends(get_current_user)):
    """Get metadata for a specific bot"""
    try:
        metadata = await metadata_service.get_bot_metadata(bot_id)
        return MetadataResponse(success=True, data=metadata.model_dump())
    except Exception as e:
        return MetadataResponse(success=False, message=str(e))

@router.post("/bot/{bot_id}", response_model=MetadataResponse)
async def update_bot_metadata(bot_id: str, metadata: BotMetadata, user=Depends(get_current_user)):
    """Update metadata for a specific bot"""
    try:
        await metadata_service.update_bot_metadata(bot_id, metadata)
        return MetadataResponse(success=True, message="Bot metadata updated successfully")
    except Exception as e:
        return MetadataResponse(success=False, message=str(e))

# Metadata values endpoints
@router.get("/values/hierarchy", response_model=MetadataResponse)
async def get_hierarchy_values(user=Depends(get_current_user)):
    """Get all hierarchy values"""
    try:
        values = await metadata_service.get_hierarchy_values()
        return MetadataResponse(success=True, data=values)
    except Exception as e:
        return MetadataResponse(success=False, message=str(e))

@router.get("/values/tags", response_model=MetadataResponse)
async def get_tag_values(user=Depends(get_current_user)):
    """Get all tag values"""
    try:
        values = await metadata_service.get_tag_values()
        return MetadataResponse(success=True, data=values)
    except Exception as e:
        return MetadataResponse(success=False, message=str(e))

@router.post("/values/hierarchy", response_model=MetadataResponse)
async def add_hierarchy_value(value: Dict, user=Depends(get_current_user)):
    """Add a new hierarchy value"""
    try:
        await metadata_service.add_hierarchy_value(value)
        return MetadataResponse(success=True, message="Hierarchy value added successfully")
    except Exception as e:
        return MetadataResponse(success=False, message=str(e))

@router.post("/values/tags", response_model=MetadataResponse)
async def add_tag_value(value: Dict, user=Depends(get_current_user)):
    """Add a new tag value"""
    try:
        await metadata_service.add_tag_value(value)
        return MetadataResponse(success=True, message="Tag value added successfully")
    except Exception as e:
        return MetadataResponse(success=False, message=str(e))

@router.delete("/values/hierarchy/{value_id}", response_model=MetadataResponse)
async def delete_hierarchy_value(value_id: str, user=Depends(get_current_user)):
    """Delete a hierarchy value"""
    try:
        await metadata_service.delete_hierarchy_value(value_id)
        return MetadataResponse(success=True, message="Hierarchy value deleted successfully")
    except Exception as e:
        return MetadataResponse(success=False, message=str(e))

@router.delete("/values/tags/{value_id}", response_model=MetadataResponse)
async def delete_tag_value(value_id: str, user=Depends(get_current_user)):
    """Delete a tag value"""
    try:
        await metadata_service.delete_tag_value(value_id)
        return MetadataResponse(success=True, message="Tag value deleted successfully")
    except Exception as e:
        return MetadataResponse(success=False, message=str(e))

# Search and analytics endpoints
@router.post("/search", response_model=PaginatedResponse)
async def search_bots(
    query: Dict, 
    limit: int = Query(50, ge=1, le=100),
    last_evaluated_key: Optional[str] = None,
    user=Depends(get_current_user)
):
    """Search for bots based on metadata criteria with pagination"""
    try:
        # Parse the last_evaluated_key from string if provided
        last_key_dict = None
        if last_evaluated_key:
            try:
                import json
                last_key_dict = json.loads(last_evaluated_key)
            except:
                raise ValueError("Invalid last_evaluated_key format")
        
        results = await metadata_service.search_bots(query, limit, last_key_dict)
        
        # Return paginated response
        return PaginatedResponse(
            success=True, 
            data=results.get('items', []),
            last_evaluated_key=results.get('last_evaluated_key')
        )
    except Exception as e:
        return PaginatedResponse(success=False, message=str(e))

@router.get("/stats", response_model=MetadataResponse)
async def get_metadata_stats(user=Depends(get_current_user)):
    """Get statistics about metadata usage"""
    try:
        stats = await metadata_service.get_metadata_stats()
        return MetadataResponse(success=True, data=stats)
    except Exception as e:
        return MetadataResponse(success=False, message=str(e)) 