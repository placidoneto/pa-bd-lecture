package com.seuprojeto.repository;
import com.seuprojeto.domain.Aluno;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.domain.BeneficioAluno;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class BeneficioAlunoRepository implements PanacheRepository<BeneficioAluno> {
    public BeneficioAluno buscarAtivo(Aluno aluno, Auxilio auxilio) {
        return find("aluno = ?1 AND auxilio = ?2 AND ativo = true", // faz uma consulta JPQL, ?1 vai ser substituído por aluno e ?2 por beneficioAluno
                aluno, auxilio).firstResult(); // vai retornar o primeiro resultado encontrado ou null
    }

    public List<BeneficioAluno> ativos() {
        return find("ativo", true).list();
    }
}