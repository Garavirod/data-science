/*
Show the difference between the largest weight and smallest weight for patients with the last name 'Maroni'
*/

-- Solution 1

select (max(weight) - min(weight)) from patients 
where last_name = 'Maroni'