package com.tpquarkus.service;

import com.tpquarkus.DTO.AssistenteSocialDTO;
import com.tpquarkus.domain.AssistenteSocial;
import com.tpquarkus.mapper.AssistenteSocialMapper;
import com.tpquarkus.repository.AssistenteSocialRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.NotFoundException;
import io.quarkus.panache.common.Sort;
import java.util.List;
import java.util.stream.Collectors;

@ApplicationScoped
public class AssistenteSocialService {

    @Inject
    AssistenteSocialRepository repository;

    public List<AssistenteSocialDTO> listarTodos() {
        return repository.listAll(Sort.by("nome")).stream()
                .map(AssistenteSocialMapper::toDTO)
                .collect(Collectors.toList());
    }

    public AssistenteSocialDTO buscarPorId(Long id) {
        AssistenteSocial entity = repository.findById(id);

        if (entity == null) {
            throw new NotFoundException("Assistente Social não encontrada com ID: " + id);
        }

        return AssistenteSocialMapper.toDTO(entity);
    }

    @Transactional
    public AssistenteSocialDTO criar(AssistenteSocialDTO request) {
        if (repository.count("matricula", request.matricula) > 0) {
            throw new IllegalArgumentException("Já existe uma Assistente Social com esta matrícula.");
        }

        AssistenteSocial entity = new AssistenteSocial();
        entity.nome = request.nome;
        entity.matricula = request.matricula;

        entity.ativo = (request.ativo != null) ? request.ativo : true;

        repository.persist(entity);

        return AssistenteSocialMapper.toDTO(entity);
    }
}