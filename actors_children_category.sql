SELECT 
	ai.first_name,
	ai.last_name
FROM 
	public.actor_info ai
ORDER BY 
	COALESCE(JSONB_ARRAY_LENGTH(ai.film_info -> 'Children'), 0) DESC
LIMIT 3;