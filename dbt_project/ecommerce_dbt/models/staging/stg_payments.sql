select
    order_id,
    payment_type,
    payment_installments,
    cast(payment_value as numeric) as payment_value
from {{ source('raw', 'raw_payments') }}
