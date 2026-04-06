import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List

from dotenv import load_dotenv

# Ensure repository root is importable when running this file directly.
repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.agent.agent import ReActAgent
from src.core.gemini_provider import GeminiProvider
from src.tools.get_travel_and_gear_recommendations_tool import get_travel_and_gear_recommendations
from src.tools.location_tools import search_camp_site
from src.tools.weather_tools import get_weather_forecast

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

tool_search_camp = {
    "name": "search_camp_site",
    "description": (
        "Tim kiem dia diem cam trai/cong vien theo ban kinh. "
        "Action Input phai la JSON: "
        '{"location": "Gia Lam, Ha Noi", "radius_km": 15.0, "capacity": 4, "amenities": ["family_friendly"]}'
    ),
    "func": search_camp_site,
}

tool_get_weather = {
    "name": "get_weather_forecast",
    "description": (
        "Lay du bao thoi tiet cho dia diem va ngay. "
        "Action Input phai la JSON: "
        '{"location": "Gia Lam, Ha Noi", "date": "06/04"}'
    ),
    "func": get_weather_forecast,
}

tool_get_travel_and_gear_recommendations = {
    "name": "get_travel_and_gear_recommendations",
    "description": (
        "Ket hop campsite + weather de tao goi khuyen nghi di chuyen va do dung. "
        "Action Input phai la JSON: "
        '{"location": "Gia Lam, Ha Noi", "date": "06/04", "radius_km": 15, "capacity": 4, "amenities": ["family_friendly"], "group_type": "family"}'
    ),
    "func": get_travel_and_gear_recommendations,
}

my_tools = [tool_search_camp, tool_get_weather, tool_get_travel_and_gear_recommendations]

# 2. Khởi tạo LLM và Agent
# os.environ.get("PLACES_API_KEY")
# os.environ.get("WEATHER_API_KEY")

try:
    from scripts.evaluate_chatbot_limitations import build_provider
except ImportError:
    # Fallback: import from core if available
    from src.core.gemini_provider import GeminiProvider
    def build_provider(provider_override="gemini"):
        if provider_override == "gemini":
            return GeminiProvider(api_key=GEMINI_API_KEY)
        return GeminiProvider(api_key=GEMINI_API_KEY)

def get_camping_agent() -> ReActAgent:
    """Tạo và trả về ReActAgent đã được cấu hình với LLM và tools."""
    provider_name = os.environ.get("DEFAULT_PROVIDER", "gemini")
    # Sử dụng hàm build_provider để tự động chọn LLM theo file .env (hỗ trợ deepseek)
    llm = build_provider(provider_override=provider_name)
    return ReActAgent(llm=llm, tools=my_tools)

if __name__ == "__main__":
    agent = get_camping_agent()

    # 3. Chạy Agent
    user_prompt = "Tôi muốn 6/4 này đi cắm trại ở đâu đó quanh HN, gần gia lâm thì tốt cho gia đình 4 người. Tôi nên chuẩn bị đồ đạc gì?"
    final_answer = agent.run(user_prompt)

    print("\n=== KẾT QUẢ CUỐI CÙNG ===")
    print(final_answer)