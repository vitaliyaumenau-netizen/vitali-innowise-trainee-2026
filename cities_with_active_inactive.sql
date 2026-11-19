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
	