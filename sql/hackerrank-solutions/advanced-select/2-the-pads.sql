/* 
    level: easy
    engine: Mysql server
*/

select name + "(" + left(occupation, 1) + ")" 
from occupations 
order by name 

select "There are a total of ", count(occupation) as cnt, lower(occupation) + "s." 
from occupations 
group by occupation 
order by cnt, occupation;