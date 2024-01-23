/*
For every admission, display the patient's full name, their admission diagnosis,
 and their doctor's full name who diagnosed their problem.
*/

-- Solution
select
  P.first_name || ' ' || P.last_name as patient_full_name,
  diagnosis,
  D.first_name || ' ' || D.last_name as doctor_full_name
from patients as P
  inner join admissions AD on P.patient_id = AD.patient_id
  inner join doctors D on AD.attending_doctor_id = D.doctor_id