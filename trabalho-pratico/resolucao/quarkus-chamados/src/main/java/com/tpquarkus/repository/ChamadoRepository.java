package com.tpquarkus.repository;
import com.tpquarkus.StatusChamado;
import com.tpquarkus.domain.Chamado;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class ChamadoRepository implements PanacheRepository<Chamado>{
    //Busca chamado por status
    public List<Chamado> findByStatus(StatusChamado status){
        return find("status", status).list();
    }

    //Busca chamado por aluno
    public List<Chamado> findByAluno(String matricula){
        return find("aluno.matricula", matricula).list();
    }

    //Busca chamado por auxilio 
    public List<Chamado> findByAuxilio(String nome){
        return find("auxilio.nome", nome).list();
    }
}
