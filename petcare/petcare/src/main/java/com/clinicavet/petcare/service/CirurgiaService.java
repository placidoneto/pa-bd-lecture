package com.clinicavet.petcare.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

import com.clinicavet.petcare.model.Cirurgia;
import com.clinicavet.petcare.repository.CirurgiaRepository;

@Service
public class CirurgiaService {

    private final CirurgiaRepository cirurgiaRepository;

    public CirurgiaService(CirurgiaRepository cirurgiaRepository) {
        this.cirurgiaRepository = cirurgiaRepository;
    }

    public Cirurgia salvar(Cirurgia cirurgia) {
        return cirurgiaRepository.save(cirurgia);
    }

    public List<Cirurgia> listarTodos() {
        return cirurgiaRepository.findAll();
    }

    public Optional<Cirurgia> buscarPorId(Long id) {
        return cirurgiaRepository.findById(id);
    }

    public void deletar(Long id) {
        cirurgiaRepository.deleteById(id);
    }

    public Cirurgia atualizar(Long id, Cirurgia dadosAtualizados) {
        return cirurgiaRepository.findById(id).map(cirurgia -> {
            cirurgia.setNome(dadosAtualizados.getNome());
            cirurgia.setData(dadosAtualizados.getData());
            cirurgia.setPet(dadosAtualizados.getPet());
            return cirurgiaRepository.save(cirurgia);
        }).orElseThrow(() -> new RuntimeException("Cirurgia não encontrada"));
    }
} 