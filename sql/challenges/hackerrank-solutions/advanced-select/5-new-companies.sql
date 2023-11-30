/* 
    level: Medium
    engine: Mysql
    https://www.hackerrank.com/challenges/the-company/problem 
*/

select company_code, founder,
    (select count(distinct lead_manager_code) from lead_manager as LM where company_code = C.company_code), 
    (select count(distinct senior_manager_code) from senior_manager as SM where company_code = C.company_code), 
    (select count(distinct manager_code) from manager as M  where company_code = C.company_code),
    (select count(distinct employee_code) from employee as E where company_code = C.company_code)
from Compnay as C
order by company_code;
