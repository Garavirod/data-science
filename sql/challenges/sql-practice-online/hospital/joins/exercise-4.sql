-- For each doctor, display their id, full name, and the first and last admission date they attended.
select doctor_id, first_name || ' ' || last_name as full_name, MIN(admission_date) as first_addmission, MAX(admission_date) as last_addmission
from admissions A
inner join doctors D on D.doctor_id = A.attending_doctor_id
group by doctor_id