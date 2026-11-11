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