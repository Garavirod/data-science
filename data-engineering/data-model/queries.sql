-- Find the revenue of all films that were rent 

select sum(p.amount) as revenue, f.title from payment as p
inner join rental as r on r.rental_id=p.rental_id
inner join inventory as i on r.inventory_id = i.inventory_id
inner join film as f on f.film_id = i.film_id
group by f.title
order by revenue DESC