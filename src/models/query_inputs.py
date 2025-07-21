from typing import Optional

from pydantic import BaseModel, model_validator


class BaseQueryInput(BaseModel):
    """
    User query input model for the application.
    """

    company: Optional[str] = None
    jobTitle: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    minEventAttendedCount: Optional[int] = None
    maxEventAttendedCount: Optional[int] = None
    minEventHostCount: Optional[int] = None
    maxEventHostCount: Optional[int] = None

    @model_validator(mode="after")
    @classmethod
    def check_city_state(cls, data):
        city = data.city
        state = data.state
        if (city and not state) or (state and not city):
            raise ValueError("Both 'city' and 'state' must be provided together.")
        return data

    @model_validator(mode="after")
    @classmethod
    def check_attended_event_count(cls, data):
        minEventAttendedCount = data.minEventAttendedCount
        maxEventAttendedCount = data.maxEventAttendedCount
        if (minEventAttendedCount and not maxEventAttendedCount) or (
            maxEventAttendedCount and not minEventAttendedCount
        ):
            raise ValueError(
                "Both 'minEventAttendedCount' and 'maxEventAttendedCount' must be provided together."
            )
        if (minEventAttendedCount and maxEventAttendedCount) and (
            minEventAttendedCount > maxEventAttendedCount
        ):
            raise ValueError(
                "minEventAttendedCount must be less than maxEventAttendedCount."
            )
        return data

    @model_validator(mode="after")
    @classmethod
    def check_hosted_event_count(cls, data):
        minEventHostCount = data.minEventHostCount
        maxEventHostCount = data.maxEventHostCount
        if (minEventHostCount and not maxEventHostCount) or (
            maxEventHostCount and not minEventHostCount
        ):
            raise ValueError(
                "Both 'minEventHostCount' and 'maxEventHostCount' must be provided together."
            )
        if (minEventHostCount and maxEventHostCount) and (
            minEventHostCount > maxEventHostCount
        ):
            raise ValueError("minEventHostCount must be less than maxEventHostCount.")
        return data

    @model_validator(mode="after")
    @classmethod
    def check_only_one_filter_group(cls, data):
        filters = []
        if data.company:
            filters.append("company")
        if data.jobTitle:
            filters.append("jobTitle")
        if data.city and data.state:
            filters.append("city_state")
        if (
            data.minEventAttendedCount is not None
            and data.maxEventAttendedCount is not None
        ):
            filters.append("attended_range")
        if data.minEventHostCount is not None and data.maxEventHostCount is not None:
            filters.append("hosted_range")

        if len(filters) == 0:
            raise ValueError(
                "You must provide exactly one filter group (e.g., company, jobTitle, city+state, etc.)"
            )
        if len(filters) > 1:
            raise ValueError(
                f"Only one filter group is allowed per query. You provided: {filters}"
            )
        return data


class UserQueryInput(BaseQueryInput):
    pagination: Optional[bool] = False
    limit: Optional[int] = 10
    ascending: Optional[bool] = True
    last_evaluated_key: Optional[dict] = None


class EmailRecipientQueryInput(BaseQueryInput):
    subject: str
    body: str
