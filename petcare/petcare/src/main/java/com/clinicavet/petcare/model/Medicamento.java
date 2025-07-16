package com.clinicavet.petcare.model;

import jakarta.persistence.*;

@Entity
public class Medicamento {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String nome;
    private String dosagem;

    @ManyToOne
    @JoinColumn(name = "pet_id", referencedColumnName = "id")
    private Pet pet;

    // Construtores
    public Medicamento() {}

    public Medicamento(String nome, String dosagem, Pet pet) {
        this.nome = nome;
        this.dosagem = dosagem;
        this.pet = pet;
    }

    // Getters e Setters
    public Long getId() { return id; }

    public void setId(Long id) { this.id = id; }

    public String getNome() { return nome; }

    public void setNome(String nome) { this.nome = nome; }

    public String getDosagem() { return dosagem; }

    public void setDosagem(String dosagem) { this.dosagem = dosagem; }

    public Pet getPet() { return pet; }

    public void setPet(Pet pet) { this.pet = pet; }
}
