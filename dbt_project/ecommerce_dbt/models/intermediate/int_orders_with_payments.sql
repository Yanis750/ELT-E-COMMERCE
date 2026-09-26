select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchase_ts,
    p.payment_type,
    p.payment_value
from {{ ref('stg_orders') }} o
left join {{ ref('stg_payments') }} p
    on o.order_id = p.order_id