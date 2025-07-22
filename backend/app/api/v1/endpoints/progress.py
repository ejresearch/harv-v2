# backend/app/api/v1/endpoints/progress.py
"""
Progress Tracking API - Real Database Analytics
Calculates actual learning progress from conversation data
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc, and_
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.course import Module
from app.models.conversation import Conversation, Message, UserProgress
from app.models.memory import MemorySummary

router = APIRouter()

# =========================================================================
# PYDANTIC SCHEMAS
# =========================================================================

class LearningObjectiveProgress(BaseModel):
    objective: str
    completed: bool
    confidence_level: float
    evidence: List[str]
    last_practiced: Optional[str] = None

class DetailedProgressResponse(BaseModel):
    user_id: int
    module_id: int
    module_title: str
    overall_completion: float
    mastery_level: str
    
    # Engagement metrics
    total_conversations: int
    total_messages: int
    total_time_minutes: int
    average_session_duration: float
    
    # Learning insights
    memory_summaries_count: int
    key_insights: List[str]
    learning_patterns: Dict[str, Any]
    
    # Objective tracking
    objectives_progress: List[LearningObjectiveProgress]
    
    # Timeline data
    learning_timeline: List[Dict[str, Any]]
    recent_sessions: List[Dict[str, Any]]
    
    # Performance indicators
    engagement_score: float
    retention_score: float
    discovery_score: float
    
    # Next steps
    recommended_actions: List[str]
    estimated_time_to_completion: int

class ObjectiveCompletionRequest(BaseModel):
    module_id: int
    objective_text: str
    what_learned: str
    connections_made: Optional[str] = None
    confidence_level: float = 0.8

class LearningAnalytics(BaseModel):
    user_id: int
    total_modules_started: int
    total_modules_completed: int
    total_study_time_minutes: int
    average_daily_engagement: float
    learning_streak_days: int
    preferred_learning_time: str
    strengths: List[str]
    areas_for_improvement: List[str]
    cross_module_connections: int

# =========================================================================
# HELPER FUNCTIONS - Real Analytics
# =========================================================================

def calculate_engagement_score(conversations: List[Conversation]) -> float:
    """Calculate engagement score based on conversation patterns"""
    if not conversations:
        return 0.0
    
    factors = []
    
    # Message frequency
    total_messages = sum(len(conv.messages) for conv in conversations)
    avg_messages_per_session = total_messages / len(conversations)
    message_score = min(avg_messages_per_session / 15, 1.0) * 30  # Up to 30 points
    factors.append(message_score)
    
    # Session consistency
    if len(conversations) >= 3:
        # Check for regular engagement
        session_dates = [conv.created_at.date() for conv in conversations]
        unique_dates = len(set(session_dates))
        consistency_score = min(unique_dates / len(conversations), 1.0) * 25  # Up to 25 points
        factors.append(consistency_score)
    else:
        factors.append(0)
    
    # Question asking (indicators of curiosity)
    question_count = 0
    for conv in conversations:
        for msg in conv.messages:
            if msg.sender_type == "user" and "?" in msg.content:
                question_count += 1
    
    question_score = min(question_count / 5, 1.0) * 20  # Up to 20 points
    factors.append(question_score)
    
    # Session length quality
    quality_sessions = 0
    for conv in conversations:
        if len(conv.messages) >= 8:  # Substantial conversations
            quality_sessions += 1
    
    quality_score = min(quality_sessions / max(len(conversations) * 0.7, 1), 1.0) * 25  # Up to 25 points
    factors.append(quality_score)
    
    return min(sum(factors), 100.0)

def analyze_learning_patterns(conversations: List[Conversation], memory_summaries: List[MemorySummary]) -> Dict[str, Any]:
    """Analyze learning patterns from conversation data"""
    
    if not conversations:
        return {"pattern": "insufficient_data", "details": "No conversations found"}
    
    patterns = {}
    
    # Conversation timing patterns
    conv_hours = [conv.created_at.hour for conv in conversations]
    if conv_hours:
        most_active_hour = max(set(conv_hours), key=conv_hours.count)
        patterns["preferred_time"] = f"{most_active_hour}:00-{most_active_hour+1}:00"
    
    # Learning progression analysis
    conversations_by_date = sorted(conversations, key=lambda c: c.created_at)
    
    if len(conversations_by_date) >= 3:
        early_sessions = conversations_by_date[:len(conversations_by_date)//3]
        recent_sessions = conversations_by_date[-len(conversations_by_date)//3:]
        
        early_avg_messages = sum(len(conv.messages) for conv in early_sessions) / len(early_sessions)
        recent_avg_messages = sum(len(conv.messages) for conv in recent_sessions) / len(recent_sessions)
        
        if recent_avg_messages > early_avg_messages * 1.2:
            patterns["trend"] = "increasing_engagement"
        elif recent_avg_messages < early_avg_messages * 0.8:
            patterns["trend"] = "decreasing_engagement"
        else:
            patterns["trend"] = "stable_engagement"
    
    # Memory formation patterns
    if memory_summaries:
        memory_confidence = [mem.confidence_level for mem in memory_summaries if mem.confidence_level]
        if memory_confidence:
            patterns["average_confidence"] = sum(memory_confidence) / len(memory_confidence)
            patterns["confidence_trend"] = "improving" if len(memory_confidence) > 1 and memory_confidence[-1] > memory_confidence[0] else "stable"
    
    return patterns

def generate_recommendations(progress_data: Dict[str, Any]) -> List[str]:
    """Generate personalized learning recommendations"""
    recommendations = []
    
    completion = progress_data.get("completion_percentage", 0)
    conversations = progress_data.get("conversations_count", 0)
    messages = progress_data.get("messages_count", 0)
    memory_count = progress_data.get("memory_summaries_count", 0)
    
    if completion < 20:
        recommendations.append("Start with basic concepts - engage in your first meaningful conversation")
    elif completion < 50:
        recommendations.append("Continue exploring core ideas through Socratic dialogue")
    elif completion < 80:
        recommendations.append("Focus on making connections between different concepts you've learned")
    else:
        recommendations.append("Consider moving to an advanced module or helping others learn")
    
    if conversations < 3:
        recommendations.append("Have at least 3 substantial learning conversations for better understanding")
    
    if memory_count == 0:
        recommendations.append("Reflect on your learning and create some memory summaries")
    
    if messages > 0 and messages / max(conversations, 1) < 8:
        recommendations.append("Engage more deeply in conversations - ask more questions")
    
    engagement_score = progress_data.get("engagement_score", 0)
    if engagement_score < 50:
        recommendations.append("Try to be more curious - ask 'why' and 'how' questions")
    
    return recommendations

# =========================================================================
# API ENDPOINTS
# =========================================================================

@router.get("/{module_id}", response_model=DetailedProgressResponse)
async def get_detailed_progress(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed progress analysis with REAL learning analytics
    All metrics calculated from actual database interactions
    """
    
    # Get module
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Get all user data for this module
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.module_id == module_id
    ).options(joinedload(Conversation.messages)).order_by(Conversation.created_at).all()
    
    memory_summaries = db.query(MemorySummary).filter(
        MemorySummary.user_id == current_user.id,
        MemorySummary.module_id == module_id
    ).order_by(MemorySummary.created_at).all()
    
    # Calculate core metrics
    total_conversations = len(conversations)
    total_messages = sum(len(conv.messages) for conv in conversations)
    memory_count = len(memory_summaries)
    
    # Calculate time metrics
    total_time_minutes = 0
    session_durations = []
    
    for conv in conversations:
        if conv.messages and len(conv.messages) > 1:
            start_time = min(msg.created_at for msg in conv.messages)
            end_time = max(msg.created_at for msg in conv.messages)
            duration = (end_time - start_time).total_seconds() / 60
            duration = max(min(duration, 120), 5)  # 5-120 minute range
            total_time_minutes += duration
            session_durations.append(duration)
    
    average_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
    
    # Calculate completion percentage
    completion_factors = {
        'conversations': min(total_conversations * 20, 30),
        'messages': min(total_messages * 2, 25),
        'memory': min(memory_count * 15, 30),
        'time': min(total_time_minutes / 2, 15)
    }
    overall_completion = min(sum(completion_factors.values()), 100.0)
    
    # Determine mastery level
    if overall_completion >= 80:
        mastery_level = "advanced"
    elif overall_completion >= 50:
        mastery_level = "intermediate"
    elif overall_completion >= 20:
        mastery_level = "beginner"
    else:
        mastery_level = "novice"
    
    # Calculate performance scores
    engagement_score = calculate_engagement_score(conversations)
    retention_score = min(memory_count * 25, 100.0)  # Based on memory formation
    
    # Discovery score based on question asking and exploration
    discovery_indicators = 0
    for conv in conversations:
        for msg in conv.messages:
            if msg.sender_type == "user":
                if any(word in msg.content.lower() for word in ["why", "how", "what if", "?"]):
                    discovery_indicators += 1
    
    discovery_score = min(discovery_indicators * 5, 100.0)
    
    # Analyze learning patterns
    learning_patterns = analyze_learning_patterns(conversations, memory_summaries)
    
    # Parse module objectives
    try:
        module_objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
    except (json.JSONDecodeError, TypeError):
        module_objectives = ["Understand core concepts", "Apply learning through practice"]
    
    # Track objective progress
    objectives_progress = []
    for i, objective in enumerate(module_objectives):
        # Determine completion based on engagement patterns
        completed = False
        confidence = 0.0
        evidence = []
        
        if i == 0 and total_conversations >= 1:
            completed = True
            confidence = 0.7
            evidence.append(f"Started learning with {total_conversations} conversation(s)")
        
        if i == 1 and total_messages >= 10:
            completed = True
            confidence = 0.8
            evidence.append(f"Active participation with {total_messages} messages")
        
        if i == 2 and memory_count >= 1:
            completed = True
            confidence = 0.9
            evidence.append(f"Generated {memory_count} learning insight(s)")
        
        # Advanced objectives based on deeper engagement
        if i >= 3:
            if total_time_minutes >= 60 and memory_count >= 2:
                completed = True
                confidence = 0.85
                evidence.append(f"Deep engagement: {int(total_time_minutes)} minutes of study")
        
        last_practiced = None
        if conversations:
            last_practiced = conversations[-1].updated_at.isoformat()
        
        objectives_progress.append(LearningObjectiveProgress(
            objective=objective,
            completed=completed,
            confidence_level=confidence,
            evidence=evidence,
            last_practiced=last_practiced
        ))
    
    # Create learning timeline
    learning_timeline = []
    for conv in conversations:
        timeline_entry = {
            "date": conv.created_at.isoformat(),
            "type": "conversation",
            "title": conv.title or f"Learning Session {conv.id}",
            "message_count": len(conv.messages),
            "duration_minutes": max((conv.updated_at - conv.created_at).total_seconds() / 60, 5),
            "key_topics": []  # Could extract from message content analysis
        }
        learning_timeline.append(timeline_entry)
    
    for memory in memory_summaries:
        timeline_entry = {
            "date": memory.created_at.isoformat(),
            "type": "insight",
            "title": "Learning Insight Generated",
            "what_learned": memory.what_learned[:100] + "..." if len(memory.what_learned) > 100 else memory.what_learned,
            "confidence": memory.confidence_level
        }
        learning_timeline.append(timeline_entry)
    
    # Sort timeline by date
    learning_timeline.sort(key=lambda x: x["date"])
    
    # Recent sessions (last 3)
    recent_sessions = []
    for conv in conversations[-3:]:
        session_data = {
            "conversation_id": conv.id,
            "date": conv.created_at.isoformat(),
            "title": conv.title or f"Session {conv.id}",
            "message_count": len(conv.messages),
            "duration_minutes": max((conv.updated_at - conv.created_at).total_seconds() / 60, 5),
            "summary": conv.summary[:150] + "..." if conv.summary and len(conv.summary) > 150 else (conv.summary or "Learning session completed")
        }
        recent_sessions.append(session_data)
    
    # Key insights from memory summaries
    key_insights = []
    for memory in memory_summaries:
        if memory.what_learned:
            insight = memory.what_learned[:100] + "..." if len(memory.what_learned) > 100 else memory.what_learned
            key_insights.append(insight)
    
    # Generate recommendations
    progress_summary = {
        "completion_percentage": overall_completion,
        "conversations_count": total_conversations,
        "messages_count": total_messages,
        "memory_summaries_count": memory_count,
        "engagement_score": engagement_score
    }
    recommended_actions = generate_recommendations(progress_summary)
    
    # Estimate time to completion
    if overall_completion >= 90:
        estimated_time = 0
    elif overall_completion >= 70:
        estimated_time = 30  # 30 minutes
    elif overall_completion >= 40:
        estimated_time = 60  # 1 hour
    else:
        estimated_time = 120  # 2 hours
    
    return DetailedProgressResponse(
        user_id=current_user.id,
        module_id=module_id,
        module_title=module.title,
        overall_completion=round(overall_completion, 1),
        mastery_level=mastery_level,
        
        total_conversations=total_conversations,
        total_messages=total_messages,
        total_time_minutes=int(total_time_minutes),
        average_session_duration=round(average_session_duration, 1),
        
        memory_summaries_count=memory_count,
        key_insights=key_insights,
        learning_patterns=learning_patterns,
        
        objectives_progress=objectives_progress,
        
        learning_timeline=learning_timeline,
        recent_sessions=recent_sessions,
        
        engagement_score=round(engagement_score, 1),
        retention_score=round(retention_score, 1),
        discovery_score=round(discovery_score, 1),
        
        recommended_actions=recommended_actions,
        estimated_time_to_completion=estimated_time
    )

