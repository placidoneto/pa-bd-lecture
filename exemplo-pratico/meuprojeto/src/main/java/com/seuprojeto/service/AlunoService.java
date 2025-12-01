package com.seuprojeto.service;

import java.util.List;

import com.seuprojeto.domain.Aluno;
import com.seuprojeto.repository.AlunoRepository;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
public class AlunoService {

    @Inject
    AlunoRepository repository;

    public List<Aluno> listarAlunos() {
        return repository.listAll();
    }

    public List<Aluno> listarAlunosAtivos() {
        return repository.ativos();
    }

    public Aluno buscarPorId(Long id) {
        return repository.findById(id);
    }

    public void salvar(Aluno aluno) {
        repository.persist(aluno);
    }

    public boolean remover(Long id) {
        return repository.deleteById(id);
    }
}
