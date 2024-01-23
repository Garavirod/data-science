with 

completed as (

  SELECT  'user_id' as ORDERS, COUNT(*) as completed
  FROM topic_grafena
  WHERE status = 'COMPLETED'

)

, total AS (

  SELECT  'user_id' as ORDERS, COUNT(*) as completed
  FROM topic_grafena
)


select ROUND(CAST(c.completed as DOUBLE)/CAST(t.completed as DOUBLE),4)*100 as completed_percent
from completed c
INNER JOIN total t on c.ORDERS = t.ORDERS