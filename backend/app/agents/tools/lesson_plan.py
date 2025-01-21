from typing import List, Dict, Any, Optional, ClassVar, Union, Tuple
from datetime import datetime
from uuid import uuid4
from enum import Enum
import re
import logging
from pydantic import BaseModel, Field, model_validator, field_validator, ConfigDict
from dataclasses import dataclass
from app.agents.tools.agent_tool import AgentTool
from app.repositories.models.custom_bot import BotModel
from app.routes.schemas.conversation import type_model_name
from app.vector_search import search_related_docs


logger = logging.getLogger(__name__)

# Custom Exceptions
class TimeStructureError(Exception):
    """Custom exception for time structure validation errors"""
    pass

class InputValidationError(Exception):
    """Custom exception for input validation errors"""
    pass

class ContentFilterError(Exception):
    """Custom exception for content filtering errors"""
    pass

# Enums
class EducationLevel(str, Enum):
    """Education levels for both K-12 and higher education"""
    # K-12 Levels
    ELEMENTARY = "elementary"
    MIDDLE = "middle"
    HIGH = "high"
    # Higher Education Levels
    ASSOCIATE = "associate"
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    PROFESSIONAL = "professional"
    CONTINUING_ED = "continuing_education"

    @classmethod
    def is_k12(cls, level: 'EducationLevel') -> bool:
        """Check if education level is K-12"""
        return level in {cls.ELEMENTARY, cls.MIDDLE, cls.HIGH}

class DeliveryMode(str, Enum):
    """Available delivery modes for lessons"""
    IN_PERSON = "in_person"
    HYBRID = "hybrid"
    ONLINE_SYNC = "online_synchronous"
    ONLINE_ASYNC = "online_asynchronous"
    BLENDED = "blended"

# Data Models
class TimeStructure(BaseModel):
    """Time allocation structure for lesson components"""
    model_config = ConfigDict(frozen=True)

    intro_percent: int = Field(
        default=10, 
        ge=5, 
        le=20,
        description="Percentage of time for introduction"
    )
    main_content_percent: int = Field(
        default=60,
        ge=40,
        le=70,
        description="Percentage of time for main content"
    )
    practice_percent: int = Field(
        default=20,
        ge=15,
        le=30,
        description="Percentage of time for practice"
    )
    wrap_up_percent: int = Field(
        default=10,
        ge=5,
        le=15,
        description="Percentage of time for wrap-up"
    )

    @model_validator(mode='after')
    def validate_total_percentage(self) -> 'TimeStructure':
        """Ensure time percentages sum to 100%"""
        total = (self.intro_percent + self.main_content_percent +
                self.practice_percent + self.wrap_up_percent)
        if total != 100:
            raise TimeStructureError(
                f"Time allocations must sum to 100%, current total: {total}%"
            )
        return self

