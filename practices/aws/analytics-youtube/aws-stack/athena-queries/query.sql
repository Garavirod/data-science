-- Query 1 

select * distinct(channel_name)
FROM "channel_stats"."youtube_stats_demo" 
WHERE channel_name = ''; -- channel name

-- Query 2
WITH STATS AS (
    SELECT channel_name
            ,subscribers
            ,lag(subscribers,1) over (order by createt_at) as prev_susc
            ,video_count
            ,lag(video_count,1) over (order by createt_at) as prev_videoc
            ,lag(total_views,1) over (order by createt_at) as prev_viewsc
            ,total_views
            ,createt_at
    FROM "channel_stats"."youtube_stats_demo" 
    WHERE channel_name = '' -- channel name
    order by createt_at desc )
            
SELECT channel_name
       ,total_views
       ,prev_viewsc
       ,((cast(total_views as decimal(16,5)) / cast(prev_viewsc as decimal(16,5))) -1 ) *100 as change_views
       ,createt_at
FROM STATS
;

-- Query Final
WITH STATS AS (
    SELECT channel_name
            ,subscribers
            ,lag(subscribers,1) over (order by createt_at) as prev_susc
            ,video_count
            ,lag(video_count,1) over (order by createt_at) as prev_videoc
            ,total_views
            ,lag(total_views,1) over (order by createt_at) as prev_viewsc
            ,createt_at
    FROM "channel_stats"."youtube_stats_demo" 
    WHERE channel_name = '' -- channel name
    order by createt_at desc )
            
SELECT channel_name
       ,subscribers - prev_susc as qty_susc
       ,((cast(subscribers as decimal(16,5)) / cast(prev_susc as decimal(16,5))) -1 ) *100 as grow_susc
       ,video_count - prev_videoc as qty_videos
       ,((cast(video_count as decimal(16,5)) / cast(prev_videoc as decimal(16,5))) -1 ) *100 as grow_videos
       ,total_views - prev_viewsc as qty_views
       ,((cast(total_views as decimal(16,5)) / cast(prev_viewsc as decimal(16,5))) -1 ) *100 as grow_views
       ,createt_at
FROM STATS
;