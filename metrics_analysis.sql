drop table if exists businesspopularity;

create table businesspopularity as (
select b.business_id, b.business_name, hc.category_type, b.business_avg_star, b.num_of_tips, b.num_of_checkins, (b.num_of_checkins + b.num_of_tips) * b.business_avg_star as popularity_rating 
from business as b
	join hascategory as hc on b.business_id = hc.business_id
group by b.business_id, b.business_name, hc.category_type, b.business_avg_star, b.num_of_tips, b.num_of_checkins
);
