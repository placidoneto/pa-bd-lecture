package com.tpquarkus.mapper;
import com.tpquarkus.DTO.AlunoDTO;
import com.tpquarkus.domain.Aluno;

public class AlunoMapper {
    // usado na api para entrada e saida de dados
    public static AlunoDTO toDTO(Aluno aluno) {
        AlunoDTO dto = new AlunoDTO();
        dto.id = aluno.id;
        dto.nome = aluno.nome;
        dto.matricula = aluno.matricula;
        dto.curso = aluno.curso;
        dto.ativo = aluno.ativo;
        return dto;
    }
    // usado  para persisitr o dado no banco
    public static Aluno toEntity(AlunoDTO dto) {
        Aluno aluno = new Aluno();
        aluno.nome = dto.nome;
        aluno.matricula = dto.matricula;
        aluno.curso = dto.curso;
        aluno.ativo = dto.ativo;
        return aluno;
    }    
}
