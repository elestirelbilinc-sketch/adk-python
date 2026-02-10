# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
VAP Media MCP Agent - AI Media Generation Example

This agent demonstrates how to use VAP Media's MCP server with Google ADK
to generate images, videos, and music using AI models.

VAP Media Features:
- Image Generation: Flux-based text-to-image with 9 aspect ratios
- Video Generation: Veo 3.1 videos (4-8 seconds, 720p/1080p)
- Music Generation: Suno V5 composition (MP3/WAV, 30-480 seconds)
- Cost Estimation: Check prices before generation
- Task Management: Track generation status and results

Prerequisites:
1. Install VAP MCP Proxy: pip install vap-mcp-proxy (or use the proxy script)
2. Get VAP API Key from https://vapagent.com
3. Set environment variable: VAP_API_KEY=your_key_here

Usage:
    # Generate an image
    "Create a futuristic cityscape at sunset"
    
    # Generate a video
    "Generate a 6-second video of ocean waves crashing"
    
    # Generate music
    "Create upbeat electronic music for a tech video"
    
    # Check task status
    "Check status of task <task_id>"
    
    # Check balance
    "What's my account balance?"

For more information:
- VAP Documentation: https://docs.vapagent.com
- API Reference: https://api.vapagent.com/docs
- Showcase: https://github.com/vapagentmedia/vap-showcase
"""

import os

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from mcp import StdioServerParameters

# Configuration
VAP_API_KEY = os.getenv("VAP_API_KEY", os.getenv("VAPE_API_KEY", ""))
VAP_MCP_PROXY_PATH = os.getenv(
    "VAP_MCP_PROXY_PATH",
    os.path.expanduser("~/vap_mcp_proxy.py")
)

root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='vap_media_assistant',
    instruction=f"""\
You are VAP Media Assistant - an AI media generation specialist powered by VAP's MCP server.

🎯 CAPABILITIES:
• Generate AI images (Flux) - 9 aspect ratios, high quality
• Generate AI videos (Veo 3.1) - 4-8 seconds, 720p/1080p
• Generate AI music (Suno V5) - MP3/WAV, 30-480 seconds
• Check task status and get results
• Estimate costs before generation
• Check account balance

💰 PRICING:
• Images: $0.18 fixed per image
• Videos: $1.96 fixed per video (Veo 3.1)
• Music: $0.68 fixed per track

📝 USAGE GUIDELINES:

For Image Generation:
- Ask for prompt if not provided
- Default aspect ratio: 1:1 (square)
- Available ratios: 1:1, 16:9, 9:16, 4:3, 3:4, 21:9, 9:21, 3:2, 2:3
- Style: Describe in detail for best results

For Video Generation:
- Duration: 4, 6, or 8 seconds (default: 8)
- Aspect ratio: 16:9 (landscape) or 9:16 (portrait)
- Resolution: 720p or 1080p (default: 720p)
- Audio: Can include AI-generated audio

For Music Generation:
- Duration: 30-480 seconds (default: 120)
- Format: MP3 or WAV
- Describe genre, mood, instruments, tempo

For Cost Estimation:
- Always offer to estimate costs before expensive operations
- Use estimate_video_cost for videos
- Image and music costs are fixed

For Task Status:
- Tasks take time to complete (30s-5min depending on type)
- Provide task_id to user after creation
- Offer to check status periodically
- When complete, provide the download URL

⚠️ IMPORTANT:
- If VAP_API_KEY is not set, warn the user and explain free tier limits
- Free tier: 3 images/day without API key
- Always confirm expensive operations (videos $1.96, music $0.68)
- Be clear about generation times (images: ~30s, videos: ~2min, music: ~1min)
""",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='python',
                    args=[VAP_MCP_PROXY_PATH],
                    env={
                        'VAP_API_KEY': VAP_API_KEY,
                        'VAP_API_URL': os.getenv('VAP_API_URL', 'https://api.vapagent.com/mcp'),
                        'VAP_API_BASE_URL': os.getenv('VAP_API_BASE_URL', 'https://api.vapagent.com'),
                    } if VAP_API_KEY else {
                        'VAP_API_URL': os.getenv('VAP_API_URL', 'https://api.vapagent.com/mcp'),
                        'VAP_API_BASE_URL': os.getenv('VAP_API_BASE_URL', 'https://api.vapagent.com'),
                    },
                ),
                timeout=300,  # 5 minutes for long operations like video generation
            ),
        )
    ],
)
