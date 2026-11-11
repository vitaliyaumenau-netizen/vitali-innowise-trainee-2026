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