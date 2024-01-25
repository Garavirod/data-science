/*

*/

-- solution 1
SELECT pr.province_name
FROM patients AS pa
  JOIN province_names AS pr ON pa.province_id = pr.province_id
GROUP BY pr.province_name
HAVING
  COUNT( CASE WHEN gender = 'M' THEN 1 END) > COUNT( CASE WHEN gender = 'F' THEN 1 END);

-- Solution 2
with more_male_than_female as (
    SELECT
      province_name,
      SUM(gender = 'M') AS n_male,
      SUM(gender = 'F') AS n_female
    FROM patients pa
      JOIN province_names pr ON pa.province_id = pr.province_id
    GROUP BY province_name
  )
select province_name from more_male_than_female
where n_male > n_female
-- solution 3
SELECT pr.province_name
FROM patients AS pa
  JOIN province_names AS pr ON pa.province_id = pr.province_id
GROUP BY pr.province_name
HAVING
  SUM(gender = 'M') > SUM(gender = 'F');

-- Solution 4
SELECT province_name
FROM patients p
  JOIN province_names r ON p.province_id = r.province_id
GROUP BY province_name
HAVING
  SUM(CASE WHEN gender = 'M' THEN 1 ELSE -1 END) > 0