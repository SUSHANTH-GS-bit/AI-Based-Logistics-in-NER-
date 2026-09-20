"""
Chat Router for SIH26002 - NER Smart Logistics Platform.

Exposes the POST /api/chat endpoint for the Logistics AI Assistant chatbot.
Follows the same APIRouter pattern as gis_router.py and sync_router.py.
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, status
from pydantic import BaseModel, Field

try:
    from backend.chat_service import chat_service
except ModuleNotFoundError:
    from chat_service import chat_service

# Create APIRouter for the chat endpoint
router = APIRouter(tags=["AI Chat Assistant"])


# ----------------------------------------------------
# Pydantic Schemas
# ----------------------------------------------------

class ChatRequest(BaseModel):
    """Request body for the AI chatbot endpoint."""
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The user's message or question for the Logistics AI Assistant.",
        example="Are there any high-risk routes in Manipur right now?"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "Optional logistics context from the frontend dashboard "
            "(e.g. current risk scores, active incidents, route details)."
        ),
        example={
            "current_page": "Route Planning",
            "active_incidents": 3,
            "route_risk_level": "HIGH"
        }
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "What does a HIGH risk level mean for my route?",
                "context": {
                    "current_page": "Route Planning",
                    "active_incidents": 3,
                    "route_risk_level": "HIGH"
                }
            }
        }
    }


class ChatResponse(BaseModel):
    """Response body from the AI chatbot endpoint."""
    reply: str = Field(
        ...,
        description="The AI-generated response to the user's message.",
        example="A HIGH risk level means there is a significant probability of landslide or road disruption..."
    )


# ----------------------------------------------------
# Endpoint
# ----------------------------------------------------

@router.post(
    "/api/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="AI Logistics Assistant Chat",
    description=(
        "Send a message to the AI Logistics Assistant. "
        "Returns an AI-generated response contextualised to NER logistics data. "
        "Optionally accepts a context object with current dashboard state to improve response quality."
    )
)
def chat_with_assistant(request: ChatRequest):
    """
    POST /api/chat

    Request:
        { "message": "string", "context": { ...optional... } }

    Response:
        { "reply": "string" }
    """
    result = chat_service.chat(
        message=request.message,
        context=request.context
    )
    return ChatResponse(reply=result["reply"])
