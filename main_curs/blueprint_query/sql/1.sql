SELECT sr_id, drivers.name, sr_year, sr_month, workhours_sum
FROM drivers
LEFT JOIN salary_report USING(dr_id)
WHERE drivers.name = %s
