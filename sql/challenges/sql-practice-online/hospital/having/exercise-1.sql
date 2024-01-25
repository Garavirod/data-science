/*
Show unique first names from the patients table which only occurs once in the list.

For example, if two or more people are named 'John' in the first_name column then 
don't include their name in the output list. If only 1 person is named 'Leo' then include them in the output
*/

-- solution 1
with occurs_name_list as (
	SELECT first_name, count(*) as occurs FROM patients
    group by first_name
    having occurs =1
)

select first_name from
occurs_name_list

-- Solution 2
SELECT first_name
FROM patients
GROUP BY first_name
HAVING COUNT(first_name) = 1