class UnifiedLessonPlanInput(BaseModel):
    """Input model for lesson plan generation"""
    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True
    )

    # Required Common Fields
    subject: str = Field(
        description="Subject or course topic",
        min_length=2,
        max_length=100
    )
    education_level: EducationLevel = Field(
        description="Educational level (K-12 or Higher Education)"
    )
    duration: int = Field(
        default=60,
        ge=30,
        le=180,
        description="Session duration in minutes"
    )

    # Add documents field for specific source documents
    documents: Optional[List[str]] = Field(
        default=None,
        description="List of source document names to search in knowledge base"
    )

    # K-12 Specific Fields
    grade: Optional[str] = Field(
        default=None,
        description="Grade level (e.g., '3rd grade', required for K-12)"
    )
    learning_style: Optional[str] = Field(
        default="mixed",
        pattern="^(visual|auditory|kinesthetic|mixed)$",
        description="Learning style focus for K-12"
    )
    
    # Higher Education Specific Fields
    course_code: Optional[str] = Field(
        default=None,
        description="Course code for higher education"
    )
    credits: Optional[int] = Field(
        default=None,
        ge=1,
        le=6,
        description="Number of credits (higher education)"
    )
    prerequisites: Optional[List[str]] = Field(
        default=None,
        description="Prerequisites for college courses"
    )
    
    # Optional Common Fields
    delivery_mode: DeliveryMode = Field(
        default=DeliveryMode.IN_PERSON,
        description="Lesson delivery method"
    )
    student_count: Optional[int] = Field(
        default=None,
        ge=1,
        le=5000000,
        description="Expected number of students"
    )
    time_structure: Optional[TimeStructure] = Field(
        default=None,
        description="Custom time allocation structure"
    )
    language: str = Field(
        default="en",
        pattern="^[a-z]{2}(-[A-Z]{2})?$",
        description="Language code (e.g., 'en', 'es-MX')"
    )

    @field_validator('grade')
    @classmethod
    def validate_grade_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate grade level format"""
        if v is None:
            return v
            
        grade_pattern = r'^(pre-k|kindergarten|[1-9]|1[0-2])(st|nd|rd|th)?\s*grade$'
        if not re.match(grade_pattern, v.lower()):
            raise InputValidationError(
                "Invalid grade format. Examples: '3rd grade', '12th grade', "
                "'kindergarten', 'pre-k'"
            )
        return v.lower()

    @field_validator('course_code')
    @classmethod
    def validate_course_code(cls, v: Optional[str]) -> Optional[str]:
        """Validate course code format"""
        if v is None:
            return v
            
        course_pattern = r'^[A-Z]{2,4}\s*\d{3,4}[A-Z]?$'
        if not re.match(course_pattern, v.upper()):
            raise InputValidationError(
                "Invalid course code format. Example: 'COMP101', 'BIO223A'"
            )
        return v.upper()


@dataclass
class ContentResult:
    """Structured content result with metadata"""
    content: str
    source_name: str
    metadata: Dict[str, Any]
    relevance_score: float

class UnifiedLessonPlannerTool(AgentTool):
    """Tool for generating comprehensive lesson plans for both K-12 and higher education"""
    
    DESCRIPTION: ClassVar[str] = (
        "Generate comprehensive lesson plans with automatic adaptation to "
        "educational context (K-12 or higher education). Provides structured "
        "content, time allocation, and assessment strategies."
    )
    
    MAX_SEARCH_RESULTS: ClassVar[int] = 12
    RELEVANCE_THRESHOLD: ClassVar[float] = 0.65
    MAX_CONTENT_LENGTH: ClassVar[int] = 5000

    def __init__(self, bot: BotModel, model: type_model_name):
        """Initialize the lesson planner tool"""
        super().__init__(
            name="lesson_planner",
            description=self.DESCRIPTION,
            args_schema=UnifiedLessonPlanInput,
            function=self.generate_lesson_plan,
            bot=bot,
            model=model
        )
        
        self.content_cache: Dict[str, List[ContentResult]] = {}

    def _process_search_results(
        self,
        results: List[Dict[str, Any]]
    ) -> List[ContentResult]:
        """Process and structure search results"""
        processed_results = []
        
        for result in results:
            try:
                content_result = ContentResult(
                    content=result.get('content', ''),
                    source_name=result.get('source_name', 'Unknown Source'),
                    metadata=result.get('metadata', {}),
                    relevance_score=float(result.get('relevance_score', 0.0))
                )
                processed_results.append(content_result)
            except (ValueError, TypeError) as e:
                logger.warning(f"Error processing search result: {e}")
                continue
                
        return processed_results

    def filter_relevant_content(
        self,
        search_results: List[ContentResult],
        education_level: EducationLevel
    ) -> Tuple[List[ContentResult], List[str]]:
        """Filter content and collect warnings about metadata issues"""
        filtered_results = []
        warnings = []
        
        for result in search_results:
            if not result.metadata:
                warnings.append(
                    f"Missing metadata for content from: {result.source_name}"
                )
                continue
                
            result_level = result.metadata.get('education_level')
            if not result_level:
                warnings.append(
                    f"Missing education level in metadata for: {result.source_name}"
                )
                continue
                
            if (result.relevance_score > self.RELEVANCE_THRESHOLD and 
                result_level == education_level):
                filtered_results.append(result)

        filtered_results = filtered_results[:self.MAX_SEARCH_RESULTS]
        
        if not filtered_results and search_results:
            warnings.append(
                "No content passed relevance and education level filters"
            )
            
        return filtered_results, warnings

    def calculate_time_allocation(
        self,
        duration: int,
        time_structure: Optional[TimeStructure] = None
    ) -> Dict[str, int]:
        """Calculate time allocation with validation and rounding compensation"""
        try:
            if not time_structure:
                time_structure = TimeStructure()
            
            # Calculate initial time allocations
            allocations = {
                "introduction": int(duration * time_structure.intro_percent / 100),
                "main_content": int(duration * time_structure.main_content_percent / 100),
                "practice": int(duration * time_structure.practice_percent / 100),
                "wrap_up": int(duration * time_structure.wrap_up_percent / 100)
            }
            
            # Handle rounding differences
            total_allocated = sum(allocations.values())
            if total_allocated != duration:
                difference = duration - total_allocated
                # Add or subtract the difference from the main content section
                allocations["main_content"] += difference
            
            # Validate final allocations
            if sum(allocations.values()) != duration:
                raise TimeStructureError(
                    "Time allocation validation failed after rounding adjustment"
                )
                
            return allocations
            
        except Exception as e:
            raise TimeStructureError(f"Time allocation error: {str(e)}")

    def _create_metadata(
        self,
        tool_input: UnifiedLessonPlanInput,
        content_results: List[ContentResult],
        time_allocation: Dict[str, int],
        warnings: List[str]
    ) -> Dict[str, Any]:
        """Create comprehensive metadata for the lesson plan"""
        metadata = {
            "plan_id": str(uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "subject": tool_input.subject,
            "education_level": tool_input.education_level,
            "delivery_mode": tool_input.delivery_mode,
            "duration": tool_input.duration,
            "time_allocation": time_allocation,
            "student_count": tool_input.student_count,
            "language": tool_input.language,
            "sources": [result.source_name for result in content_results],
            "warnings": warnings if warnings else [],
            "validation_status": "warning" if warnings else "success"
        }

        # Add context-specific metadata
        if EducationLevel.is_k12(tool_input.education_level):
            metadata.update({
                "grade": tool_input.grade,
                "learning_style": tool_input.learning_style
            })
        else:
            # Only add higher education fields if they exist
            higher_ed_fields = {}
            if tool_input.course_code:
                higher_ed_fields["course_code"] = tool_input.course_code
            if tool_input.credits:
                higher_ed_fields["credits"] = tool_input.credits
            if tool_input.prerequisites:
                higher_ed_fields["prerequisites"] = tool_input.prerequisites
            metadata.update(higher_ed_fields)

        return metadata


    def _build_search_query(
        self,
        tool_input: UnifiedLessonPlanInput
    ) -> str:
        """Build context-appropriate search query for knowledge base search"""
        is_k12 = EducationLevel.is_k12(tool_input.education_level)

        # Base components for search query
        subject_term = tool_input.subject
        level_term = tool_input.grade if is_k12 else tool_input.education_level
        
        if is_k12:
            query = (
                f"Find curriculum standards and teaching strategies for "
                f"{subject_term} at {level_term} level"
            )
        else:
            # Build higher education query
            query_parts = [
                f"Find course content and teaching strategies for {subject_term}",
                f"at {level_term} level"
            ]
            
            if tool_input.course_code:
                query_parts.insert(1, f"course {tool_input.course_code}")
                
            query = " ".join(query_parts)

        # Add any documents if specified
        if tool_input.documents:
            documents_list = " ".join(tool_input.documents)
            query += f" sources: {documents_list}"

        logger.info(f"Built search query: {query}")
        return query


    def _truncate_content(self, content: str, max_length: int) -> str:
        """Smartly truncate content to specified length"""
        if len(content) <= max_length:
            return content
            
        # Try to truncate at sentence boundary
        truncated = content[:max_length]
        last_period = truncated.rfind('.')
        if last_period > max_length * 0.8:  # Don't truncate too short
            return truncated[:last_period + 1]
        return truncated

    def generate_lesson_plan(
        self,
        tool_input: UnifiedLessonPlanInput,
        bot: BotModel | None,
        model: type_model_name | None
    ) -> List[Dict[str, Any]]:
        """Generate a comprehensive lesson plan based on input parameters"""
        if bot is None:
            raise ValueError("Bot instance required for lesson plan generation")

        warnings = []
        try:
            is_k12 = EducationLevel.is_k12(tool_input.education_level)
            context_type = "K-12" if is_k12 else "Higher Education"
            
            logger.info(
                f"Generating {context_type} lesson plan - "
                f"Subject: {tool_input.subject}, "
                f"Level: {tool_input.education_level}"
            )

            # Validate knowledge base configuration
            if not hasattr(bot, 'bedrock_knowledge_base') or bot.bedrock_knowledge_base is None:
                logger.warning("Bedrock knowledge base not configured, proceeding with base template")
                # Create a minimal result without search
                time_allocation = self.calculate_time_allocation(
                    tool_input.duration,
                    tool_input.time_structure
                )
                
                lesson_prompt = self._create_lesson_prompt(
                    tool_input=tool_input,
                    content_results=[],  # Empty content results
                    time_allocation=time_allocation,
                    is_k12=is_k12
                )
                
                return [{
                    "content": lesson_prompt,
                    "source_name": "Unified Lesson Planner",
                    "status": "success",
                    "metadata": self._create_metadata(
                        tool_input=tool_input,
                        content_results=[],
                        time_allocation=time_allocation,
                        warnings=["Knowledge base not configured - using base template"]
                    )
                }]

            # If knowledge base is configured, proceed with search
            search_results = search_related_docs(
                bot=bot,
                query=self._build_search_query(tool_input)
            )

            if not search_results:
                return [{
                    "content": (
                        f"No content found for {tool_input.subject}. "
                        "Please verify the subject and try again."
                    ),
                    "source_name": "Unified Lesson Planner",
                    "status": "error"
                }]

            # Process and filter content
            processed_results = self._process_search_results(search_results)
            filtered_results, content_warnings = self.filter_relevant_content(
                processed_results,
                tool_input.education_level
            )
            warnings.extend(content_warnings)

            # Calculate time allocation
            time_allocation = self.calculate_time_allocation(
                tool_input.duration,
                tool_input.time_structure
            )

            # Generate appropriate prompt
            lesson_prompt = self._create_lesson_prompt(
                tool_input,
                filtered_results,
                time_allocation,
                is_k12
            )

            logger.info(
                f"Successfully generated lesson plan for {tool_input.subject}"
            )
            
            # Create response
            response = [{
                "content": lesson_prompt,
                "source_name": "Unified Lesson Planner",
                "status": "success",
                "metadata": self._create_metadata(
                    tool_input,
                    filtered_results,
                    time_allocation,
                    warnings
                )
            }]

            if warnings:
                response[0]["warnings"] = warnings

            return response

        except TimeStructureError as e:
            logger.error(f"Time structure error: {str(e)}")
            return [{
                "content": f"Error in time allocation: {str(e)}",
                "source_name": "Unified Lesson Planner",
                "status": "error"
            }]
        except InputValidationError as e:
            logger.error(f"Input validation error: {str(e)}")
            return [{
                "content": f"Invalid input: {str(e)}",
                "source_name": "Unified Lesson Planner",
                "status": "error"
            }]
        except Exception as e:
            logger.error(
                f"Unexpected error in lesson plan generation: {str(e)}", 
                exc_info=True
            )
            return [{
                "content": (
                    f"An unexpected error occurred while generating the lesson plan: "
                    f"{str(e)}"
                ),
                "source_name": "Unified Lesson Planner",
                "status": "error"
            }]

    def _create_lesson_prompt(
        self,
        tool_input: UnifiedLessonPlanInput,
        content_results: List[ContentResult],
        time_allocation: Dict[str, int],
        is_k12: bool
    ) -> str:
        """Create appropriate lesson plan prompt based on education level"""
        # Combine and truncate content
        content_text = "\n\n".join(
            self._truncate_content(result.content, self.MAX_CONTENT_LENGTH)
            for result in content_results
        )
        sources = [f"- {result.source_name}" for result in content_results]

        if is_k12:
            return self._create_k12_prompt(
                tool_input,
                content_text,
                sources,
                time_allocation
            )
        return self._create_higher_ed_prompt(
            tool_input,
            content_text,
            sources,
            time_allocation
        )

    def _create_k12_prompt(
        self,
        tool_input: UnifiedLessonPlanInput,
        content_text: str,
        sources: List[str],
        time_allocation: Dict[str, int]
    ) -> str:
        """Create K-12 specific lesson plan prompt"""
        return f"""You are a K-12 education specialist creating a {tool_input.duration}-minute 
