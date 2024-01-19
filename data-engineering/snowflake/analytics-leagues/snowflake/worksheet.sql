CREATE STAGE "FOOTBALL_ANALYTICS_BDD"."PUBLIC".demo_stage;
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
CREATE OR REPLACE TABLE football_leagues (
id                  VARCHAR (30) NOT NULL,
team                VARCHAR (30) NOT NULL,
played              INTEGER NOT NULL,
won                 INTEGER NOT NULL,
tied                INTEGER NOT NULL,
lost                INTEGER NOT NULL,
goals_favor         INTEGER NOT NULL,
goals_against       INTEGER NOT NULL,
diff                INTEGER NOT NULL,
scores              INTEGER NOT NULL,
league              VARCHAR (30) NOT NULL,
created_at          VARCHAR (30) NOT NULL
);

-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

list @demo_stage;

select *
from "FOOTBALL_ANALYTICS_BDD"."PUBLIC"."FOOTBALL_LEAGUES";