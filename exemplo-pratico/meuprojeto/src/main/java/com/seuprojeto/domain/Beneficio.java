package com.seuprojeto.domain;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class Beneficio extends PanacheEntity {
    
    public String nome;
    public String descricao;
    public Boolean ativo;

    @ManyToOne
    @JoinColumn(name = "auxilio_id") // nome da coluna FK
    public Auxilio auxilio;

}
