from pydantic import BaseModel, Field, ConfigDict
from tools.fakers import fake


class ExerciseSchema(BaseModel):
    """
    Описание структуры задания.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class GetExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение задания.
    """
    exercise: ExerciseSchema


class GetExercisesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка заданий.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    course_id: str = Field(alias="courseId")


class GetExercisesResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение списка заданий.
    """
    exercises: list[ExerciseSchema]


class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание задания.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    title: str = Field(default_factory=fake.sentence)
    course_id: str = Field(default_factory=fake.uuid4, alias="courseId")
    max_score: int = Field(default_factory=fake.max_score, alias="maxScore")
    min_score: int = Field(default_factory=fake.min_score, alias="minScore")
    order_index: int = Field(default_factory=fake.integer, alias="orderIndex")
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(default_factory=fake.estimated_time, alias="estimatedTime")


class CreateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания задания.
    """
    exercise: ExerciseSchema


class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление задания.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    title: str | None = Field(default_factory=fake.sentence)
    max_score: int | None = Field(default_factory=fake.max_score, alias="maxScore")
    min_score: int | None = Field(default_factory=fake.min_score, alias="minScore")
    order_index: int | None = Field(default_factory=fake.integer, alias="orderIndex")
    description: str | None = Field(default_factory=fake.text)
    estimated_time: str | None = Field(default_factory=fake.estimated_time, alias="estimatedTime")


class UpdateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления задания.
    """
    exercise: ExerciseSchema