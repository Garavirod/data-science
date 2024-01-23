/*
    Show first_name, last_name, and the total number of admissions attended for each doctor.
*/

-- Solution 1
with number_doc_addmissions as (
	select attending_doctor_id, count(*) as ocurrence from admissions
  	group by attending_doctor_id
)

select D.first_name, D.last_name, DA.ocurrence from doctors D
inner join number_doc_addmissions DA on D.doctor_id = DA.attending_doctor_id

-- Solution 2
select D.first_name, D.last_name, count(*) as total from admissions as A
inner join doctors D on A.attending_doctor_id = D.doctor_id
group by attending_doctor_id

-- Solution 3
SELECT
  first_name,
  last_name,
  count(*)
from
  doctors p,
  admissions a
where
  a.attending_doctor_id = p.doctor_id
group by p.doctor_id;