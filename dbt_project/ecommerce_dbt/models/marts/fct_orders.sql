select
    order_id,
    customer_id,
    order_status,
    purchase_ts,
    sum(payment_value) as total_paid
from {{ ref('int_orders_with_payments') }}
group by 1,2,3,4