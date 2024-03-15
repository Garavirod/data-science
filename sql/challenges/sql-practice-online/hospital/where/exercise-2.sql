
-- Show patient_id and first_name from patients where their first_name start and ends with 's' and is at least 6 characters long.

-- Solution 1
SELECT patient_id, first_name 
from patients where (
  first_name like "_%s" and 
  first_name like "s%_" and
  len(first_name) >= 6
) 

-- Solution 2

SELECT
  patient_id,
  first_name
FROM patients
WHERE first_name LIKE 's____%s'; -- The 4 underscores means the length by by default


-- solution 3

SELECT
  patient_id,
  first_name
FROM patients
WHERE
  first_name LIKE 's%s'
  AND len(first_name) >= 6;