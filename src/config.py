from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    aws_region: str = "ap-southeast-1"
    aws_dynamodb_table_name_events: str = "crm-events-table"
    aws_dynamodb_table_name_users: str = "crm-users-table"
    aws_ses_sender_email: str = "noreply@example.com"
    aws_ses_config_set: str = "crm-config-set"

settings = Setting()