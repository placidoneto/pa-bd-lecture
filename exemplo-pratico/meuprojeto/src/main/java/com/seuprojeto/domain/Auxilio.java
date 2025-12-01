package com.seuprojeto.domain;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;

@Entity
public class Auxilio extends PanacheEntity {
    public String titulo;
    public String descricao;
    public Boolean ativo;
}
