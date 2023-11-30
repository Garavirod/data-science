/*  
  level: medium
  engine: mysql
  https://www.hackerrank.com/challenges/full-score/problem
*/
select s.hacker_id, h.name  from submissions as s 
    inner join challenges as c 
    on s.challenge_id=c.challenge_id
    inner join difficulty as d 
    on d.difficulty_level=c.difficulty_level
    inner join hackers as h 
    on h.hacker_id=s.hacker_id 
where d.score=s.score 
group by s.hacker_id,h.name 
having count(*)>1 
order by count(*) desc, s.hacker_id;