lesson plan for {tool_input.subject} at {tool_input.grade} level.

LESSON CONTEXT:
Grade Level: {tool_input.grade}
Subject: {tool_input.subject}
Learning Style Focus: {tool_input.learning_style}
Class Size: {tool_input.student_count or 'Not specified'}
Delivery Mode: {tool_input.delivery_mode}

CONTENT RESOURCES:
{content_text}

REFERENCE MATERIALS:
{chr(10).join(sources)}

LESSON PLAN STRUCTURE:

1. LESSON OVERVIEW
- Subject & Grade Level
- Duration: {tool_input.duration} minutes
- Standards Alignment
- Learning Objectives (2-3 specific, measurable objectives)

2. MATERIALS & PREPARATION
- Required Materials
- Technology Tools
- Visual Aids
- Room Setup
- Safety Considerations (if applicable)

3. LESSON FLOW
a) Introduction & Hook ({time_allocation['introduction']} minutes)
   - Engagement Strategy
   - Prior Knowledge Activation
   - Learning Objectives Review

b) Main Lesson ({time_allocation['main_content']} minutes)
   - Direct Instruction
   - Modeling/Demonstrations
   - Student Engagement Strategies
   - Key Concepts Coverage

c) Guided Practice ({time_allocation['practice']} minutes)
   - Student Activities
   - Group/Individual Work
   - Application Exercises
   - Support Strategies

