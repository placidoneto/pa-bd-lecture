package com.seuprojeto.mapper;

import com.seuprojeto.DTO.AuxilioDTO;
import com.seuprojeto.domain.Auxilio;


public class AuxilioMapper {
    // usado na api para entrada e saida de dados
    public static AuxilioDTO toDTO(Auxilio auxlio) {
        AuxilioDTO dto = new AuxilioDTO();
        dto.id = auxlio.id;
        dto.titulo = auxlio.titulo;
        dto.descricao = auxlio.descricao;
        dto.ativo = auxlio.ativo;
        return dto;
    }
    // usado  para persisitr o dado no banco
    public static Auxilio toEntity(AuxilioDTO dto) {
        Auxilio auxlio = new Auxilio();
        auxlio.titulo = dto.titulo;
        auxlio.descricao = dto.descricao;
        auxlio.ativo = dto.ativo;
        return auxlio;
    }
}
