package com.tpquarkus.DTO;

import jakarta.validation.constraints.NotBlank;

public class AssistenteSocialDTO {
    public Long id;

    @NotBlank(message = "O nome é obrigatório")
    public String nome;

    @NotBlank(message = "A matrícula é obrigatória")
    public String matricula;

    public Boolean ativo;
}