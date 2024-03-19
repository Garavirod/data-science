-- Find the max revenue of all films that were rent 
select sum(p.amount) as revenue, f.title from payment as p
inner join rental as r on r.rental_id=p.rental_id
inner join inventory as i on r.inventory_id = i.inventory_id
inner join film as f on f.film_id = i.film_id
group by f.title
order by revenue DESC


-- Find the top cities which are given the high revenue
select sum(P.amount) as revenue, CI.city from payment as P
inner join rental as R on R.rental_id = P.rental_id
inner join customer as C on C.customer_id = R.customer_id
inner join address as A on A.address_id = C.address_id
inner join city as CI on CI.city_id = A.city_id
group by CI.city
order by revenue DESC