/*
Show patient_id, diagnosis from admissions. Find patients admitted multiple times for the same diagnosis.
*/

-- Solution
select patient_id,diagnosis from admissions
group by patient_id, diagnosis
having count(*) > 1