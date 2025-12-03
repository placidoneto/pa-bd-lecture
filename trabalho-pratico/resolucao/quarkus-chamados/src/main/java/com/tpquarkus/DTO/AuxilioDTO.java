package com.tpquarkus.DTO;

import jakarta.validation.constraints.NotBlank;

public class AuxilioDTO {
    public Long id;

    @NotBlank(message = "O nome do auxílio é obrigatório")
    public String nome;

    public String descricao;

    public Boolean ativo;
}
