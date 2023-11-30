select CO.continent, floor(avg(CI.population))
from country as CO
inner join city as CI
    on CO.code = CI.countrycode
group by CO.continent;
