select 
    (
        case 
            when (g.grade >= 8) then s.name
            else 'NULL'
        end
    ) as name, g.grade, s.marks
from students as s
join grades as g
on s.marks between g.min_mark and g.max_mark
order by g.grade desc, name asc, s.marks asc;
