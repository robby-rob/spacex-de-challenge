/*
Which payload nationality has been on the most launches? List nationalities and the count 
of launches that the nationality has been up on from most to least launches.
*/

/*
# data structures

payloads have:
    - launch
    - nationalities:
        - nationality

launches have:
    - upcoming

*/

with
-- tables
payload as (
    select * from raw_payloads
),
launch as (
    select * from raw_launches
),

-- prep
past_nationality_payloads as (
    select
        unnest(payload.nationalities::VARCHAR[]) as nationality,
        payload.launch
    from
        payload
        inner join launch
            on payload.launch = launch.id
    where
        launch.upcoming = False
)

-- ouput
select
    nationality,
    count(distinct launch) as payload_launch_count
from
    past_nationality_payloads
group by
    nationality
order by
    2 desc;