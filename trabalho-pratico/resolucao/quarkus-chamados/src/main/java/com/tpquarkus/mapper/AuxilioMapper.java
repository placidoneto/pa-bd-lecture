package com.tpquarkus.mapper;
import com.tpquarkus.DTO.AuxilioDTO;
import com.tpquarkus.domain.Auxilio;

public class AuxilioMapper {

    public static AuxilioDTO toDTO(Auxilio auxilio) {
        AuxilioDTO dto = new AuxilioDTO();
        dto.id = auxilio.id;
        dto.nome = auxilio.nome;
        dto.descricao = auxilio.descricao;
        dto.ativo = auxilio.ativo;
        return dto;
    }
    public static Auxilio toEntity(AuxilioDTO dto) {
        Auxilio auxilio = new Auxilio();
        auxilio.nome = dto.nome;
        auxilio.descricao = dto.descricao;
        auxilio.ativo = dto.ativo;
        return auxilio;
    }    
}
