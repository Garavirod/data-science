/*
  Engine: Mysql
  Level: easy
  https://www.hackerrank.com/challenges/african-cities/problem
*/
select name from city 
    where countrycode in (
        select code from country where continent = 'Africa'
    );
