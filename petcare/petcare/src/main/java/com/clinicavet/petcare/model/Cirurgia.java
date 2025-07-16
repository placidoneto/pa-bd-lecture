package com.clinicavet.petcare.model;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
public class Cirurgia {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;    

    private String nome;
    private LocalDate data;

    @ManyToOne
    @JoinColumn(name = "pet_id", referencedColumnName = "id")
    private Pet pet;

    public Cirurgia() {}

    public Cirurgia(String nome, LocalDate data, Pet pet) {
        this.nome = nome;
        this.data = data;
        this.pet = pet;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }

    public LocalDate getData() { return data; }
    public void setData(LocalDate data) { this.data = data; }

    public Pet getPet() { return pet; }
    public void setPet(Pet pet) { this.pet = pet; }
} 