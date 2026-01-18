package org.example.entity;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class LocationTest {

    private Location location;

    @BeforeEach
    public void setUp() {
        location = new Location();
    }

    @Test
    public void testLocationCreation() {
        location.setId(1L);
        location.setCity("Paris");
        location.setCountry("FR");
        location.setLatitude(48.8566);
        location.setLongitude(2.3522);

        assertEquals(1L, location.getId());
        assertEquals("Paris", location.getCity());
        assertEquals("FR", location.getCountry());
        assertEquals(48.8566, location.getLatitude());
        assertEquals(2.3522, location.getLongitude());
    }

    @Test
    public void testLocationWithNullValues() {
        location.setId(2L);
        location.setCity("Unknown");

        assertEquals(2L, location.getId());
        assertEquals("Unknown", location.getCity());
        assertNull(location.getCountry());
    }

    @Test
    public void testLocationSensorsRelationship() {
        location.setId(1L);
        location.setCity("Paris");

        Sensor sensor = new Sensor();
        sensor.setId(101L);
        sensor.setParameter("pm10");
        sensor.setLocation(location);

        List<Sensor> sensors = new ArrayList<>();
        sensors.add(sensor);
        location.setSensors(sensors);

        assertEquals(1, location.getSensors().size());
        assertEquals("pm10", location.getSensors().get(0).getParameter());
    }

    @Test
    public void testLocationCoordinates() {
        location.setId(1L);
        location.setLatitude(40.7128);
        location.setLongitude(-74.0060);

        assertTrue(location.getLatitude() >= -90 && location.getLatitude() <= 90);
        assertTrue(location.getLongitude() >= -180 && location.getLongitude() <= 180);
    }

    @Test
    public void testMultipleSensorsPerLocation() {
        location.setId(1L);
        location.setCity("Paris");

        List<Sensor> sensors = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            Sensor sensor = new Sensor();
            sensor.setId((long) i);
            sensor.setParameter("pm10");
            sensors.add(sensor);
        }
        location.setSensors(sensors);

        assertEquals(5, location.getSensors().size());
    }
}
