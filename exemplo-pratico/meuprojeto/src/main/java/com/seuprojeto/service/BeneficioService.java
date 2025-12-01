package com.seuprojeto.service;
import java.util.List;

import com.seuprojeto.domain.Beneficio;
import com.seuprojeto.repository.BeneficioRepository;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
public class BeneficioService {
    
    @Inject
    BeneficioRepository repository;

    public List<Beneficio> listarBeneficio() {
        return repository.listAll();
    }

    public List<Beneficio> listarBeneficiosAtivos() {
        return repository.ativos();
    }
    
    public Beneficio buscarPorId(Long id) {
        return repository.findById(id);
    }

    public void salvar(Beneficio auxilio) {
        repository.persist(auxilio);
    }   

    public boolean remover(Long id) {
        return repository.deleteById(id);
    }   

}
