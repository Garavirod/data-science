/* Occupations */
/* table rotation https://stackoverflow.com/questions/71544038/using-max-with-case-when-in-mysql*/
/* table partition by field https://www.javatpoint.com/mysql-row_number-function */
/* mysql */

select 
    max(case when occupation = "Doctor" then name end),
    max(case when occupation = "Professor" then name end),
    max(case when occupation = "Singer" then name end),
    max(case when occupation = "Actor" then name end)
from (
    select occupation, name, row_number() 
    over 
    (
        partition by occupation
        order by name
    ) as row_num
    from occupations
) as t
group by row_num
order by row_num;