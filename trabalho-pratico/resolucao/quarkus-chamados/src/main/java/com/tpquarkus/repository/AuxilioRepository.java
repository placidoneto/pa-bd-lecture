package com.tpquarkus.repository;
import com.tpquarkus.domain.Auxilio;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class AuxilioRepository implements PanacheRepository<Auxilio>{
    //Retorna todos os auxilios ativos
    public List<Auxilio> ativos(){
        return find("ativo", true).list();
    }

    //Retorna todos os auxilio desativados
    public List<Auxilio> desativados(){
        return find("ativo", false).list();
    }

}
