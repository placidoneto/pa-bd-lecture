package com.clinicavet.petcare.service;

import com.clinicavet.petcare.model.Tutor;
import com.clinicavet.petcare.repository.TutorRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class TutorService {

    private final TutorRepository tutorRepository;

    public TutorService(TutorRepository tutorRepository) {
        this.tutorRepository = tutorRepository;
    }

    public Tutor salvar(Tutor tutor) {
        return tutorRepository.save(tutor);
    }

    public List<Tutor> listarTodos() {
        return tutorRepository.findAll();
    }

    public Optional<Tutor> buscarPorId(Long id) {
        return tutorRepository.findById(id);
    }

    public Tutor atualizar(Long id, Tutor tutor) {
        Tutor existente = tutorRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Tutor não encontrado"));
        existente.setNome(tutor.getNome());
        existente.setContato(tutor.getContato());
        return tutorRepository.save(existente);
    }

    public void deletar(Long id) {
        tutorRepository.deleteById(id);
    }
}