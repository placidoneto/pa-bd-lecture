package com.seuprojeto.repository;
import com.seuprojeto.domain.Aluno;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class AlunoRepository implements PanacheRepository<Aluno> {
    // Retorna todos os alunos ativos
    public List<Aluno> ativos(){
        return find("ativo", true).list();
    }
}