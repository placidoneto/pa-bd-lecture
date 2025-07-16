package com.clinicavet.petcare.controller;

import com.clinicavet.petcare.model.Vacina;
import com.clinicavet.petcare.repository.VacinaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/vacinas")
public class VacinaController {

    @Autowired
    private VacinaRepository vacinaRepository;

    @GetMapping
    public List<Vacina> listar() {
        return vacinaRepository.findAll();
    }

    @PostMapping
    public Vacina criar(@RequestBody Vacina vacina) {
        return vacinaRepository.save(vacina);
    }

    @PutMapping("/{id}")
    public Vacina atualizar(@PathVariable Long id, @RequestBody Vacina novaVacina) {
        return vacinaRepository.findById(id).map(v -> {
            v.setNome(novaVacina.getNome());
            v.setDataAplicacao(novaVacina.getDataAplicacao());
            v.setPet(novaVacina.getPet());
            return vacinaRepository.save(v);
        }).orElseThrow();
    }

    @DeleteMapping("/{id}")
    public void deletar(@PathVariable Long id) {
        vacinaRepository.deleteById(id);
    }
}