@router.post("/objectives/complete")
async def complete_objective(
    objective_data: ObjectiveCompletionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark an objective as completed and create memory summary
    Creates REAL database entries for learning achievements
    """
    
    # Verify module exists
    module = db.query(Module).filter(Module.id == objective_data.module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Create memory summary for this learning achievement
    memory_summary = MemorySummary(
        user_id=current_user.id,
        module_id=objective_data.module_id,
        what_learned=objective_data.what_learned,
        how_learned="Discovered through Socratic dialogue and reflection",
        connections_made=objective_data.connections_made or "",
        confidence_level=objective_data.confidence_level,
        created_at=datetime.utcnow()
    )
    
    db.add(memory_summary)
    
    # Update or create user progress record
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.module_id == objective_data.module_id
    ).first()
    
    if not progress:
        # Calculate current progress for new record
        conversations = db.query(Conversation).filter(
            Conversation.user_id == current_user.id,
            Conversation.module_id == objective_data.module_id
        ).all()
        
        total_conversations = len(conversations)
        total_messages = sum(len(conv.messages) for conv in conversations)
        memory_count = db.query(MemorySummary).filter(
            MemorySummary.user_id == current_user.id,
            MemorySummary.module_id == objective_data.module_id
        ).count() + 1  # +1 for the one we're adding
        
        # Calculate completion based on new memory summary
        completion_percentage = min((memory_count * 20) + (total_conversations * 15) + min(total_messages, 25), 100)
        
        progress = UserProgress(
            user_id=current_user.id,
            module_id=objective_data.module_id,
            completion_percentage=completion_percentage,
            mastery_level="beginner" if completion_percentage < 40 else "intermediate",
            total_conversations=total_conversations,
            total_messages=total_messages,
            time_spent=0,  # Would be calculated from conversation timestamps
            created_at=datetime.utcnow()
        )
        db.add(progress)
    else:
        # Update existing progress
        memory_count = db.query(MemorySummary).filter(
            MemorySummary.user_id == current_user.id,
            MemorySummary.module_id == objective_data.module_id
        ).count() + 1  # +1 for the one we're adding
        
        # Increase completion percentage based on new insight
        progress.completion_percentage = min(progress.completion_percentage + (20 / 5), 100)  # Assume 5 objectives max
        
        if progress.completion_percentage >= 80:
            progress.mastery_level = "advanced"
        elif progress.completion_percentage >= 50:
            progress.mastery_level = "intermediate"
        else:
            progress.mastery_level = "beginner"
        
        progress.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(memory_summary)
    db.refresh(progress)
    
    return {
        "status": "objective_completed",
        "objective": objective_data.objective_text,
        "memory_summary_id": memory_summary.id,
        "new_completion_percentage": round(progress.completion_percentage, 1),
        "mastery_level": progress.mastery_level,
        "confidence_level": objective_data.confidence_level,
        "created_at": memory_summary.created_at.isoformat(),
        "message": "Learning achievement recorded successfully!"
    }

@router.get("/analytics/overview", response_model=LearningAnalytics)
async def get_learning_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get overall learning analytics across all modules
    Provides comprehensive learning insights from real database data
    """
    
    # Get all user progress records
    user_progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()
    
    # Get all conversations
    all_conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id
    ).options(joinedload(Conversation.messages)).all()
    
    # Get all memory summaries
    all_memories = db.query(MemorySummary).filter(
        MemorySummary.user_id == current_user.id
    ).all()
    
    # Calculate metrics
    total_modules_started = len(set(conv.module_id for conv in all_conversations))
    total_modules_completed = len([p for p in user_progress if p.completion_percentage >= 80])
    
    # Calculate total study time
    total_study_time = 0
    for conv in all_conversations:
        if conv.messages and len(conv.messages) > 1:
            duration = (conv.updated_at - conv.created_at).total_seconds() / 60
            total_study_time += max(min(duration, 120), 5)
    
    # Calculate learning streak
    conversation_dates = sorted(set(conv.created_at.date() for conv in all_conversations))
    learning_streak = 0
    if conversation_dates:
        current_streak = 1
        for i in range(1, len(conversation_dates)):
            if (conversation_dates[i] - conversation_dates[i-1]).days <= 2:  # Allow 1 day gap
                current_streak += 1
            else:
                current_streak = 1
            learning_streak = max(learning_streak, current_streak)
    
    # Analyze preferred learning time
    conv_hours = [conv.created_at.hour for conv in all_conversations]
    preferred_time = "Not determined"
    if conv_hours:
        most_common_hour = max(set(conv_hours), key=conv_hours.count)
        if most_common_hour < 12:
            preferred_time = "Morning (6AM-12PM)"
        elif most_common_hour < 17:
            preferred_time = "Afternoon (12PM-5PM)"
        else:
            preferred_time = "Evening (5PM-11PM)"
    
    # Calculate average daily engagement
    if conversation_dates:
        days_active = len(conversation_dates)
        total_messages = sum(len(conv.messages) for conv in all_conversations)
        average_daily_engagement = total_messages / days_active
    else:
        average_daily_engagement = 0.0
    
    # Identify strengths based on memory summaries and engagement
    strengths = []
    if len(all_memories) >= 3:
        strengths.append("Strong reflection and insight generation")
    if average_daily_engagement >= 15:
        strengths.append("High engagement and participation")
    if learning_streak >= 3:
        strengths.append("Consistent learning habits")
    if total_study_time >= 180:  # 3+ hours
        strengths.append("Dedicated time investment")
    
    # Areas for improvement
    areas_for_improvement = []
    if len(all_memories) < 2:
        areas_for_improvement.append("Create more learning reflections and insights")
    if average_daily_engagement < 8:
        areas_for_improvement.append("Increase engagement in conversations")
    if learning_streak < 2:
        areas_for_improvement.append("Develop more consistent learning routine")
    if total_modules_started > 0 and total_modules_completed == 0:
        areas_for_improvement.append("Focus on completing started modules")
    
    # Count cross-module connections
    cross_module_connections = 0
    for memory in all_memories:
        if memory.connections_made and len(memory.connections_made.strip()) > 0:
            cross_module_connections += 1
    
    return LearningAnalytics(
        user_id=current_user.id,
        total_modules_started=total_modules_started,
        total_modules_completed=total_modules_completed,
        total_study_time_minutes=int(total_study_time),
        average_daily_engagement=round(average_daily_engagement, 1),
        learning_streak_days=learning_streak,
        preferred_learning_time=preferred_time,
        strengths=strengths or ["Getting started with learning journey"],
        areas_for_improvement=areas_for_improvement or ["Continue current learning approach"],
        cross_module_connections=cross_module_connections
    )
