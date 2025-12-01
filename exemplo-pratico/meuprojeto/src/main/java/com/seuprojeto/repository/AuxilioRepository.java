package com.seuprojeto.repository;
import com.seuprojeto.domain.Auxilio;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class AuxilioRepository implements PanacheRepository<Auxilio> {
    public List<Auxilio> ativos(){
        return find("ativo", true).list();
    }
}