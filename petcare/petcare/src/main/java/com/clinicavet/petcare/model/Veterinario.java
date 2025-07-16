package com.clinicavet.petcare.model;

import jakarta.persistence.*;

@Entity
public class Veterinario {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String nome;
    private String especialidade;

    public Veterinario() {}

    public Veterinario(String nome, String especialidade){
        this.nome = nome;
        this.especialidade = especialidade;
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

    public String getEspecialidade(){
        return especialidade;
    }

    public void setEspecialidade(String especialidade){
        this.especialidade = especialidade;
    }
}

