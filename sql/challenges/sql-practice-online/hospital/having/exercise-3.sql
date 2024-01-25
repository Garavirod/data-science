/*
Show the province_id(s), sum of height; where the total sum of its patient's height 
is greater than or equal to 7,000.
*/


-- Solution 1
select province_id, sum(height) as hs from patients
group by province_id
having hs > 7000