package org.example.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import java.util.List;

@Entity
@Table(name = "location")
public class Location {

    @Id
    private Long id;

    private String city;
    private String country;
    private Double latitude;
    private Double longitude;

    @OneToMany(mappedBy = "location")
    private List<Sensor> sensors;
}

