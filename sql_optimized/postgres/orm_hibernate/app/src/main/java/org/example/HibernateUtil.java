package org.example;

import org.example.entity.Location;
import org.example.entity.Measurement;
import org.example.entity.Sensor;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class HibernateUtil {

    private static final SessionFactory sessionFactory =
        new Configuration()
            .configure()
            .addAnnotatedClass(Location.class)
            .addAnnotatedClass(Sensor.class)
            .addAnnotatedClass(Measurement.class)
            .buildSessionFactory();

    public static SessionFactory getSessionFactory() {
        return sessionFactory;
    }
}
