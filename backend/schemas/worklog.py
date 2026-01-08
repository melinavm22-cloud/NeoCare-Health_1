from pydantic import BaseModel, Field, field_validator
from datetime import date as date_type, datetime
from typing import Optional

class WorklogCreate(BaseModel):
    """Schema for creating a new worklog"""
    date: date_type = Field(..., description="Date of the work (cannot be in the future)")
    hours: float = Field(..., gt=0, description="Hours worked (must be greater than 0)")
    note: Optional[str] = Field(None, max_length=200, description="Optional note (max 200 characters)")

    @field_validator('date')
    @classmethod
    def validate_date_not_future(cls, v: date_type) -> date_type:
        from datetime import date as today_date
        if v > today_date.today():
            raise ValueError('Date cannot be in the future')
        return v

    @field_validator('hours')
    @classmethod
    def validate_hours_minimum(cls, v: float) -> float:
        if v < 0.25:
            # Warning: minimum recommended is 0.25
            pass  # Not enforcing, just validating > 0 which is done by Field(gt=0)
        return v

class WorklogUpdate(BaseModel):
    """Schema for updating a worklog (only hours and note can be updated)"""
    hours: Optional[float] = Field(None, gt=0, description="Hours worked (must be greater than 0)")
    note: Optional[str] = Field(None, max_length=200, description="Optional note (max 200 characters)")

class WorklogOut(BaseModel):
    """Schema for worklog output"""
    id: int
    card_id: int
    user_id: int
    date: date_type
    hours: float
    note: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WeeklyWorklogResponse(BaseModel):
    """Schema for weekly worklog summary"""
    week: str = Field(..., description="Week in ISO format (YYYY-WW)")
    total_week_hours: float = Field(..., description="Total hours for the week")
    daily_totals: dict[str, float] = Field(..., description="Hours per day")
    worklogs: list[WorklogOut] = Field(..., description="List of worklogs for the week")
