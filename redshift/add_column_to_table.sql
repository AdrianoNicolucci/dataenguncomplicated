/*Create a new category table using the same schema from the existing sample table */
create table public.category_1 (
    catid smallint,
    catgroup varchar(10),
    catname varchar(10),
    catdesc varchar(50))

/* insert records into new table */
INSERT INTO public.category_1 (catid, catgroup, catname, catdesc)
SELECT catid, catgroup, catname, catdesc
FROM public.category

/* add new column to existing table */
ALTER TABLE public.category_1 add date_modified date;

/*update date_modified column for all rows in the table.
  You should always use a WHERE statement when update table if you want to isolate specific records.*/
update public.category_1 set date_modified = '2021-03-11'
