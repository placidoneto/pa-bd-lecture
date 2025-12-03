package com.tpquarkus.mapper;
import com.tpquarkus.DTO.AssistenteSocialDTO;
import com.tpquarkus.domain.AssistenteSocial;

public class AssistenteSocialMapper {
    // usado na api para entrada e saida de dados
    public static AssistenteSocialDTO toDTO(AssistenteSocial assistenteSocial) {
        AssistenteSocialDTO dto = new AssistenteSocialDTO();
        dto.id = assistenteSocial.id;
        dto.nome = assistenteSocial.nome;
        dto.matricula = assistenteSocial.matricula;
        dto.ativo = assistenteSocial.ativo;
        return dto;
    }

    // usado  para persisitr o dado no banco
    public static AssistenteSocial toEntity(AssistenteSocialDTO dto) {
        AssistenteSocial assistenteSocial = new AssistenteSocial();
        assistenteSocial.nome = dto.nome;
        assistenteSocial.matricula = dto.matricula;
        assistenteSocial.ativo = dto.ativo;
        return assistenteSocial;
    }
}
