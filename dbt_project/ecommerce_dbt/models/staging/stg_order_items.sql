select
    order_id,
    order_item_id,
    product_id,
    seller_id,
    cast(price as numeric) as price,
    cast(freight_value as numeric) as freight_value
from {{ source('raw', 'raw_order_items') }}
