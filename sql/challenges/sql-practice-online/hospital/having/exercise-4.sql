/*
Show all columns for patient_id 542's most recent admission_date.
*/

-- Solution 1
select * from admissions
group by patient_id
having patient_id = 542 and max(admission_date)

-- Solution 2
SELECT *
FROM admissions
WHERE patient_id = 542
GROUP BY patient_id
HAVING
  admission_date = MAX(admission_date);