/*
Show patient_id, first_name, last_name from patients whos diagnosis is 'Dementia'.
Primary diagnosis is stored in the admissions table.
*/

-- solution 1
select patient_id, first_name, last_name from patients 
where patient_id in (
	select patient_id from admissions where diagnosis = 'Dementia'
)
