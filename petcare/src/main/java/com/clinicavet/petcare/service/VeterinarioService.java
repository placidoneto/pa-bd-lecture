package com.clinicavet.petcare.service;

import com.clinicavet.petcare.model.Veterinario;
import com.clinicavet.petcare.repository.VeterinarioRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class VeterinarioService {

    private final VeterinarioRepository veterinarioRepository;

    public VeterinarioService(VeterinarioRepository veterinarioRepository) {
        this.veterinarioRepository = veterinarioRepository;
    }

    public Veterinario salvar(Veterinario veterinario) {
        return veterinarioRepository.save(veterinario);
    }

    public List<Veterinario> listarTodos() {
        return veterinarioRepository.findAll();
    }

    public Optional<Veterinario> buscarPorId(Long id) {
        return veterinarioRepository.findById(id);
    }

    public Veterinario atualizar(Long id, Veterinario veterinario) {
        Veterinario existente = veterinarioRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Veterinário não encontrado"));
        existente.setNome(veterinario.getNome());
        existente.setEspecialidade(veterinario.getEspecialidade());
        return veterinarioRepository.save(existente);
    }

    public void deletar(Long id) {
        veterinarioRepository.deleteById(id);
    }
}