package openaq;

import io.hypersistence.utils.hibernate.type.json.JsonType;
import jakarta.persistence.*;
import org.hibernate.annotations.Type;

import java.time.OffsetDateTime;

@Entity
@Table(name = "measurements")
public class MeasurementEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    public Long id;

    @Column(nullable = false)
    public OffsetDateTime timestamp;

    @Column(nullable = false)
    public Double value;

    @Type(JsonType.class)
    @Column(columnDefinition = "jsonb", nullable = false)
    public Object sensor;

    @Type(JsonType.class)
    @Column(columnDefinition = "jsonb", nullable = false)
    public Object location;

    @Type(JsonType.class)
    @Column(columnDefinition = "jsonb", nullable = false)
    public Object raw;
}
