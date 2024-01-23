
/*
All patients who have gone through admissions, can see their medical documents on our site. Those patients are given a temporary password after their first admission. Show the patient_id and temp_password.

The password must be the following, in order:
1. patient_id
2. the numerical length of patient's last_name
3. year of patient's birth_date
*/

-- Solution 1
select
  distinct P.patient_id,
  P.patient_id || '' || cast(len(P.last_name) AS int) || '' || cast(year(P.birth_date) as int) as temp_password
from patients as P
  inner join admissions AD on AD.patient_id = P.patient_id

-- Solution 2
  select
  distinct p.patient_id,
  p.patient_id || floor(len(last_name)) || floor(year(birth_date)) as temp_password
from patients p
  join admissions a on p.patient_id = a.patient_id

-- Solution 3
select
  pa.patient_id,
  ad.patient_id || floor(len(pa.last_name)) || floor(year(pa.birth_date)) as temp_password
from patients pa
  join admissions ad on pa.patient_id = ad.patient_id
group by pa.patient_id;