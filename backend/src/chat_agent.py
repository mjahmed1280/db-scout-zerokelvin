import os
import logging
import sys
from typing import AsyncGenerator

# --- Google ADK Imports ---
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import our custom RAG tool
from src.rag_utils import search_rag_corpus

logger = logging.getLogger("chat_agent")

# --- ADK Session Memory ---
session_service = InMemorySessionService()

async def execute_chat(query: str, rag_corpus_id: str, session_id: str, user_id: str = "frontend_user") -> str:
    """
    Executes a chat interaction using Google ADK with session memory and structural Markdown instructions.
    """
    try:
        # 1. Dynamically configure Vertex AI Authentication from Corpus Path
        corpus_parts = rag_corpus_id.split('/')
        project_id = corpus_parts[1]
        location = corpus_parts[3]
        
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
        os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
        os.environ["GOOGLE_CLOUD_LOCATION"] = location

        # 2. Define search tool
        def search_schema(search_query: str) -> str:
            """Tool to search the database schema and documentation corpus."""
            return search_rag_corpus(search_query, rag_corpus_id)

        # 3. Define the ADK LlmAgent with Prompt Engineering for Presentation
        instruction = """
        You are the 'DB Scout Agent', a highly advanced database reconnaissance expert. 
        Your goal is to provide intelligent answers based on the database documentation provided in the search tool.

        RECONNAISSANCE PROTOCOLS:
        1. DATA ORIGIN: Answer ONLY based on information found via 'search_schema'. 
        2. STRUCTURE: Use Markdown tables for table metadata or row count distributions.
        3. CODE: Provide SQL snippets in ```sql blocks.
        4. ANOMALIES: Highlight data quality risks (nulls, outliers) using blockquotes or bold red text.
        5. HEADINGS: Use ## and ### to separate different sections of your analysis.
        6. BREVITY: Be technical and concise. Avoid conversational filler.
        """

        agent = LlmAgent(
            name='db_scout_agent',
            model='gemini-2.5-flash', # Powerful for structural reasoning
            instruction=instruction,
            tools=[search_schema],
        )

        # 4. Create the ADK Runner
        runner = Runner(
            app_name='db_scout_app',
            agent=agent,
            session_service=session_service,
        )

        # 5. Handle Session State
        current_session = await session_service.get_session(
            app_name='db_scout_app',
            user_id=user_id,
            session_id=session_id
        )
        
        if current_session is None:
            await session_service.create_session(
                app_name='db_scout_app',
                user_id=user_id,
                session_id=session_id
            )

        # 6. Trigger Agent Execution
        content = types.Content(role='user', parts=[types.Part(text=query)])
        events_async = runner.run_async(
            session_id=session_id,
            user_id=user_id,
            new_message=content
        )
        
        full_response = ""
        async for event in events_async:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        full_response += part.text
        
        return full_response

    except Exception as e:
        logger.error(f"ADK Chat Agent Error: {str(e)}", exc_info=True)
        return f"⚠️ **Scout Agent Error:** {str(e)}"