d) Wrap-up & Assessment ({time_allocation['wrap_up']} minutes)
   - Learning Review
   - Exit Tickets/Checks
   - Preview of Next Lesson

4. DIFFERENTIATION STRATEGIES
- Support for Different Learning Styles
- Accommodations for Various Ability Levels
- Extension Activities for Advanced Learners
- Support for Struggling Learners

5. ASSESSMENT STRATEGY
- Formative Assessment Methods
- Success Criteria
- Student Self-reflection
- Progress Monitoring Tools

6. HOMEWORK & EXTENSION
- Assigned Work (if applicable)
- Family Connection Activities
- Additional Resources
- Early Finisher Activities

7. CONTINGENCY PLANS
- Alternative Activities
- Technical Backup Plans
- Time Management Adjustments

Begin lesson plan generation:"""


    def _create_higher_ed_prompt(
        self,
        tool_input: UnifiedLessonPlanInput,
        content_text: str,
        sources: List[str],
        time_allocation: Dict[str, int]
    ) -> str:
        """Create higher education specific lesson plan prompt"""
        
        # Build course context information
        context_lines = [
            f"Academic Level: {tool_input.education_level}",
            f"Delivery Mode: {tool_input.delivery_mode}"
        ]
        
        # Add optional fields only if they exist
        if tool_input.course_code:
            if tool_input.subject:
                context_lines.insert(0, f"Course: {tool_input.course_code} - {tool_input.subject}")
            else:
                context_lines.insert(0, f"Course: {tool_input.course_code}")
        else:
            context_lines.insert(0, f"Subject: {tool_input.subject}")
            
        if tool_input.credits:
            context_lines.append(f"Credits: {tool_input.credits}")
            
        if tool_input.prerequisites:
            prereqs = ", ".join(tool_input.prerequisites)
            context_lines.append(f"Prerequisites: {prereqs}")
        
        if tool_input.student_count:
            context_lines.append(f"Class Size: {tool_input.student_count}")
            
        # Join context lines with newlines
        course_context = "\n".join(context_lines)
        
        return f"""You are a higher education instructional designer creating a {tool_input.duration}-minute 
