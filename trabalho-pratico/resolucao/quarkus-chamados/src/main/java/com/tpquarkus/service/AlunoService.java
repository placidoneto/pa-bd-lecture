package com.tpquarkus.service;

import com.tpquarkus.DTO.AlunoDTO;
import com.tpquarkus.domain.Aluno;
import com.tpquarkus.mapper.AlunoMapper;
import com.tpquarkus.repository.AlunoRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.NotFoundException;
import io.quarkus.panache.common.Sort;
import java.util.List;
import java.util.stream.Collectors;

@ApplicationScoped
public class AlunoService {

    @Inject
    AlunoRepository alunoRepository;

    public List<AlunoDTO> listarTodos() {
        return alunoRepository.listAll(Sort.by("nome")).stream()
                .map(AlunoMapper::toDTO)
                .collect(Collectors.toList());
    }

    public AlunoDTO buscarPorId(Long id) {
        Aluno aluno = alunoRepository.findById(id);

        if (aluno == null) {
            throw new NotFoundException("Aluno não encontrado com o ID: " + id);
        }

        return AlunoMapper.toDTO(aluno);
    }

    @Transactional
    public AlunoDTO criar(AlunoDTO request) {
        if (alunoRepository.count("matricula", request.matricula) > 0) {
            throw new IllegalArgumentException("Já existe um aluno com esta matrícula.");
        }

        Aluno aluno = new Aluno();
        aluno.nome = request.nome;
        aluno.matricula = request.matricula;
        aluno.curso = request.curso;

        aluno.ativo = true;

        alunoRepository.persist(aluno);

        return AlunoMapper.toDTO(aluno);
    }

    public List<AlunoDTO> listarAtivos() {
        return alunoRepository.list("ativo", true).stream()
                .map(AlunoMapper::toDTO)
                .collect(Collectors.toList());
    }

    public List<AlunoDTO> listarDesativados() {
        return alunoRepository.list("ativo", false).stream()
                .map(AlunoMapper::toDTO)
                .collect(Collectors.toList());
    }

    @Transactional
    public AlunoDTO atualizar(Long id, AlunoDTO request) {
        Aluno aluno = alunoRepository.findById(id);

        if (aluno == null) {
            throw new NotFoundException("Aluno não encontrado");
        }

        aluno.nome = request.nome;
        aluno.curso = request.curso;

        if (request.ativo != null) {
            aluno.ativo = request.ativo;
        }

        return AlunoMapper.toDTO(aluno);
    }
}