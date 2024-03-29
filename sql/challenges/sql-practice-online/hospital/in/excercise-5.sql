/*
We are looking for a specific patient. Pull all columns for the patient who matches the following criteria:
- First_name contains an 'r' after the first two letters.
- Identifies their gender as 'F'
- Born in February, May, or December
- Their weight would be between 60kg and 80kg
- Their patient_id is an odd number
- They are from the city 'Kingston'
*/

select * from patients 
where (
	patients.first_name like '__r%' and
  	patients.gender = 'F' and
  	month(patients.birth_date) in (2, 5, 12) and
    (patients.weight between 60 and 80)and
  	patients.patient_id % 2 != 0 and
  	patients.city = 'Kingston'
)