SELECT 
	a.actor_id,
	a.first_name,
	a.last_name,
	COUNT(r.rental_id) AS total_rental
FROM 
	public.film_actor fa
INNER JOIN public.actor a 
ON 
	a.actor_id = fa.actor_id 
INNER JOIN public.inventory i 
ON 
	i.film_id = fa.film_id 
INNER JOIN public.rental r
ON 
	r.inventory_id = i.inventory_id
GROUP BY 
	a.first_name,
	a.last_name,
	a.actor_id
ORDER BY
	COUNT(r.rental_id) DESC
LIMIT 10;