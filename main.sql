SELECT 
	c."name", 
	COUNT(fc.film_id)
FROM
	public.film_category fc
INNER JOIN category c 
ON
	c.category_id = fc.category_id
GROUP BY 
	c."name"
ORDER BY 
	COUNT(fc.film_id) DESC;


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


SELECT 
    f.title
FROM 
    public.film f
WHERE 
    NOT EXISTS (
        SELECT 1 
        FROM public.inventory i 
        WHERE i.film_id = f.film_id
    );


SELECT 
	ai.first_name,
	ai.last_name
FROM 
	public.actor_info ai
ORDER BY 
	COALESCE(JSONB_ARRAY_LENGTH(ai.film_info -> 'Children'), 0) DESC
LIMIT 3;


SELECT 
	COUNT(*) FILTER (WHERE active = 1) AS active_count,
	COUNT(*) FILTER (WHERE active = 0) AS inactive_count,
	cl.city
FROM 
	public.customer c
INNER JOIN public.customer_list cl  
ON 
	c.customer_id = cl.id
GROUP BY 
	cl.city
ORDER BY 
	inactive_count DESC;
	

WITH highest_number_of_total_rental AS (
	SELECT 
		c."name",
		c3.city,
		SUM(r.return_date - r.rental_date) AS total_rental_hours_in_the_city
	FROM 
		public.category c
	INNER JOIN public.film_category fc 
	ON 
		c.category_id = fc.category_id
	INNER JOIN public.inventory i 
	ON 
		fc.film_id = i.film_id
	INNER JOIN public.rental r 
	ON 
		r.inventory_id = i.inventory_id
	INNER JOIN public.customer c2 
	ON 
		c2.customer_id = r.customer_id 
	INNER JOIN public.address a
	ON 
		c2.address_id = a.address_id
	INNER JOIN public.city c3 
	ON 
		a.city_id = c3.city_id
		AND (
			c3.city LIKE 'a%'
			OR 
			c3.city LIKE '%-%'
		)
	GROUP BY 
		c3.city,
		c."name"
	ORDER BY 
		total_rental_hours_in_the_city DESC NULLS LAST
	
)	
(
	SELECT 
		name
	FROM
		highest_number_of_total_rental
	WHERE 
		city LIKE 'a%'
	LIMIT 1
)
	
UNION ALL

(
	SELECT 
		name
	FROM highest_number_of_total_rental
	WHERE 
		city LIKE '%-%'
	LIMIT 1
);
	
