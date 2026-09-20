"""
Chat Service for SIH26002 - NER Smart Logistics Platform.

Provides a logistics-domain chatbot with an offline fallback.
The Gemini integration can be restored later when API access is available.
"""

import os
from typing import Optional, Any


class ChatService:
    """
    AI chat service for logistics-domain questions.

    When Gemini is available, it can be used.
    When Gemini is unavailable, the service provides an offline
    logistics assistant response.
    """

    SYSTEM_PROMPT = """You are the Logistics AI Assistant for the ResQ Byte platform.

You help users with:
- Route planning and optimization in the North Eastern Region of India
- Landslide and road disruption risk
- Vehicle GPS tracking and fleet management
- Incident reporting
- Hospitals, fuel stations, bridges, warehouses and settlements
- Offline GPS synchronization
- Logistics analytics and risk scores

Be concise, informative and practical.
"""

    def __init__(self):
        self.client: Optional[Any] = None
        self.model_name = "gemini-2.0-flash"
        self._initialized = False
        self._init_error = None

        self._try_initialize()

    def _try_initialize(self):
        """Try to initialize Gemini if available."""

        api_key = os.getenv("GEMINI_API_KEY", "").strip()

        if not api_key:
            self._init_error = "Gemini API key is not available."
            return

        try:
            from google import genai

            self.client = genai.Client(api_key=api_key)
            self._initialized = True

        except ImportError:
            self._init_error = "Gemini package is not installed."

        except Exception as e:
            self._init_error = f"Gemini initialization failed: {e}"

    def _offline_response(self, message: str) -> str:
        """
        Provide a useful response without requiring an AI API.
        """

        text = message.lower().strip()

        if any(word in text for word in ["hello", "hi", "hey"]):
            return (
                "Hello! I'm your NER Logistics Assistant. "
                "I can help with route planning, risk assessment, "
                "vehicle tracking, incidents and accessibility."
            )

        if "route" in text or "routing" in text:
            return (
                "For route planning, consider distance, road conditions, "
                "rainfall, landslide risk, traffic and accessibility. "
                "The safest route may not always be the shortest route."
            )

        if "landslide" in text:
            return (
                "Landslide risk can be assessed using factors such as "
                "rainfall, terrain slope and previous landslide history. "
                "High-risk roads should be monitored before dispatching vehicles."
            )

        if "risk" in text:
            return (
                "Logistics risk can include landslides, heavy rainfall, "
                "road disruption and accessibility problems. "
                "Risk scores can help prioritize safer routes."
            )

        if "vehicle" in text or "tracking" in text or "fleet" in text:
            return (
                "Vehicle tracking can use GPS information to monitor "
                "vehicle location, routes and fleet activity. "
                "This can help identify delays and route deviations."
            )

        if "hospital" in text:
            return (
                "For accessibility planning, nearby hospitals can be "
                "considered when evaluating routes and emergency logistics."
            )

        if "fuel" in text:
            return (
                "Fuel stations are important accessibility points for "
                "route planning, especially in areas with long travel distances."
            )

        if "incident" in text or "accident" in text:
            return (
                "Incidents can be reported and monitored so logistics "
                "teams can identify affected routes and adjust operations."
            )

        if "weather" in text or "rain" in text:
            return (
                "Heavy rainfall can affect road accessibility and increase "
                "the risk of landslides and disruptions. Check current "
                "weather and road conditions before dispatching vehicles."
            )

        return (
            "I can help with NER logistics, route planning, landslide risks, "
            "vehicle tracking, incidents and accessibility. "
            "Try asking something like: "
            "\"How can I optimize a delivery route?\""
        )

    def chat(self, message: str, context: dict | None = None) -> dict:
        """
        Process a chatbot message.

        Uses Gemini when available.
        Otherwise uses the offline logistics assistant.
        """

        if not message or not message.strip():
            return {
                "reply": "Please enter a message so I can help you.",
                "status": "EMPTY"
            }

        # If Gemini is unavailable, use offline mode.
        if not self._initialized or self.client is None:
            return {
                "reply": self._offline_response(message),
                "status": "OFFLINE_FALLBACK"
            }

        # Build prompt with optional dashboard context.
        prompt = message.strip()

        if context:
            context_lines = []

            for key, value in context.items():
                if value:
                    context_lines.append(f"- {key}: {value}")

            if context_lines:
                context_block = "\n".join(context_lines)

                prompt = (
                    "[Current logistics context:]\n"
                    f"{context_block}\n\n"
                    f"[User question:]\n{message}"
                )

        try:
            from google.genai import types

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.SYSTEM_PROMPT,
                    max_output_tokens=1024,
                    temperature=0.7,
                )
            )

            reply_text = (
                response.text.strip()
                if response.text
                else "No response generated."
            )

            return {
                "reply": reply_text,
                "status": "OK"
            }

        except Exception:
            # If Gemini fails, automatically fall back to offline mode.
            return {
                "reply": self._offline_response(message),
                "status": "OFFLINE_FALLBACK"
            }


# Singleton instance used by the backend.
chat_service = ChatService()