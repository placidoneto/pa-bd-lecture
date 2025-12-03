package com.tpquarkus.repository;
import com.tpquarkus.domain.AssistenteSocial;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class AssistenteSocialRepository implements PanacheRepository<AssistenteSocial>{
    
}
