package com.seuprojeto.repository;
import com.seuprojeto.domain.Beneficio;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class BeneficioRepository implements PanacheRepository<Beneficio> {
    public List<Beneficio> ativos(){
        return find("ativo", true).list();
    }
}