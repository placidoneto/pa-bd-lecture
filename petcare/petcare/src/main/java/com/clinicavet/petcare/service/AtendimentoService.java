package com.clinicavet.petcare.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

import com.clinicavet.petcare.model.Atendimento;
import com.clinicavet.petcare.repository.AtendimentoRepository;

@Service
public class AtendimentoService {

    private final AtendimentoRepository atendimentoRepository;

    public AtendimentoService(AtendimentoRepository atendimentoRepository) {
        this.atendimentoRepository = atendimentoRepository;
    }

    public Atendimento salvar(Atendimento atendimento) {
        return atendimentoRepository.save(atendimento);
    }

    public List<Atendimento> listarTodos() {
        return atendimentoRepository.findAll();
    }

    public Optional<Atendimento> buscarPorId(Long id) {
        return atendimentoRepository.findById(id);
    }

    public void deletar(Long id) {
        atendimentoRepository.deleteById(id);
    }

    public Atendimento atualizar(Long id, Atendimento dadosAtualizados) {
        return atendimentoRepository.findById(id).map(atendimento -> {
            atendimento.setData(dadosAtualizados.getData());
            atendimento.setDescricao(dadosAtualizados.getDescricao());
            atendimento.setVeterinario(dadosAtualizados.getVeterinario());
            atendimento.setPet(dadosAtualizados.getPet());
            return atendimentoRepository.save(atendimento);
        }).orElseThrow(() -> new RuntimeException("Atendimento não encontrado"));
    }
}
