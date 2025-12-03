package com.tpquarkus.mapper;
import com.tpquarkus.DTO.ChamadoDTO;
import com.tpquarkus.domain.Chamado;
import com.tpquarkus.domain.Aluno;
import com.tpquarkus.domain.AssistenteSocial;
import com.tpquarkus.domain.Auxilio;

public class ChamadoMapper {
    public static ChamadoDTO toDTO(Chamado chamado) {
        ChamadoDTO dto = new ChamadoDTO();
        dto.id = chamado.id;
        dto.descricao = chamado.descricao;
        dto.resposta = chamado.resposta;
        dto.status = chamado.status;
        dto.dataAbertura = chamado.dataAbertura;
        dto.dataAnalise = chamado.dataAnalise;

        dto.alunoId = chamado.aluno.id;
        dto.assistenteSocialId = chamado.assistenteSocial.id;
        dto.auxilioId = chamado.auxilio.id;
        return dto;
    }

    public static Chamado toEntity(ChamadoDTO dto) {
        Chamado chamado = new Chamado();
        chamado.descricao = dto.descricao;
        chamado.status = dto.status;
        chamado.dataAbertura = dto.dataAbertura;
        chamado.dataAnalise = dto.dataAnalise;
        chamado.resposta = dto.resposta;

        Aluno aluno = new Aluno();
        aluno.id = dto.alunoId;
        chamado.aluno = aluno;

        AssistenteSocial assistenteSocial = new AssistenteSocial();
        assistenteSocial.id = dto.assistenteSocialId;
        chamado.assistenteSocial = assistenteSocial;

        Auxilio auxilio = new Auxilio();
        auxilio.id = dto.auxilioId;
        chamado.auxilio = auxilio;

        return chamado;
    }

}