/* Show first name, last name, and the full province name of each patient. */
select first_name, last_name, province_name from patients as PA
join province_names as P 
where P.province_id = PA.province_id