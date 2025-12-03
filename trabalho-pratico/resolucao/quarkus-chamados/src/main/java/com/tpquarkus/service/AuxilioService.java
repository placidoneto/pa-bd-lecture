package com.tpquarkus.service;

import com.tpquarkus.DTO.AuxilioDTO;
import com.tpquarkus.domain.Auxilio;
import com.tpquarkus.mapper.AuxilioMapper;
import com.tpquarkus.repository.AuxilioRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.NotFoundException;
import io.quarkus.panache.common.Sort;
import java.util.List;
import java.util.stream.Collectors;

@ApplicationScoped
public class AuxilioService {

    @Inject
    AuxilioRepository repository;

    public List<AuxilioDTO> listarTodos() {
        return repository.listAll(Sort.by("nome")).stream()
                .map(AuxilioMapper::toDTO)
                .collect(Collectors.toList());
    }

    public AuxilioDTO buscarPorId(Long id) {
        Auxilio auxilio = repository.findById(id);

        if (auxilio == null) {
            throw new NotFoundException("Auxílio não encontrado com o ID: " + id);
        }

        return AuxilioMapper.toDTO(auxilio);
    }

    @Transactional
    public AuxilioDTO criar(AuxilioDTO request) {
        if (repository.count("LOWER(nome)", request.nome.toLowerCase()) > 0) {
            throw new IllegalArgumentException("Já existe um auxílio com este nome.");
        }

        Auxilio auxilio = new Auxilio();
        auxilio.nome = request.nome;
        auxilio.descricao = request.descricao;

        auxilio.ativo = (request.ativo != null) ? request.ativo : true;

        repository.persist(auxilio);

        return AuxilioMapper.toDTO(auxilio);
    }

    public List<AuxilioDTO> listarAtivos() {
        return repository.list("ativo", true).stream()
                .map(AuxilioMapper::toDTO)
                .collect(Collectors.toList());
    }

    public List<AuxilioDTO> listarDesativados() {
        return repository.list("ativo", false).stream()
                .map(AuxilioMapper::toDTO)
                .collect(Collectors.toList());
    }

    @Transactional
    public AuxilioDTO atualizar(Long id, AuxilioDTO request) {
        Auxilio auxilio = repository.findById(id);

        if (auxilio == null) {
            throw new NotFoundException("Auxílio não encontrado");
        }

        auxilio.nome = request.nome;
        auxilio.descricao = request.descricao;

        if (request.ativo != null) {
            auxilio.ativo = request.ativo;
        }

        return AuxilioMapper.toDTO(auxilio);
    }
}