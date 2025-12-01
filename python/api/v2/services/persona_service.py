"""
Persona service - Business logic for persona management
"""

from typing import List, Optional
from datetime import datetime
import uuid
from ..models import PersonaCreate, PersonaUpdate, PersonaResponse, PersonaDomain
from python.helpers import files
import json
import os

class PersonaService:
    """Service for managing personas"""
    
    PERSONAS_DIR = "/workspace/personas"
    
    @classmethod
    def _ensure_personas_dir(cls):
        """Ensure personas directory exists"""
        os.makedirs(cls.PERSONAS_DIR, exist_ok=True)
    
    @classmethod
    def _get_persona_path(cls, user_id: str, persona_id: str) -> str:
        """Get file path for persona"""
        return os.path.join(cls.PERSONAS_DIR, user_id, f"{persona_id}.json")
    
    @classmethod
    def _save_persona(cls, user_id: str, persona: PersonaResponse):
        """Save persona to disk"""
        cls._ensure_personas_dir()
        user_dir = os.path.join(cls.PERSONAS_DIR, user_id)
        os.makedirs(user_dir, exist_ok=True)
        
        filepath = cls._get_persona_path(user_id, persona.id)
        with open(filepath, 'w') as f:
            json.dump(persona.dict(), f, indent=2, default=str)
    
    @classmethod
    def _load_persona(cls, user_id: str, persona_id: str) -> Optional[PersonaResponse]:
        """Load persona from disk"""
        filepath = cls._get_persona_path(user_id, persona_id)
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
            return PersonaResponse(**data)
    
    @classmethod
    def create_persona(cls, user_id: str, data: PersonaCreate) -> PersonaResponse:
        """Create a new persona"""
        persona_id = str(uuid.uuid4())
        now = datetime.now()
        
        persona = PersonaResponse(
            id=persona_id,
            name=data.name,
            role=data.role,
            expertise=data.expertise,
            avatar=data.avatar,
            traits=data.traits,
            behavior=data.behavior,
            config=data.config,
            domain=data.domain,
            custom_instructions=data.custom_instructions,
            created_at=now,
            updated_at=now,
            user_id=user_id
        )
        
        cls._save_persona(user_id, persona)
        return persona
    
    @classmethod
    def get_persona(cls, persona_id: str, user_id: str) -> Optional[PersonaResponse]:
        """Get persona by ID"""
        return cls._load_persona(user_id, persona_id)
    
    @classmethod
    def list_personas(
        cls,
        user_id: str,
        domain: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[PersonaResponse]:
        """List personas for user"""
        cls._ensure_personas_dir()
        user_dir = os.path.join(cls.PERSONAS_DIR, user_id)
        
        if not os.path.exists(user_dir):
            return []
        
        personas = []
        for filename in os.listdir(user_dir):
            if filename.endswith('.json'):
                persona_id = filename[:-5]  # Remove .json
                persona = cls._load_persona(user_id, persona_id)
                if persona:
                    if domain is None or persona.domain == domain:
                        personas.append(persona)
        
        # Sort by created_at descending
        personas.sort(key=lambda p: p.created_at, reverse=True)
        
        # Apply pagination
        return personas[offset:offset + limit]
    
    @classmethod
    def update_persona(
        cls,
        persona_id: str,
        user_id: str,
        data: PersonaUpdate
    ) -> Optional[PersonaResponse]:
        """Update persona"""
        persona = cls._load_persona(user_id, persona_id)
        if not persona:
            return None
        
        # Update fields
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(persona, field):
                setattr(persona, field, value)
        
        persona.updated_at = datetime.now()
        cls._save_persona(user_id, persona)
        return persona
    
    @classmethod
    def delete_persona(cls, persona_id: str, user_id: str) -> bool:
        """Delete persona"""
        filepath = cls._get_persona_path(user_id, persona_id)
        if not os.path.exists(filepath):
            return False
        
        os.remove(filepath)
        return True
    
    @classmethod
    def create_default_personas(cls, user_id: str) -> List[PersonaResponse]:
        """Create default personas for new user"""
        default_personas = [
            PersonaCreate(
                name="General Assistant",
                role="Helpful AI assistant",
                expertise=["general knowledge", "problem solving", "conversation"],
                domain=PersonaDomain.GENERAL,
                traits={"formality": 50, "verbosity": 50, "creativity": 60, "empathy": 70, "humor": 40},
                behavior={
                    "greeting": "Hello! I'm here to help you with anything you need.",
                    "style": "friendly and helpful",
                    "constraints": [],
                    "preferences": []
                }
            ),
            PersonaCreate(
                name="Robotics Engineer",
                role="Robotics and automation specialist",
                expertise=["ROS", "computer vision", "motion planning", "embedded systems", "Python", "C++"],
                domain=PersonaDomain.ROBOTICS,
                traits={"formality": 60, "verbosity": 50, "creativity": 55, "empathy": 50, "humor": 30},
                behavior={
                    "greeting": "Hello! I'm your robotics engineering assistant. How can I help with your robotics project?",
                    "style": "technical and precise",
                    "constraints": ["Always consider safety implications", "Validate hardware constraints"],
                    "preferences": ["Use ROS best practices", "Provide code examples"]
                },
                custom_instructions="Focus on robotics engineering best practices. Always consider safety, real-time constraints, and hardware limitations. Provide practical, tested solutions."
            ),
            PersonaCreate(
                name="Financial Analyst",
                role="Financial analysis and investment specialist",
                expertise=["financial modeling", "data analysis", "market research", "risk assessment", "Python", "Excel"],
                domain=PersonaDomain.FINANCE,
                traits={"formality": 80, "verbosity": 60, "creativity": 40, "empathy": 50, "humor": 20},
                behavior={
                    "greeting": "Good day. I'm your financial analysis assistant. How may I assist you?",
                    "style": "professional and analytical",
                    "constraints": ["Always cite data sources", "Provide risk disclaimers"],
                    "preferences": ["Use quantitative analysis", "Show calculations"]
                },
                custom_instructions="Focus on data-driven financial analysis. Always provide sources, show calculations, and include appropriate risk disclaimers."
            ),
            PersonaCreate(
                name="Software Architect",
                role="Software architecture and engineering specialist",
                expertise=["system design", "software architecture", "code review", "best practices", "multiple languages"],
                domain=PersonaDomain.ENGINEERING,
                traits={"formality": 60, "verbosity": 65, "creativity": 60, "empathy": 60, "humor": 35},
                behavior={
                    "greeting": "Hi! I'm your software architecture assistant. What are we building today?",
                    "style": "thoughtful and thorough",
                    "constraints": ["Follow SOLID principles", "Consider scalability"],
                    "preferences": ["Provide design rationale", "Consider trade-offs"]
                },
                custom_instructions="Focus on software architecture best practices. Consider scalability, maintainability, and trade-offs. Provide clear rationale for design decisions."
            ),
            PersonaCreate(
                name="Marketing Strategist",
                role="Marketing and content strategy specialist",
                expertise=["content creation", "SEO", "social media", "campaign planning", "analytics"],
                domain=PersonaDomain.MARKETING,
                traits={"formality": 40, "verbosity": 60, "creativity": 85, "empathy": 75, "humor": 65},
                behavior={
                    "greeting": "Hey there! Ready to create something amazing? Let's make your brand shine!",
                    "style": "creative and engaging",
                    "constraints": ["Stay on brand", "Consider target audience"],
                    "preferences": ["Use storytelling", "Provide examples"]
                },
                custom_instructions="Focus on creative, engaging content that resonates with target audiences. Consider brand voice, SEO, and measurable outcomes."
            )
        ]
        
        created = []
        for persona_data in default_personas:
            persona = cls.create_persona(user_id, persona_data)
            created.append(persona)
        
        return created
