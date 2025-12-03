package com.tpquarkus.service;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import java.util.stream.Collectors;

import com.tpquarkus.DTO.ChamadoDTO;
import com.tpquarkus.StatusChamado;
import com.tpquarkus.domain.Aluno;
import com.tpquarkus.domain.AssistenteSocial;
import com.tpquarkus.domain.Auxilio;
import com.tpquarkus.domain.Chamado;
import com.tpquarkus.mapper.ChamadoMapper;
import com.tpquarkus.repository.AlunoRepository;
import com.tpquarkus.repository.AssistenteSocialRepository;
import com.tpquarkus.repository.AuxilioRepository;
import com.tpquarkus.repository.ChamadoRepository;

import io.quarkus.panache.common.Sort;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import jakarta.ws.rs.NotFoundException;

@ApplicationScoped
public class ChamadoService {

    @Inject
    ChamadoRepository chamadoRepository;

    @Inject
    AlunoRepository alunoRepository;
    @Inject
    AssistenteSocialRepository assistenteSocialRepository;
    @Inject
    AuxilioRepository auxilioRepository;

    public List<ChamadoDTO> listarTodos() {
        return chamadoRepository.listAll(Sort.descending("dataAbertura")).stream()
                .map(ChamadoMapper::toDTO)
                .collect(Collectors.toList());
    }

    public ChamadoDTO buscarPorId(Long id) {
        Chamado chamado = chamadoRepository.findById(id);

        if (chamado == null) {
            throw new NotFoundException("Chamado não encontrado com o ID: " + id);
        }

        return ChamadoMapper.toDTO(chamado);
    }

    public List<ChamadoDTO> buscarPorStatus(StatusChamado status) {
        return chamadoRepository.list("status", status).stream()
                .map(ChamadoMapper::toDTO)
                .collect(Collectors.toList());
    }

    public List<ChamadoDTO> buscarPorMatriculaAluno(String matricula) {
        return chamadoRepository.list("aluno.matricula", matricula).stream()
                .map(ChamadoMapper::toDTO)
                .collect(Collectors.toList());
    }

    public List<ChamadoDTO> buscarPorNomeAuxilio(String nome) {
        return chamadoRepository.list("LOWER(auxilio.nome) = ?1", nome.toLowerCase()).stream()
                .map(ChamadoMapper::toDTO)
                .collect(Collectors.toList());
    }

    @Transactional
    public ChamadoDTO create(@Valid ChamadoDTO request) {
        Aluno aluno = alunoRepository.findById(request.alunoId);
        if (aluno == null) throw new NotFoundException("Aluno não encontrado");

        AssistenteSocial assistenteSocial = assistenteSocialRepository.findById(request.assistenteSocialId);
        if (assistenteSocial == null) throw new NotFoundException("Assistente Social não encontrado");

        Auxilio auxilio = auxilioRepository.findById(request.auxilioId);
        if (auxilio == null) throw new NotFoundException("Auxílio não encontrado");

        LocalDateTime agora = LocalDateTime.now(ZoneId.of("America/Sao_Paulo"));

        Chamado chamado = new Chamado();
        chamado.descricao = request.descricao;
        chamado.resposta = null;
        chamado.status = StatusChamado.ABERTO;
        chamado.dataAbertura = agora;
        chamado.dataAnalise = null;
        chamado.aluno = aluno;
        chamado.assistenteSocial = assistenteSocial;
        chamado.auxilio = auxilio;

        chamadoRepository.persist(chamado);

        return ChamadoMapper.toDTO(chamado);
    }

    @Transactional
    public ChamadoDTO responder(Long id, String resposta) {
        Chamado chamado = chamadoRepository.findById(id);
        if (chamado == null) {
            throw new NotFoundException("Chamado não encontrado");
        }

        chamado.resposta = resposta;
        chamado.status = StatusChamado.EM_ANALISE;
        chamado.dataAnalise = LocalDateTime.now(ZoneId.of("America/Sao_Paulo"));

        return ChamadoMapper.toDTO(chamado);
    }

    @Transactional
    public ChamadoDTO update(Long id, ChamadoDTO request) {
        Chamado chamado = chamadoRepository.findById(id);
        if (chamado == null) {
            throw new NotFoundException("Chamado não encontrado");
        }

        chamado.descricao = request.descricao;
        chamado.resposta = request.resposta;
        chamado.status = request.status;
        chamado.dataAnalise = request.dataAnalise;

        if (request.alunoId != null) {
            Aluno aluno = alunoRepository.findById(request.alunoId);
            if (aluno == null) throw new NotFoundException("Aluno não encontrado");
            chamado.aluno = aluno;
        }

        if (request.assistenteSocialId != null) {
            AssistenteSocial as = assistenteSocialRepository.findById(request.assistenteSocialId);
            if (as == null) throw new NotFoundException("Assistente Social não encontrada");
            chamado.assistenteSocial = as;
        }

        if (request.auxilioId != null) {
            Auxilio auxilio = auxilioRepository.findById(request.auxilioId);
            if (auxilio == null) throw new NotFoundException("Auxílio não encontrado");
            chamado.auxilio = auxilio;
        }

        if (request.resposta != null){
            chamado.status = StatusChamado.EM_ANALISE;
            chamado.dataAnalise = LocalDateTime.now(ZoneId.of("America/Sao_Paulo"));
        }

        return ChamadoMapper.toDTO(chamado);
    }

    @Transactional
    public ChamadoDTO close(Long id) {
        Chamado chamado = chamadoRepository.findById(id);
        if (chamado == null) {
            throw new NotFoundException("Chamado não encontrado");
        }

        if (chamado.status != StatusChamado.EM_ANALISE) {
            throw new IllegalStateException("Somente chamados em análise podem ser fechados");
        }

        chamado.status = StatusChamado.FECHADO;
        return ChamadoMapper.toDTO(chamado);
    }

    @Transactional
    public void delete(Long id) {
        boolean deletou = chamadoRepository.deleteById(id);

        if (!deletou) {
            throw new NotFoundException("Não foi possível deletar: Chamado não encontrado");
        }
    }
}