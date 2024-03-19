-- Dimension tables creation
CREATE TABLE dimDate(
	date_key integer NOT NULL PRIMARY KEY,
	date date NOT NULL,
	year smallint NOT NULL,
	quarter smallint NOT NULL,
	month smallint NOT NULL,
	day smallint NOT NULL,
	week smallint NOT NULL,
	is_weekend BOOLEAN
);


CREATE TABLE dimCustomer(
	customer_key SERIAL PRIMARY KEY,
	customer_id smallint NOT NULL,
	first_name varchar(45) NOT NULL,
	last_name varchar(45) NOT NULL,
	email varchar(50),
	address varchar(50) NOT NULL,
	address2 varchar(50),
	district varchar(20) NOT NULL,
	city varchar(50) NOT NULL,
	country varchar(50) NOT NULL,
	postal_code varchar(10),
    phone varchar(20) NOT NULL,
    active smallint NOT NULL,
	create_date timestamp NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL
);


CREATE TABLE dimMovie
(
	movie_key SERIAL PRIMARY KEY,
	film_id smallint NOT NULL,
	title varchar(255) NOT NULL,
	description text,
	release_year year,
	language varchar(20) NOT NULL,
	original_languagee varchar(20),
	rental_duration smallint NOT NULL,
	length smallint NOT NULL,
	rating varchar(5) NOT NULL,
	spaceial_features varchar(60) NOT NULL
);


CREATE TABLE dimStore
(
	store_key SERIAL PRIMARY KEY,
	store_id smallint NOT NULL,
	address varchar(50) NOT NULL,
	address2 varchar(50),
	district varchar(20) NOT NULL,
	city varchar(50) NOT NULL,
	country varchar(50) NOT NULL,
	postal_code varchar(10),
	manager_first_name varchar(45) NOT NULL,
	manager_last_name varchar(45) NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL
);

-- Getting information
select * from information_schema.columns where table_name = 'dimdate'
select column_name, data_type from information_schema.columns where table_name = 'dimdate'


-- Population
INSERT INTO dimDate( date_key,date,year,quarter,month,day,week, is_weekend)
SELECT
	DISTINCT(TO_CHAR(payment_date :: DATE, 'yyyMMDD')::integer) as date_key, 
	date(payment_date) as date,
	EXTRACT(year from payment_date) as year,
	EXTRACT(quarter from payment_date) as quarter,
	EXTRACT(month from payment_date) as month,
	EXTRACT(day from payment_date) as day,
	EXTRACT(week from payment_date) as week,
	CASE 
		WHEN EXTRACT(ISODOW FROM payment_date) in (6,7) THEN true ELSE false END
FROM payment;


INSERT INTO dimCustomer(
    customer_key,
    customer_id,
    first_name,
    last_name,
    email,
    address,
    address2,
    district,
    city,
    country,
    postal_code,
    phone,
    active,
    create_date,
    start_date,
    end_date
    )
SELECT C.customer_id AS customer_key,
C.customer_id,
C.first_name,
C.last_name,
C.email,
A.address,
A.address2,
A.district,
CI.city,
CO.country,
postal_code,
A.phone,
C.active,
C.create_date,
now() as start_date,
now() as end_date
FROM customer as C
inner join address as A on (C.address_id = A.address_id)
inner join city as CI on (A.city_id = CI.city_id)
inner join country as CO on (CI.country_id = CO.country_id);


INSERT INTO dimStore(
    store_key,
    store_id,
    address,
    address2,
    district,
    city,
    country,
    postal_code,
    manager_first_name,
    manager_last_name,
    start_date,
    end_date
)
select S.store_id as store_key,
S.store_id,
A.address,
A.address2,
A.district,
C.city,
CO.country,
A.postal_code,
ST.first_name as manager_first_name,
ST.last_name as manager_last_name,
now() as start_date,
now() as end_date
FROM store as S
inner join staff as ST on (S.manager_staff_id = ST.staff_id)
inner join address as A on (S.address_id = A.address_id)
inner join city as C on (A.city_id = C.city_id)
inner join country as CO on (CO.country_id = C.country_id);