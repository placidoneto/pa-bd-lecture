package com.clinicavet.petcare.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

import com.clinicavet.petcare.model.Medicamento;
import com.clinicavet.petcare.repository.MedicamentoRepository;

@Service
public class MedicamentoService {
    
    private final MedicamentoRepository medicamentoRepository;

    public MedicamentoService(MedicamentoRepository medicamentoRepository) {
        this.medicamentoRepository = medicamentoRepository;
    }

    public Medicamento salvar(Medicamento medicamento) {
        return medicamentoRepository.save(medicamento);
    }

    public List<Medicamento> listarTodos() {
        return medicamentoRepository.findAll();
    }

    public Optional<Medicamento> buscarPorId(Long id) {
        return medicamentoRepository.findById(id);
    }

    public void deletar(Long id) {
        medicamentoRepository.deleteById(id);
    }

    public Medicamento atualizar(Long id, Medicamento dadosAtualizados) {
        return medicamentoRepository.findById(id).map(medicamento -> {
            medicamento.setNome(dadosAtualizados.getNome());
            medicamento.setDosagem(dadosAtualizados.getDosagem());
            medicamento.setPet(dadosAtualizados.getPet());
            return medicamentoRepository.save(medicamento);
        }).orElseThrow(() -> new RuntimeException("Medicamento não encontrado"));
    }

}
