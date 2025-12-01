package com.seuprojeto.mapper;

import com.seuprojeto.DTO.BeneficioDTO;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.domain.Beneficio;


public class BeneficioMapper {
    // usado na api para entrada e saida de dados
    public static BeneficioDTO toDTO(Beneficio beneficio) {
        BeneficioDTO dto = new BeneficioDTO();
        dto.id = beneficio.id;
        dto.nome = beneficio.nome;
        dto.descricao = beneficio.descricao;
        dto.ativo = beneficio.ativo;
        dto.auxilioId = beneficio.auxilio != null ? beneficio.auxilio.id : null;
        return dto;
    }
    // usado  para persisitr o dado no banco
    public static Beneficio toEntity(BeneficioDTO dto) {
        Beneficio beneficio = new Beneficio();
        beneficio.nome = dto.nome;
        beneficio.descricao = dto.descricao;
        beneficio.ativo = dto.ativo;
        // cria um Auxilio só com o ID
        Auxilio aux = new Auxilio();
        aux.id = dto.auxilioId;

        beneficio.auxilio = aux;
        return beneficio;
    }
}
