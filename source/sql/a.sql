/*
Which drone ships has received the most successful successive landings by falcon 9 booster?
List landing drone ships in order from most successful successive landings to least.
*/

/*
# data structures

landpads have:
    - launches
    - name
    - type

launches have:
    - cores:
        - landing attempts
        - landing success
        - landing type
    - date
    - rockets

rockets have:
    - name

# notes
ASDS ship types are drone ship landing pads

*/

with
-- tables
launch as (
    select * from raw_launches
),
rocket as (
    select * from raw_rockets
),
landpad as (
    select * from raw_landpads
),

-- prep
past_falcon9_launch as (
    select
        date_utc::timestamp as date_utc,
        unnest(cores::varchar[])::json as core
    from
        launch
        inner join rocket
            on launch.rocket = rocket.id
    where
        upcoming != True
        and rocket.name = 'Falcon 9'
),

falcon9_droneship_landing as (
    select
        date_utc,
        core->>'landpad' as core_landpad,
        case core->>'landing_success'
            when 'true' then 1
            when 'false' then 0
            else null
        end::boolean as core_landing_success
    from
        past_falcon9_launch
    where
        core->>'landing_type' = 'ASDS'
),

droneship_landings_group as (
    select
        core_landpad,
        date_utc,
        core_landing_success,
        (
            row_number() over (
                partition by core_landpad
                order by date_utc asc
            )
            - row_number() over (
                partition by core_landpad, core_landing_success
                order by date_utc asc
            )
        ) as successive_group
    from
        falcon9_droneship_landing
    where
        core_landing_success is not null
),

droneship_landing_rank as (
    select
        core_landpad,
        date_utc,
        core_landing_success,
        row_number() over (partition by core_landpad, successive_group order by date_utc asc) landing_rank
    from
        droneship_landings_group
)

-- output
select
    landpad.full_name::varchar as droneship_name,
    max(landing.landing_rank) as successful_successive_landings
from
    droneship_landing_rank as landing
    inner join landpad
        on landing.core_landpad = landpad.id
where
    landing.core_landing_success = True
group by
    landpad.full_name
order by
    2 desc;
