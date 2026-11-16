from functools import lru_cache 
from pathlib import Path
from pydantic_settings import BaseSettings , SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings) :
    app_name : str = "Agentic Rag Copilot"
    app_env : str = "development"
    groq_api_key : str = ""
    tavily_api_key : str = ""
    supabase_url : str = ""
    supabase_service_key : str = ""
    embedding_model : str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model :str= "openai/gpt-oss-120b"
    kb_namespace : str = "enterprice-it-support"
    top_k : int = 4
    max_retries : int= 1
    admin_api_key : str = "change_me"
    audit_db_path : str = str( BASE_DIR /  "data" / "audit.db")
    uploads_dir : str = str(BASE_DIR / "uploads")
    sample_db_dir : str = str ( BASE_DIR /  "data" / "sample.db")
    
    model_config = SettingsConfigDict(env_file = str(BASE_DIR / ".env"), extra="ignore")
    
    



@lru_cache
def get_settings() -> Settings:
    return Settings()