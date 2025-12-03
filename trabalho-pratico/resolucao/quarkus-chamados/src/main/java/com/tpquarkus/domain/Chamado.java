package com.tpquarkus.domain;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.*;

import java.time.LocalDateTime;
import com.tpquarkus.StatusChamado;

@Entity
public class Chamado extends PanacheEntity {

    @Column(nullable = false)
    public String descricao;

    public String resposta;

    @Enumerated(EnumType.STRING)
    public StatusChamado status;

    public LocalDateTime dataAbertura;

    public LocalDateTime dataAnalise;

    @ManyToOne
    public Aluno aluno;

    @ManyToOne
    public AssistenteSocial assistenteSocial;

    @ManyToOne
    public Auxilio auxilio;

}

