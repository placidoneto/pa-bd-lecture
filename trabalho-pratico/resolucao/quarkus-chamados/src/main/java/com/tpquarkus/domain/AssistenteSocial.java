package com.tpquarkus.domain;
import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;

@Entity
public class AssistenteSocial extends PanacheEntity {

    public String nome;
    public String matricula;
    public Boolean ativo;
}