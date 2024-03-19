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