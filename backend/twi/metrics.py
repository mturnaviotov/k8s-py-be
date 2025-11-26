from prometheus_client import Counter

POST_OPERATIONS_TOTAL = Counter(
    'post_operations_total', 
    'Total number of CRUD operations on the Post model', 
    # Label дозволяє розділяти метрики за типом операції
    ['operation_type'] 
)