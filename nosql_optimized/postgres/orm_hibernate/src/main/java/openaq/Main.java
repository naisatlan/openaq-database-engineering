package openaq;

import org.hibernate.Session;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Main {

    static Map<String, Double> queryTimings = new LinkedHashMap<>();

    public static void main(String[] args) throws Exception {

        Files.createDirectories(Paths.get("results"));

        try (Session session = HibernateUtil.getSessionFactory().openSession()) {

            exportLastMeasures(session, 13866, 20);
            exportStationProfiles(session);
            exportRolling24h(session);
            exportPollutionSpikes(session, 600);

            printQueryTimings();
        }

        HibernateUtil.getSessionFactory().close();
    }

    static void printQueryTimings() {
        System.out.println("\nQuery execution times (ms):");
        for (var e : queryTimings.entrySet()) {
            System.out.printf("  %s: %.2f ms%n", e.getKey(), e.getValue());
        }
    }

    static void exportLastMeasures(Session session, int sensorId, int limit) throws IOException {
        long t0 = System.currentTimeMillis();

        String sql = """
            SELECT CAST(timestamp AS TEXT) AS ts,
                   value,
                   raw->'location'->>'city' AS city,
                   raw->'sensor'->>'parameter' AS parameter
            FROM measurements
            WHERE CAST(raw->'sensor'->>'id' AS INTEGER) = %d
            ORDER BY timestamp DESC
            LIMIT %d
        """.formatted(sensorId, limit);

        List<Object[]> rows = session.createNativeQuery(sql).getResultList();

        queryTimings.put("last_measures", (double)(System.currentTimeMillis() - t0));
        writeCsv("last_measures.csv", rows, "timestamp,value,city,parameter");
    }

    static void exportStationProfiles(Session session) throws IOException {
        long t0 = System.currentTimeMillis();

        List<Object[]> rows = session.createNativeQuery("""
            SELECT CAST(raw->'sensor'->>'id' AS INTEGER) AS sensor_id,
                   AVG(value) AS avg_pm10,
                   STDDEV_POP(value) AS std_pm10
            FROM measurements
            GROUP BY CAST(raw->'sensor'->>'id' AS INTEGER)
            ORDER BY avg_pm10 DESC
        """).getResultList();

        queryTimings.put("station_profiles", (double)(System.currentTimeMillis() - t0));
        writeCsv("station_profiles.csv", rows, "sensor_id,avg_pm10,std_pm10");
    }

    static void exportRolling24h(Session session) throws IOException {
        long t0 = System.currentTimeMillis();

        List<Object[]> rows = session.createNativeQuery("""
            WITH last_ts AS (SELECT MAX(timestamp) AS tmax FROM measurements)
            SELECT raw->'location'->>'city' AS city,
                   AVG(value) AS avg_pm10,
                   COUNT(*) AS count
            FROM measurements, last_ts
            WHERE timestamp BETWEEN last_ts.tmax - INTERVAL '24 hours' AND last_ts.tmax
            GROUP BY raw->'location'->>'city'
            ORDER BY avg_pm10 DESC
        """).getResultList();

        queryTimings.put("rolling_last_24h_available", (double)(System.currentTimeMillis() - t0));
        writeCsv("rolling_last_24h_available.csv", rows, "city,avg_pm10,count");
    }

    static void exportPollutionSpikes(Session session, double threshold) throws IOException {
        long t0 = System.currentTimeMillis();
        String sql = String.format(Locale.US, """
            SELECT raw->'location'->>'city' AS city,
                DATE_TRUNC('hour', timestamp) AS hour,
                MAX(value) AS max_value,
                COUNT(*) AS count
            FROM measurements
            WHERE value >= %.2f
            GROUP BY raw->'location'->>'city', DATE_TRUNC('hour', timestamp)
            ORDER BY max_value DESC
        """, threshold);

        List<Object[]> rows = session.createNativeQuery(sql).getResultList();

        queryTimings.put("pollution_spikes", (double)(System.currentTimeMillis() - t0));
        writeCsv("pollution_spikes.csv", rows, "city,hour,max_value,count");
    }

    // -------------------------------------------------------------

    static void writeCsv(String filename, List<Object[]> rows, String header) throws IOException {
        String path = "results/" + filename;
        try (FileWriter fw = new FileWriter(path)) {
            fw.write(header + "\n");
            for (Object[] r : rows) {
                for (int i = 0; i < r.length; i++) {
                    if (i > 0) fw.write(",");
                    fw.write(r[i] == null ? "" : r[i].toString());
                }
                fw.write("\n");
            }
        }
        System.out.println("Exported " + filename);
    }
}
