/*
    Display the total amount of patients for each province. Order by descending.
*/

-- Solution
select
  PN.province_name,
  count(*) as num_patients
from patients as PA
  inner join province_names PN on PA.province_id = PN.province_id
group by province_name
order by num_patients desc