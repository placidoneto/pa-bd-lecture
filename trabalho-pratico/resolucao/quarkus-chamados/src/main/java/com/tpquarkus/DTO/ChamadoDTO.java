package com.tpquarkus.DTO;
import java.time.LocalDateTime;
import jakarta.validation.constraints.NotBlank;

import com.tpquarkus.StatusChamado;

public class ChamadoDTO {
    public Long id;

    @NotBlank(message = "A descrição não pode estar vazia")
    public String descricao;

    public String resposta;
    public StatusChamado status;
    public LocalDateTime dataAbertura;
    public LocalDateTime dataAnalise;
    public Long alunoId;
    public Long assistenteSocialId;
    public Long auxilioId;
}
