SELECT
    COUNT(appointment_id)
FROM
    fact_appointments
WHERE
    appointment_status = 'attended';

SELECT
    COUNT(appointment_id)
FROM
    fact_appointments
WHERE
    appointment_status IN ('missed', 'cancelled');

SELECT
    EXTRACT(
        YEAR
        FROM
            appointment_date
    ) AS year,
    COALESCE(
        SUM(
            CASE
                WHEN appointment_status = 'attended' THEN 1
                ELSE 0
            END
        ),
        0
    ) AS attended,
    COALESCE(
        SUM(
            CASE
                WHEN appointment_status IN ('missed', 'cancelled') THEN 1
                ELSE 0
            END
        ),
        0
    ) AS cancelled
FROM
    fact_appointments
GROUP BY
    EXTRACT(
        YEAR
        FROM
            appointment_date
    )
ORDER BY
    year;