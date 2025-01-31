-- models/my_transformation.sql
with raw_data as (
    select 
        id,
        channel_title,
        channel_username,
        message_id,
        message,
        message_date,
        emoji_used,
        youtube_links
    from {{ source('telegram_data', 'telegram_messages') }}
    where message_date > '2023-01-01'
)

select 
    id,
    channel_title,
    channel_username,
    message_id,
    message,
    message_date,
    emoji_used,
    youtube_links
from raw_data
