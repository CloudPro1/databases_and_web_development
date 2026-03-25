SELECT drivers.name, route_id, date_of_workday, work_start, work_finish
FROM drivers
LEFT JOIN schedule USING(dr_id)
WHERE date_of_workday = %s