package org.example.entity;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class SensorTest {

    private Sensor sensor;
    private Location location;

    @BeforeEach
    public void setUp() {
        sensor = new Sensor();
        location = new Location();
        location.setId(1L);
        location.setCity("Paris");
    }

    @Test
    public void testSensorCreation() {
        sensor.setId(101L);
        sensor.setParameter("pm10");
        sensor.setLocation(location);

        assertEquals(101L, sensor.getId());
        assertEquals("pm10", sensor.getParameter());
        assertEquals(location, sensor.getLocation());
        assertEquals("Paris", sensor.getLocation().getCity());
    }

    @Test
    public void testSensorWithDifferentParameters() {
        sensor.setId(102L);
        sensor.setParameter("pm25");
        sensor.setLocation(location);

        assertEquals("pm25", sensor.getParameter());
    }

    @Test
    public void testSensorMeasurementsRelationship() {
        sensor.setId(101L);
        sensor.setParameter("pm10");
        sensor.setLocation(location);

        List<Measurement> measurements = new ArrayList<>();
        measurements.add(new Measurement());
        sensor.setMeasurements(measurements);

        assertEquals(1, sensor.getMeasurements().size());
    }

    @Test
    public void testSensorWithMultipleMeasurements() {
        sensor.setId(101L);
        sensor.setParameter("pm10");

        List<Measurement> measurements = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            Measurement m = new Measurement();
            m.setValue(25.5 + i);
            measurements.add(m);
        }
        sensor.setMeasurements(measurements);

        assertEquals(10, sensor.getMeasurements().size());
    }

    @Test
    public void testSensorLocationRelationship() {
        Location loc1 = new Location();
        loc1.setId(1L);
        loc1.setCity("Paris");

        Location loc2 = new Location();
        loc2.setId(2L);
        loc2.setCity("Lyon");

        sensor.setId(101L);
        sensor.setLocation(loc1);

        assertEquals("Paris", sensor.getLocation().getCity());

        // change location
        sensor.setLocation(loc2);
        assertEquals("Lyon", sensor.getLocation().getCity());
    }

    @Test
    public void testSensorParameterTypes() {
        String[] parameters = {"pm10", "pm25", "no2", "o3", "co"};

        for (String param : parameters) {
            sensor.setParameter(param);
            assertEquals(param, sensor.getParameter());
        }
    }

    @Test
    public void testSensorNullLocation() {
        sensor.setId(101L);
        sensor.setParameter("pm10");

        assertNull(sensor.getLocation());
    }
}
