from typing import List

from boto3.dynamodb.conditions import Key

from models.crm_items import User
from models.dynamo_items import (UserEventCount, UserPersonalInfo,
                                 UserProfessionalInfo)
from models.query_inputs import UserQueryInput
from utils.logger_utils import get_logger

logger = get_logger(__name__)


async def create_user(user: User):
    logger.info(f"Creating user: {user}")
    user_personal_info, user_professional_info = user.to_dynamo_item()
    user_event_count = UserEventCount(id=user.id, hostedEvents=0, attendedEvents=0)

    UserPersonalInfo.put_item(user_personal_info.to_payload())
    UserProfessionalInfo.put_item(user_professional_info.to_payload())
    UserEventCount.put_item(user_event_count.to_payload())
    logger.info(f"User personal info: {user_personal_info}")
    logger.info(f"User professional info: {user_professional_info}")
    logger.info(f"User event count: {user_event_count}")


async def get_user_based_on_query(queries: List[UserQueryInput]):
    logger.info(f"Getting users based on queries: {queries}")
    responses = []
    for query in queries:
        if query.company:
            response = await get_user_based_on_company(
                query.company, query.limit, query.last_evaluated_key, query.ascending
            )
        elif query.jobTitle:
            response = await get_user_based_on_job_title(
                query.jobTitle, query.limit, query.last_evaluated_key, query.ascending
            )
        elif query.city and query.state:
            response = await get_user_based_on_city_state(
                query.city,
                query.state,
                query.limit,
                query.last_evaluated_key,
                query.ascending,
            )
        elif query.minEventAttendedCount and query.maxEventAttendedCount:
            response = await get_user_based_on_attended_events(
                query.minEventAttendedCount,
                query.maxEventAttendedCount,
                query.limit,
                query.last_evaluated_key,
                query.ascending,
            )
        elif query.minEventHostCount and query.maxEventHostCount:
            response = await get_user_based_on_hosted_events(
                query.minEventHostCount,
                query.maxEventHostCount,
                query.limit,
                query.last_evaluated_key,
                query.ascending,
            )
        users = []
        for item in response["Items"]:
            user = await get_user_by_id(item["PK"])
            users.append(user)
        if query.pagination:
            last_evaluated_key = response.get("LastEvaluatedKey")
            responses.append({"users": users, "last_evaluated_key": last_evaluated_key})
        else:
            responses.append({"users": users})
    return responses


async def get_user_based_on_company(
    company: str, limit: int, last_evaluated_key: dict, ascending: bool
):
    logger.info(f"Getting users based on company: {company}")
    response = UserPersonalInfo.query_item(
        index_name="GSI_Company",
        key_condition_expression=Key("company").eq(company),
        limit=limit,
        last_evaluated_key=last_evaluated_key,
        ascending=ascending,
    )
    return response


async def get_user_based_on_job_title(
    job_title: str, limit: int, last_evaluated_key: dict, ascending: bool
):
    logger.info(f"Getting users based on job title: {job_title}")
    response = UserProfessionalInfo.query_item(
        index_name="GSI_JobTitle",
        key_condition_expression=Key("jobTitle").eq(job_title),
        limit=limit,
        last_evaluated_key=last_evaluated_key,
        ascending=ascending,
    )
    return response


async def get_user_based_on_city_state(
    city: str, state: str, limit: int, last_evaluated_key: dict, ascending: bool
):
    logger.info(f"Getting users based on city: {city} and state: {state}")
    response = UserProfessionalInfo.query_item(
        index_name="GSI_CityState",
        key_condition_expression=Key("city").eq(city) & Key("state").eq(state),
        limit=limit,
        last_evaluated_key=last_evaluated_key,
        ascending=ascending,
    )
    return response


async def get_user_based_on_hosted_events(
    min_hosted_events: int,
    max_hosted_events: int,
    limit: int,
    last_evaluated_key: dict,
    ascending: bool,
):
    logger.info(
        f"Getting users based on hosted events: {min_hosted_events} to {max_hosted_events}"
    )
    response = UserEventCount.query_item(
        index_name="GSI_HostedEvents",
        key_condition_expression=Key("hostedEvents").between(
            min_hosted_events, max_hosted_events
        ),
        limit=limit,
        last_evaluated_key=last_evaluated_key,
        ascending=ascending,
    )
    return response


async def get_user_based_on_attended_events(
    min_attended_events: int,
    max_attended_events: int,
    limit: int,
    last_evaluated_key: dict,
    ascending: bool,
):
    logger.info(
        f"Getting users based on attended events: {min_attended_events} to {max_attended_events}"
    )
    response = UserEventCount.query_item(
        index_name="GSI_AttendedEvents",
        key_condition_expression=Key("attendedEvents").between(
            min_attended_events, max_attended_events
        ),
        limit=limit,
        last_evaluated_key=last_evaluated_key,
        ascending=ascending,
    )
    return response


async def update_user_hosted_events(user_id: str):
    logger.info(f"Updating user hosted events: {user_id}")
    UserEventCount.update_item(
        key=f"USER#{user_id}",
        sort_key="USEREVENTCOUNT",
        update_expression="SET hostedEvents = if_not_exists(hostedEvents, :start) + :inc",
        expression_attribute_values={":start": 0, ":inc": 1},
    )


async def update_user_attended_events(user_id: str):
    logger.info(f"Updating user attended events: {user_id}")
    UserEventCount.update_item(
        key=f"USER#{user_id}",
        sort_key="USEREVENTCOUNT",
        update_expression="SET attendedEvents = if_not_exists(attendedEvents, :start) + :inc",
        expression_attribute_values={":start": 0, ":inc": 1},
    )


async def get_user_by_id(user_id: str):
    logger.info(f"Getting user by id: {user_id}")
    user_personal_info = UserPersonalInfo.query_item(
        key_condition_expression=Key("PK").eq(user_id) & Key("SK").eq("USERINFO")
    )["Items"][0]
    user_professional_info = UserProfessionalInfo.query_item(
        key_condition_expression=Key("PK").eq(user_id) & Key("SK").eq("USERPROF")
    )["Items"][0]
    user_event_count = UserEventCount.query_item(
        key_condition_expression=Key("PK").eq(user_id) & Key("SK").eq("USEREVENTCOUNT")
    )["Items"][0]
    user = {**user_personal_info, **user_professional_info, **user_event_count}
    user.pop("PK", None)
    user.pop("SK", None)
    user["attendedEvents"] = int(user["attendedEvents"])
    user["hostedEvents"] = int(user["hostedEvents"])
    return user
