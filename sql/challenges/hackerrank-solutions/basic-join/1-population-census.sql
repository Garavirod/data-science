/*
  Level: Easy
  Engine: Mysql 
  https://www.hackerrank.com/challenges/asian-population/problem?isFullScreen=true
*/
select sum(population) from city 
  where countrycode in (
    select code from country where continent = 'Asia'
  );
