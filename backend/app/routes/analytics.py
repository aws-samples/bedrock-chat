"""Analytics routes."""

from datetime import datetime
import logging
import time
import os
from typing import Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from app.dependencies import check_permission, get_current_user
from app.routes.schemas.analytics import (
    AnalyticsDashboard,
    BotAnalytics,
    SummaryAnalyticsData,
    TopEntitiesData,
    TopicsData,
    DailyUsage,
    TopicAnalysis,
    UsagePerBot,
    UsagePerUser,
    MetadataAnalytics,
    FeedbackAnalytics,
    TokenAnalytics,
)
from app.user import User
from app.usecases import analytics_usecases

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)

@router.get(
    "/dashboard/summary",
    response_model=SummaryAnalyticsData,
    dependencies=[Depends(check_permission("view_analytics_dashboard"))]
)
async def get_analytics_dashboard_summary(
    from_date: Optional[str] = Query(None, description="Start date YYYYMMDD or YYYYMMDDHH"),
    to_date: Optional[str] = Query(None, description="End date YYYYMMDD or YYYYMMDDHH"),
    request: Request = Request,
):
    """Get summary dashboard metrics (summary, daily usage)."""
    current_user: User = request.state.current_user
    request_id = f"summary_{current_user.id}_{int(time.time())}"
    logger.info(f"[{request_id}] Analytics summary requested by user {current_user.id}")
    logger.info(f"[{request_id}] Request parameters: from={from_date}, to={to_date}")
    start_time = time.time()
    try:
        result = await analytics_usecases.get_summary_metrics(
            current_user=current_user,
            from_str=from_date,
            to_str=to_date
        )
        elapsed = time.time() - start_time
        logger.info(f"[{request_id}] Summary metrics retrieved successfully in {elapsed:.2f}s")
        return result
    except ValueError as e:
        logger.warning(f"[{request_id}] Value error getting summary metrics: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        logger.warning(f"[{request_id}] Permission error getting summary metrics: {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"[{request_id}] Exception in summary endpoint after {elapsed:.2f}s: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error retrieving summary analytics.")

@router.get(
    "/dashboard/top-entities",
    response_model=TopEntitiesData,
    dependencies=[Depends(check_permission("view_analytics_dashboard"))]
)
async def get_analytics_top_entities(
    from_date: Optional[str] = Query(None, description="Start date YYYYMMDD or YYYYMMDDHH"),
    to_date: Optional[str] = Query(None, description="End date YYYYMMDD or YYYYMMDDHH"),
    limit: int = Query(10, description="Number of entities", ge=1, le=50),
    request: Request = Request,
):
    """Get top users and bots."""
    current_user: User = request.state.current_user
    request_id = f"top_entities_{current_user.id}_{int(time.time())}"
    logger.info(f"[{request_id}] Analytics top entities requested by user {current_user.id}")
    logger.info(f"[{request_id}] Request parameters: from={from_date}, to={to_date}, limit={limit}")
    start_time = time.time()
    try:
        result = await analytics_usecases.get_top_entities_data(
            current_user=current_user,
            from_str=from_date,
            to_str=to_date,
            limit=limit
        )
        elapsed = time.time() - start_time
        logger.info(f"[{request_id}] Top entities retrieved successfully in {elapsed:.2f}s")
        return result
    except ValueError as e:
        logger.warning(f"[{request_id}] Value error getting top entities: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        logger.warning(f"[{request_id}] Permission error getting top entities: {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TimeoutError as e:
        logger.warning(f"[{request_id}] Timeout error getting top entities: {e}")
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Query timed out retrieving top entities.")
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"[{request_id}] Exception in top entities endpoint after {elapsed:.2f}s: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error retrieving top entities.")

@router.get(
    "/dashboard/topics",
    response_model=TopicsData,
    dependencies=[Depends(check_permission("view_analytics_dashboard"))]
)
async def get_analytics_dashboard_topics(
    from_date: Optional[str] = Query(None, description="Start date YYYYMMDD or YYYYMMDDHH"),
    to_date: Optional[str] = Query(None, description="End date YYYYMMDD or YYYYMMDDHH"),
    limit: int = Query(20, description="Max number of topics"),
    request: Request = Request,
):
    """Get topic analysis data."""
    current_user: User = request.state.current_user
    request_id = f"topics_{current_user.id}_{int(time.time())}"
    logger.info(f"[{request_id}] Analytics topics requested by user {current_user.id}")
    logger.info(f"[{request_id}] Request parameters: from={from_date}, to={to_date}, limit={limit}")
    start_time = time.time()
    try:
        result = await analytics_usecases.get_topics_data(
            current_user=current_user,
            from_str=from_date,
            to_str=to_date,
            limit=limit
        )
        elapsed = time.time() - start_time
        logger.info(f"[{request_id}] Topics analysis retrieved successfully in {elapsed:.2f}s")
        return result
    except ValueError as e:
        logger.warning(f"[{request_id}] Value error getting topics: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        logger.warning(f"[{request_id}] Permission error getting topics: {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TimeoutError as e:
        logger.warning(f"[{request_id}] Timeout error getting topics: {e}")
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Query timed out retrieving topics.")
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"[{request_id}] Exception in topics endpoint after {elapsed:.2f}s: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error retrieving topics analysis.")

@router.get(
    "/bot/{bot_id}",
    response_model=BotAnalytics,
    dependencies=[Depends(check_permission("view_bot_analytics"))]
)
async def get_bot_analytics_for_bot(
    bot_id: str,
    from_date: Optional[str] = Query(None, description="Start date YYYYMMDD or YYYYMMDDHH"),
    to_date: Optional[str] = Query(None, description="End date YYYYMMDD or YYYYMMDDHH"),
    request: Request = Request,
):
    """Get detailed analytics for a specific bot."""
    current_user: User = request.state.current_user
    request_id = f"bot_{bot_id}_{current_user.id}_{int(time.time())}"
    logger.info(f"[{request_id}] Analytics for bot {bot_id} requested by user {current_user.id}")
    logger.info(f"[{request_id}] Request parameters: from={from_date}, to={to_date}")
    start_time = time.time()
    try:
        result = await analytics_usecases.get_bot_analytics(
            current_user=current_user,
            bot_id=bot_id,
            from_str=from_date,
            to_str=to_date
        )
        elapsed = time.time() - start_time
        logger.info(f"[{request_id}] Bot analytics for {bot_id} retrieved successfully in {elapsed:.2f}s")
        return result
    except ValueError as e:
        logger.warning(f"[{request_id}] Value error getting analytics for bot {bot_id}: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        logger.warning(f"[{request_id}] Permission error getting analytics for bot {bot_id}: {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TimeoutError as e:
        logger.warning(f"[{request_id}] Timeout error getting bot analytics {bot_id}: {e}")
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"Query timed out retrieving analytics for bot {bot_id}.")
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"[{request_id}] Exception in bot analytics endpoint for {bot_id} after {elapsed:.2f}s: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error retrieving analytics for bot {bot_id}.") 