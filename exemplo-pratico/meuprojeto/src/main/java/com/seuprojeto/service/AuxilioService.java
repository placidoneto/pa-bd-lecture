package com.seuprojeto.service;
import java.util.List;

import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.repository.AuxilioRepository;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
public class AuxilioService {
    
    @Inject
    AuxilioRepository repository;

    public List<Auxilio> listarAuxilios() {
        return repository.listAll();
    }

    public List<Auxilio> listarAuxiliosAtivos() {
        return repository.ativos();
    }
    
    public Auxilio buscarPorId(Long id) {
        return repository.findById(id);
    }

    public void salvar(Auxilio auxilio) {
        repository.persist(auxilio);
    }   

    public boolean remover(Long id) {
        return repository.deleteById(id);
    }   

}
