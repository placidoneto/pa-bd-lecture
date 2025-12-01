package com.seuprojeto.domain;

import java.time.LocalDate;

import org.hibernate.annotations.CreationTimestamp; // já gera o id automaticamente

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;


@Entity
public class BeneficioAluno extends PanacheEntity {
    
    public String observacao;
    @CreationTimestamp // registra automaticamente quando é criado
    public LocalDate data_concessao;
    public Boolean ativo;

    @ManyToOne
    @JoinColumn(name = "aluno_id") // nome da coluna FK
    public Aluno aluno;

    @ManyToOne
    @JoinColumn(name = "auxilio_id") // nome da coluna FK
    public Auxilio auxilio;

}
