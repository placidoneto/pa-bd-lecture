package com.clinicavet.petcare.model;

import jakarta.persistence.*;

@Entity
public class Tutor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String nome;
    private String contato;

    public Tutor() {}

    public Tutor(String nome, String contato){
        this.nome = nome;
        this.contato = contato;
    }

    public Long getId(){ 
        return id;
    }
    
    public void setId(Long id){
        this.id = id;
    }

    public String getNome(){
        return nome;
    }

    public void setNome(String nome){
        this.nome = nome;
    }

    public String getContato(){
        return contato;
    }

    public void setContato(String contato){
        this.contato = contato;
    }
}

