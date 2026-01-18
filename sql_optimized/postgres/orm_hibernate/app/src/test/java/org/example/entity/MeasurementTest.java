package org.example.entity;

import java.time.Instant;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class MeasurementTest {

    private Measurement measurement;
    private Sensor sensor;

    @BeforeEach
    public void setUp() {
        measurement = new Measurement();
        sensor = new Sensor();
        sensor.setId(101L);
        sensor.setParameter("pm10");
    }

    @Test
    public void testMeasurementCreation() {
        Instant timestamp = Instant.now();
        measurement.setValue(25.5);
        measurement.setTimestamp(timestamp);
        measurement.setSensor(sensor);

        assertEquals(25.5, measurement.getValue());
        assertEquals(timestamp, measurement.getTimestamp());
        assertEquals(sensor, measurement.getSensor());
        assertEquals("pm10", measurement.getSensor().getParameter());
    }

    @Test
    public void testMeasurementValue() {
        measurement.setValue(35.7);
        assertEquals(35.7, measurement.getValue());
    }

    @Test
    public void testMeasurementValueRange() {
        double[] values = {0.0, 10.5, 25.3, 50.0, 100.5};

        for (double value : values) {
            measurement.setValue(value);
            assertEquals(value, measurement.getValue());
            assertTrue(measurement.getValue() >= 0);
        }
    }

    @Test
    public void testMeasurementTimestamp() {
        Instant now = Instant.now();
        measurement.setTimestamp(now);

        assertEquals(now, measurement.getTimestamp());
    }

    @Test
    public void testMeasurementSensorRelationship() {
        Location location = new Location();
        location.setId(1L);
        location.setCity("Paris");

        Sensor sensor1 = new Sensor();
        sensor1.setId(101L);
        sensor1.setParameter("pm10");
        sensor1.setLocation(location);

        measurement.setSensor(sensor1);

        assertEquals("pm10", measurement.getSensor().getParameter());
        assertEquals("Paris", measurement.getSensor().getLocation().getCity());
    }

    @Test
    public void testMeasurementWithNegativeValue() {
        measurement.setValue(-10.0);
        assertEquals(-10.0, measurement.getValue());
    }

    @Test
    public void testMeasurementTimestampOrdering() {
        Instant t1 = Instant.parse("2024-01-01T10:00:00Z");
        Instant t2 = Instant.parse("2024-01-01T11:00:00Z");

        Measurement m1 = new Measurement();
        m1.setTimestamp(t1);
        m1.setValue(25.5);

        Measurement m2 = new Measurement();
        m2.setTimestamp(t2);
        m2.setValue(26.3);

        assertTrue(m1.getTimestamp().isBefore(m2.getTimestamp()));
    }

    @Test
    public void testMeasurementNullSensor() {
        measurement.setValue(25.5);
        measurement.setTimestamp(Instant.now());

        assertNull(measurement.getSensor());
    }

    @Test
    public void testMeasurementIdAutoGeneration() {
        assertNull(measurement.getId());
    }

    @Test
    public void testMeasurementDecimalPrecision() {
        double preciseValue = 25.123456;
        measurement.setValue(preciseValue);

        assertEquals(preciseValue, measurement.getValue());
    }
}
