/*
Show patient_id, first_name, last_name from patients whos diagnosis is 'Dementia'.
*/

-- Solution 1
with dementia_patiants as (
	select patient_id from admissions where diagnosis = 'Dementia'
)

select P.patient_id, P.first_name, P.last_name from patients as P
inner join dementia_patiants d on d.patient_id = P.patient_id

-- Solution 2
SELECT
  patients.patient_id,
  first_name,
  last_name
FROM patients
  INNER JOIN admissions ON admissions.patient_id = patients.patient_id
WHERE diagnosis = 'Dementia';

-- Solution 3
SELECT
  patient_id,
  first_name,
  last_name
FROM patients
WHERE patient_id IN (
    SELECT patient_id
    FROM admissions
    WHERE diagnosis = 'Dementia'
  );