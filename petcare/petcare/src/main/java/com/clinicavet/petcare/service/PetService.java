package com.clinicavet.petcare.service;

import com.clinicavet.petcare.model.Pet;
import com.clinicavet.petcare.repository.PetRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class PetService {

    private final PetRepository petRepository;

    public PetService(PetRepository petRepository) {
        this.petRepository = petRepository;
    }

    public Pet salvar(Pet pet) {
        return petRepository.save(pet);
    }

    public List<Pet> listarTodos() {
        return petRepository.findAll();
    }

    public Optional<Pet> buscarPorId(Long id) {
        return petRepository.findById(id);
    }

    public void deletar(Long id) {
        petRepository.deleteById(id);
    }

    public Pet atualizar(Long id, Pet dadosAtualizados) {
        return petRepository.findById(id).map(pet -> {
            pet.setNome(dadosAtualizados.getNome());
            pet.setIdade(dadosAtualizados.getIdade());
            pet.setTipo(dadosAtualizados.getTipo());
            pet.setRaca(dadosAtualizados.getRaca());
            return petRepository.save(pet);
        }).orElseThrow(() -> new RuntimeException("Pet não encontrado"));
    }
}
