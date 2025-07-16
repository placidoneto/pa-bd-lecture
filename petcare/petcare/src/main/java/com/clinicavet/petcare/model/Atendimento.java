package com.clinicavet.petcare.model;
import java.time.LocalDate;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class Atendimento{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private LocalDate data;
    private String descricao;
    @ManyToOne
    @JoinColumn(name = "veterinario_id", referencedColumnName = "id") 
    private Veterinario veterinario; 
    @ManyToOne
    @JoinColumn(name = "pet_id", referencedColumnName = "id") 
    private Pet pet;  

    public Atendimento () {}
    public Atendimento (LocalDate data, String descricao, Veterinario veterinario,Pet pet) {
        this.data = data;
        this.descricao = descricao;
        this.veterinario = veterinario;
        this.pet = pet;
    }

    public Long getId() { return this.id; }
    public void setId(Long id) { this.id = id; }

    public LocalDate getData() { return this.data; }
    public void setData(LocalDate data) { this.data = data; }

    public String getDescricao() { return descricao; }
    public void setDescricao(String descricao) { this.descricao = descricao; }

    public Veterinario getVeterinario() { return veterinario; }
    public void setVeterinario(Veterinario veterinario) { this.veterinario = veterinario; }

    public Pet getPet() { return pet; }
    public void setPet(Pet pet) { this.pet = pet; }

}