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
