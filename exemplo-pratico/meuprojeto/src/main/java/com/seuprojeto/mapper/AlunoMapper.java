package com.seuprojeto.mapper;

import com.seuprojeto.DTO.AlunoDTO;
import com.seuprojeto.domain.Aluno;

public class AlunoMapper {
    // usado na api para entrada e saida de dados
    public static AlunoDTO toDTO(Aluno aluno) {
        AlunoDTO dto = new AlunoDTO();
        dto.id = aluno.id;
        dto.nome = aluno.nome;
        dto.email = aluno.email;
        dto.ativo = aluno.ativo;
        return dto;
    }
    // usado  para persisitr o dado no banco
    public static Aluno toEntity(AlunoDTO dto) {
        Aluno aluno = new Aluno();
        aluno.nome = dto.nome;
        aluno.email = dto.email;
        aluno.ativo = dto.ativo;
        return aluno;
    }
}
