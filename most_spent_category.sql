SELECT 
	c."name",
	SUM(p.amount) AS total_spent
FROM 
	public.film_category fc
INNER JOIN public.category c 
ON 
	fc.category_id = c.category_id 
INNER JOIN public.inventory i 
ON 
	fc.film_id = i.film_id 
INNER JOIN public.rental r
ON 
	i.inventory_id = r.inventory_id 
INNER JOIN public.payment p 
ON
	r.rental_id = p.rental_id
GROUP BY
	c."name"
ORDER BY 
	SUM(p.amount) DESC
LIMIT 1;