session plan for {tool_input.subject}.

COURSE CONTEXT:
{course_context}

CONTENT RESOURCES:
{content_text}

REFERENCE MATERIALS:
{chr(10).join(sources)}

SESSION PLAN STRUCTURE:

1. SESSION OVERVIEW
- Course Information & Context
- Session Learning Outcomes (3-4 specific, measurable outcomes)
- Connection to Course Objectives
- Prerequisites Review

2. PREPARATION & RESOURCES
- Required Materials
- Technology Requirements
- Pre-session Setup
- Student Preparation Requirements
- Supplementary Resources

3. SESSION FLOW
a) Introduction & Context Setting ({time_allocation['introduction']} minutes)
   - Topic Introduction
   - Relevance & Application
   - Learning Outcomes Review
   - Prior Knowledge Activation

b) Primary Content Delivery ({time_allocation['main_content']} minutes)
   - Key Concepts Presentation
   - Theoretical Framework
   - Examples & Applications
   - Critical Analysis Points
   - Research Connections

c) Interactive Components ({time_allocation['practice']} minutes)
   - Discussion Points
   - Applied Activities
   - Case Studies/Problem Solving
   - Peer Learning Opportunities
   - Skill Development Exercises

d) Synthesis & Assessment ({time_allocation['wrap_up']} minutes)
   - Key Concepts Review
   - Learning Verification
   - Future Applications
   - Next Session Preview

4. ENGAGEMENT STRATEGIES
- Active Learning Techniques
- Discussion Facilitation Methods
- Group Work Structure
- Student Participation Mechanisms
- Online/Hybrid Engagement Tools

5. ACCESSIBILITY & INCLUSION
- Universal Design for Learning Principles
- Accommodations Framework
- Diverse Learning Support
- Cultural Responsiveness
- Language Considerations

6. ASSESSMENT APPROACH
- Formative Assessment Methods
- Learning Evidence Collection
- Feedback Mechanisms
- Rubrics/Evaluation Criteria
- Self-Assessment Tools

7. SESSION EXTENSIONS
- Additional Reading Materials
- Research Connections
- Industry Applications
- Professional Development Links

8. ACADEMIC SUPPORT
- Office Hours Information
- Resource Access Details
- Support Services Links
- Study Group Facilitation

9. CONTINGENCY PLANNING
- Technical Alternatives
- Time Management Strategies
- Backup Activities
- Alternative Delivery Methods

Begin session plan generation:"""


def create_unified_lesson_planner_tool(
    bot: BotModel,
    model: type_model_name
) -> AgentTool:
    """Create an instance of the unified lesson planner tool"""
    return UnifiedLessonPlannerTool(bot, model)