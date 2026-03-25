SELECT drivers.name, date_of_workday
FROM drivers
LEFT JOIN schedule USING(dr_id)
WHERE route_id = %s AND YEAR(date_of_workday) = %s AND MONTH(date_of_workday) = %s