package com.seuprojeto.service;
import java.util.List;

import com.seuprojeto.DTO.BeneficioAlunoDTO;
import com.seuprojeto.domain.Aluno;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.domain.BeneficioAluno;
import com.seuprojeto.exception.BusinessException;
import com.seuprojeto.repository.AlunoRepository;
import com.seuprojeto.repository.AuxilioRepository;
import com.seuprojeto.repository.BeneficioAlunoRepository;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;

@ApplicationScoped
public class BeneficioAlunoService {

    @Inject
    BeneficioAlunoRepository repository;

    @Inject
    AuxilioRepository auxilioRepository;

    @Inject
    AlunoRepository alunoRepository;

    public List<BeneficioAluno> listarBeneficiados() {
        return repository.listAll();
    }

    public List<BeneficioAluno> listarBeneficiadosAtivos() {
        return repository.ativos();
    }

    public BeneficioAluno buscarPorId(Long id) {
        return repository.findById(id);
    }

    @Transactional
    public void salvar(BeneficioAluno beneficiado) {
        repository.persist(beneficiado);
    }

    @Transactional
    public boolean remover(Long id) {
        return repository.deleteById(id);
    }

    @Transactional
    public BeneficioAluno inserirAlunoBeneficio(BeneficioAlunoDTO request) {

        // 1. Busca o benefício (auxílio) correto e o aluno de acordo com id fornecido 
        Auxilio auxilio = auxilioRepository.findById(request.auxilioId);
        Aluno aluno = alunoRepository.findById(request.alunoId);

        if (aluno == null) {
            throw new BusinessException("Aluno não encontrado");
        }

        if (auxilio == null) {
            throw new BusinessException("Auxílio não encontrado");
        }

        // 2. Verifica se esse aluno já tem esse mesmo benefício ativo
        BeneficioAluno beneficioAtivo = repository.buscarAtivo(aluno, auxilio);

        if (beneficioAtivo != null) {
            throw new BusinessException("Aluno já possui esse benefício ativo");
        }

        // 3. Cria um novo vínculo
        BeneficioAluno novo = new BeneficioAluno();
        novo.aluno = aluno;
        novo.auxilio = auxilio;
        novo.observacao = request.observacao;
        novo.data_concessao = request.data_concessao;
        novo.ativo = true;

        repository.persist(novo);
        return novo;
    }
}
